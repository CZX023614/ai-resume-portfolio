"""
AI Resume Backend — FastAPI server for:
  - AI Customer Service (RAG + DeepSeek)
  - AI Shopping Guide (Recommendation + DeepSeek)
  - Admin Panel (Knowledge Base & Prompt Management)
"""
import json
import uuid
import asyncio
from pathlib import Path
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from database import get_db, init_db
from rag_engine import rag_engine
from deepseek_client import chat_stream, get_deepseek_config

app = FastAPI(title="AI Resume Backend")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent  # standalone-pages root

# ═══════════════════════════════════════════════════════════
#  Static file mounts (frontend pages served from same origin)
# ═══════════════════════════════════════════════════════════
app.mount("/resume", StaticFiles(directory=str(ROOT_DIR / "ai-resume"), html=True), name="resume")
app.mount("/service", StaticFiles(directory=str(ROOT_DIR / "ai-customer-service"), html=True), name="service")
app.mount("/guide", StaticFiles(directory=str(ROOT_DIR / "ai-shopping-guide"), html=True), name="guide")
app.mount("/scrm", StaticFiles(directory=str(ROOT_DIR / "scrm-system"), html=True), name="scrm")
app.mount("/assets", StaticFiles(directory=str(ROOT_DIR / "scrm-system" / "assets")), name="scrm_assets")
app.mount("/cockpit", StaticFiles(directory=str(ROOT_DIR / "ai-data-cockpit"), html=True), name="cockpit")

@app.get("/")
def home():
    return FileResponse(str(ROOT_DIR / "ai-resume" / "index.html"))

@app.get("/photo.jpg")
def photo():
    return FileResponse(str(ROOT_DIR / "ai-resume" / "photo.jpg"))

# ═══════════════════════════════════════════════════════════
#  Startup
# ═══════════════════════════════════════════════════════════
@app.on_event("startup")
def startup():
    init_db()
    print("Database initialized.")

# ═══════════════════════════════════════════════════════════
#  Chat Models
# ═══════════════════════════════════════════════════════════
class ChatRequest(BaseModel):
    session_id: str = ""
    message: str

class ShoppingChatRequest(BaseModel):
    session_id: str = ""
    message: str
    user_profile_id: str = ""

# ═══════════════════════════════════════════════════════════
#  Customer Service Chat API
# ═══════════════════════════════════════════════════════════
@app.post("/api/customer-service/chat")
async def customer_service_chat(req: ChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    message = req.message.strip()

    # Save user message
    _save_chat(session_id, "customer_service", "user", message)

    # 1. RAG retrieval
    rag_results = rag_engine.search(message, top_k=5)
    rag_context = rag_engine.get_context_for_llm(message, top_k=5)

    # 2. Intent detection (simple keyword-based)
    intent, sub_intent, entities = _detect_intent(message)
    sentiment = _detect_sentiment(message)
    confidence = min(0.95, 0.5 + len(rag_results) * 0.1) if rag_results else 0.4

    # 3. Load system prompt
    system_prompt = _get_prompt("customer_service_system")
    fewshot = _get_prompt("customer_service_fewshot")

    # 4. Build messages with fallback logic
    auto_handoff = confidence < 0.75
    fallback_mode = not rag_context or confidence < 0.3

    fallback_instruction = ""
    if fallback_mode:
        fallback_instruction = (
            "\n\n## ⚠️ 兜底模式\n"
            "知识库中未找到匹配答案，请按以下规则回复：\n"
            "1. 先表达歉意，说明暂时无法准确解答\n"
            "2. 根据用户问题类型，提供1-2个通用建议或引导\n"
            "3. 建议用户联系人工客服获得更详细帮助\n"
            "4. 语气友善、不让用户感到被拒绝"
        )
    elif auto_handoff:
        fallback_instruction = (
            "\n\n## ⚠️ 低置信度\n"
            "请基于知识库尽力回答，并在结尾提醒用户如需更详细帮助可联系人工客服。"
        )

    full_system = system_prompt
    if rag_context:
        full_system += f"\n\n## 知识库参考（基于用户问题检索）\n{rag_context}"
    full_system += fallback_instruction
    if fewshot:
        full_system += f"\n\n## 对话示例\n{fewshot}"

    messages = [{"role": "user", "content": message}]

    async def event_stream():
        # Send pipeline info
        pipeline_data = {
            "intent": intent, "sub_intent": sub_intent,
            "entities": entities, "sentiment": sentiment,
            "confidence": {"score": confidence, "auto_handoff": auto_handoff},
            "rag_sources": [{"category": r['category'], "question": r['question'], "score": r['score']} for r in rag_results[:5]],
            "fallback": fallback_mode,
        }
        yield f"event: pipeline\ndata: {json.dumps(pipeline_data, ensure_ascii=False)}\n\n"

        # Stream LLM response
        full_response = ""
        async for chunk in chat_stream(messages, system_prompt=full_system):
            yield chunk
            if '"text"' in chunk:
                try:
                    d = json.loads(chunk[chunk.index('{'):])
                    full_response += d.get('text', '')
                except Exception:
                    pass

        # Save assistant message
        if full_response:
            _save_chat(session_id, "customer_service", "assistant", full_response, intent=intent, confidence=confidence)
        elif fallback_mode:
            full_response = "抱歉，我暂时无法准确回答这个问题 😊 建议您联系人工客服获取更详细的帮助。您可以在APP「我的-帮助中心」找到在线客服入口。"
            _save_chat(session_id, "customer_service", "assistant", full_response, intent=intent, confidence=confidence)

        yield f"event: done\ndata: {json.dumps({'session_id': session_id})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

# ═══════════════════════════════════════════════════════════
#  Shopping Guide Chat API
# ═══════════════════════════════════════════════════════════
@app.post("/api/shopping-guide/chat")
async def shopping_guide_chat(req: ShoppingChatRequest):
    session_id = req.session_id or str(uuid.uuid4())
    message = req.message.strip()

    _save_chat(session_id, "shopping_guide", "user", message)

    # 1. Extract preferences from message
    preferences = _extract_preferences(message)

    # 2. RAG for product recommendations
    rag_results = rag_engine.search(message, top_k=5)
    rag_context = rag_engine.get_context_for_llm(message, top_k=5)

    # 3. Build simulated recommendations (in production: from product DB)
    rec_items = _build_recommendations(message, preferences, rag_results)

    # 4. Load prompt
    system_prompt = _get_prompt("shopping_guide_system")
    fewshot = _get_prompt("shopping_guide_fewshot")

    full_system = system_prompt
    if rag_context:
        full_system += f"\n\n## 知识库参考\n{rag_context}"
    if fewshot:
        full_system += f"\n\n## 对话示例\n{fewshot}"

    messages = [{"role": "user", "content": message}]

    async def event_stream():
        yield f"event: recommendations\ndata: {json.dumps({'items': rec_items}, ensure_ascii=False)}\n\n"

        pipeline_data = {"preferences": preferences}
        yield f"event: pipeline\ndata: {json.dumps(pipeline_data, ensure_ascii=False)}\n\n"

        full_response = ""
        async for chunk in chat_stream(messages, system_prompt=full_system):
            yield chunk
            if '"text"' in chunk:
                try:
                    d = json.loads(chunk[chunk.index('{'):])
                    full_response += d.get('text', '')
                except Exception:
                    pass

        if full_response:
            _save_chat(session_id, "shopping_guide", "assistant", full_response)

        yield f"event: done\ndata: {json.dumps({'session_id': session_id})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")

# ═══════════════════════════════════════════════════════════
#  User Profiles API (for Shopping Guide demo)
# ═══════════════════════════════════════════════════════════
@app.get("/api/shopping-guide/profiles")
def get_profiles():
    return {
        "profiles": [
            {"id": "p1", "name": "张三", "rfm_segment": "高价值·活跃用户",
             "preferences": "增肌,力量训练,高蛋白", "budget": "中高", "level": "中级"},
            {"id": "p2", "name": "李四", "rfm_segment": "新用户·潜力",
             "preferences": "减脂,瑜伽,低卡", "budget": "低", "level": "新手"},
            {"id": "p3", "name": "王五", "rfm_segment": "流失预警",
             "preferences": "CrossFit,功能性训练", "budget": "高", "level": "高级"},
        ]
    }

# ═══════════════════════════════════════════════════════════
#  Admin API — Knowledge Base
# ═══════════════════════════════════════════════════════════
@app.get("/api/admin/knowledge")
def list_knowledge(category_id: int = None, search: str = "", page: int = 1, limit: int = 50):
    conn = get_db()
    where = []
    params = []
    if category_id:
        where.append("ke.category_id = ?")
        params.append(category_id)
    if search:
        where.append("(ke.question LIKE ? OR ke.answer LIKE ? OR ke.keywords LIKE ?)")
        params.extend([f"%{search}%"] * 3)
    where_clause = "WHERE " + " AND ".join(where) if where else ""
    offset = (page - 1) * limit
    rows = conn.execute(
        f"""SELECT ke.*, c.name as category_name FROM knowledge_entries ke
            LEFT JOIN categories c ON ke.category_id = c.id
            {where_clause} ORDER BY ke.updated_at DESC LIMIT ? OFFSET ?""",
        params + [limit, offset]
    ).fetchall()
    total = conn.execute(
        f"SELECT COUNT(*) as cnt FROM knowledge_entries ke {where_clause}", params
    ).fetchone()['cnt']
    conn.close()
    return {"entries": [dict(r) for r in rows], "total": total, "page": page, "limit": limit}

@app.post("/api/admin/knowledge")
def create_knowledge(data: dict):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO knowledge_entries (category_id, question, answer, keywords) VALUES (?,?,?,?)",
        (data.get('category_id'), data['question'], data['answer'], data.get('keywords', ''))
    )
    conn.commit()
    entry_id = cur.lastrowid
    conn.close()
    rag_engine.rebuild_index()
    return {"id": entry_id, "message": "知识条目已创建"}

@app.put("/api/admin/knowledge/{entry_id}")
def update_knowledge(entry_id: int, data: dict):
    conn = get_db()
    conn.execute(
        """UPDATE knowledge_entries SET category_id=?, question=?, answer=?, keywords=?, updated_at=CURRENT_TIMESTAMP
           WHERE id=?""",
        (data.get('category_id'), data['question'], data['answer'], data.get('keywords', ''), entry_id)
    )
    conn.commit()
    conn.close()
    rag_engine.rebuild_index()
    return {"message": "知识条目已更新"}

@app.delete("/api/admin/knowledge/{entry_id}")
def delete_knowledge(entry_id: int):
    conn = get_db()
    conn.execute("DELETE FROM knowledge_entries WHERE id=?", (entry_id,))
    conn.commit()
    conn.close()
    rag_engine.rebuild_index()
    return {"message": "知识条目已删除"}

@app.post("/api/admin/knowledge/import")
async def import_knowledge(file: UploadFile = File(...)):
    content = await file.read()
    try:
        data = json.loads(content)
        conn = get_db()
        count = 0
        for item in data:
            if 'question' in item and 'answer' in item:
                conn.execute(
                    "INSERT INTO knowledge_entries (category_id, question, answer, keywords) VALUES (?,?,?,?)",
                    (item.get('category_id'), item['question'], item['answer'], item.get('keywords', ''))
                )
                count += 1
        conn.commit()
        conn.close()
        rag_engine.rebuild_index()
        return {"message": f"成功导入 {count} 条记录", "count": count}
    except json.JSONDecodeError:
        raise HTTPException(400, "JSON格式错误")

@app.get("/api/admin/knowledge/export")
def export_knowledge():
    conn = get_db()
    rows = conn.execute(
        "SELECT id, category_id, question, answer, keywords FROM knowledge_entries ORDER BY id"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

# ═══════════════════════════════════════════════════════════
#  Admin API — Categories
# ═══════════════════════════════════════════════════════════
@app.get("/api/admin/categories")
def list_categories():
    conn = get_db()
    rows = conn.execute("SELECT c.*, (SELECT COUNT(*) FROM knowledge_entries WHERE category_id=c.id) as entry_count FROM categories c ORDER BY c.id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/admin/categories")
def create_category(data: dict):
    conn = get_db()
    cur = conn.execute("INSERT INTO categories (name, description) VALUES (?,?)", (data['name'], data.get('description', '')))
    conn.commit()
    cat_id = cur.lastrowid
    conn.close()
    return {"id": cat_id, "message": "分类已创建"}

@app.put("/api/admin/categories/{cat_id}")
def update_category(cat_id: int, data: dict):
    conn = get_db()
    conn.execute("UPDATE categories SET name=?, description=? WHERE id=?", (data['name'], data.get('description', ''), cat_id))
    conn.commit()
    conn.close()
    return {"message": "分类已更新"}

@app.delete("/api/admin/categories/{cat_id}")
def delete_category(cat_id: int):
    conn = get_db()
    conn.execute("UPDATE knowledge_entries SET category_id=NULL WHERE category_id=?", (cat_id,))
    conn.execute("DELETE FROM categories WHERE id=?", (cat_id,))
    conn.commit()
    conn.close()
    return {"message": "分类已删除"}

# ═══════════════════════════════════════════════════════════
#  Admin API — Prompts
# ═══════════════════════════════════════════════════════════
@app.get("/api/admin/prompts")
def list_prompts():
    conn = get_db()
    rows = conn.execute("SELECT name, description, updated_at FROM prompts ORDER BY name").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/admin/prompts/{name}")
def get_prompt_detail(name: str):
    conn = get_db()
    row = conn.execute("SELECT * FROM prompts WHERE name=?", (name,)).fetchone()
    conn.close()
    if not row:
        raise HTTPException(404, "Prompt模板不存在")
    return dict(row)

@app.put("/api/admin/prompts/{name}")
def update_prompt(name: str, data: dict):
    conn = get_db()
    conn.execute(
        "INSERT INTO prompts (name, content, description, updated_at) VALUES (?,?,?,CURRENT_TIMESTAMP) ON CONFLICT(name) DO UPDATE SET content=?, description=?, updated_at=CURRENT_TIMESTAMP",
        (name, data['content'], data.get('description', ''), data['content'], data.get('description', ''))
    )
    conn.commit()
    conn.close()
    return {"message": "Prompt模板已更新"}

# ═══════════════════════════════════════════════════════════
#  Admin API — Settings
# ═══════════════════════════════════════════════════════════
@app.get("/api/admin/settings")
def get_settings():
    conn = get_db()
    rows = conn.execute("SELECT key, value FROM settings").fetchall()
    conn.close()
    return {r['key']: r['value'] for r in rows}

@app.put("/api/admin/settings")
def update_settings(data: dict):
    conn = get_db()
    for key, value in data.items():
        conn.execute(
            "INSERT INTO settings (key, value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=?",
            (key, str(value), str(value))
        )
    conn.commit()
    conn.close()
    return {"message": "设置已更新"}

# ═══════════════════════════════════════════════════════════
#  Admin API — Stats
# ═══════════════════════════════════════════════════════════
@app.get("/api/admin/stats")
def get_stats():
    conn = get_db()
    kb_count = conn.execute("SELECT COUNT(*) as cnt FROM knowledge_entries").fetchone()['cnt']
    cat_count = conn.execute("SELECT COUNT(*) as cnt FROM categories").fetchone()['cnt']
    chat_count = conn.execute("SELECT COUNT(*) as cnt FROM chat_history").fetchone()['cnt']
    recent_chats = conn.execute(
        "SELECT * FROM chat_history ORDER BY created_at DESC LIMIT 20"
    ).fetchall()
    config = get_deepseek_config()
    conn.close()
    return {
        "knowledge_count": kb_count,
        "category_count": cat_count,
        "chat_count": chat_count,
        "model": config['model'],
        "has_api_key": bool(config['api_key']),
        "recent_chats": [dict(r) for r in recent_chats],
    }

# ═══════════════════════════════════════════════════════════
#  Admin API — Chat History
# ═══════════════════════════════════════════════════════════
@app.get("/api/admin/chat-history")
def chat_history(project: str = "", page: int = 1, limit: int = 50):
    conn = get_db()
    where = "WHERE project = ?" if project else ""
    params = [project] if project else []
    offset = (page - 1) * limit
    rows = conn.execute(
        f"SELECT * FROM chat_history {where} ORDER BY created_at DESC LIMIT ? OFFSET ?",
        params + [limit, offset]
    ).fetchall()
    total = conn.execute(f"SELECT COUNT(*) as cnt FROM chat_history {where}", params).fetchone()['cnt']
    conn.close()
    return {"chats": [dict(r) for r in rows], "total": total, "page": page}

@app.put("/api/admin/chat-history/{chat_id}/feedback")
def update_chat_feedback(chat_id: int, data: dict):
    conn = get_db()
    conn.execute("UPDATE chat_history SET feedback=? WHERE id=?", (data.get('feedback'), chat_id))
    conn.commit()
    conn.close()
    return {"message": "反馈已记录"}

# ═══════════════════════════════════════════════════════════
#  Admin API — Products (Shopping Guide)
# ═══════════════════════════════════════════════════════════
@app.get("/api/admin/products")
def list_products(category: str = "", search: str = ""):
    conn = get_db()
    where = []
    params = []
    if category:
        where.append("category = ?")
        params.append(category)
    if search:
        where.append("(name LIKE ? OR tags LIKE ? OR reason LIKE ?)")
        params.extend([f"%{search}%"] * 3)
    where_clause = "WHERE " + " AND ".join(where) if where else ""
    rows = conn.execute(f"SELECT * FROM products {where_clause} ORDER BY id", params).fetchall()
    conn.close()
    return {"products": [dict(r) for r in rows]}

@app.get("/api/admin/products/categories")
def list_product_categories():
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT category FROM products WHERE category != '' ORDER BY category").fetchall()
    conn.close()
    return [r['category'] for r in rows]

@app.post("/api/admin/products")
def create_product(data: dict):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO products (name,emoji,price,original_price,tags,match_score,reason,category) VALUES (?,?,?,?,?,?,?,?)",
        (data['name'], data.get('emoji', '📦'), data['price'], data.get('original_price', 0),
         data.get('tags', ''), data.get('match_score', 0.8), data.get('reason', ''), data.get('category', '综合'))
    )
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return {"id": pid, "message": "商品已创建"}

@app.put("/api/admin/products/{pid}")
def update_product(pid: int, data: dict):
    conn = get_db()
    conn.execute(
        """UPDATE products SET name=?,emoji=?,price=?,original_price=?,tags=?,match_score=?,reason=?,category=?,updated_at=CURRENT_TIMESTAMP
           WHERE id=?""",
        (data['name'], data.get('emoji', '📦'), data['price'], data.get('original_price', 0),
         data.get('tags', ''), data.get('match_score', 0.8), data.get('reason', ''), data.get('category', '综合'), pid)
    )
    conn.commit()
    conn.close()
    return {"message": "商品已更新"}

@app.delete("/api/admin/products/{pid}")
def delete_product(pid: int):
    conn = get_db()
    conn.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return {"message": "商品已删除"}

# ═══════════════════════════════════════════════════════════
#  Admin API — Intent Rules
# ═══════════════════════════════════════════════════════════
@app.get("/api/admin/intent-rules")
def list_intent_rules(project: str = ""):
    conn = get_db()
    if project:
        rows = conn.execute("SELECT * FROM intent_rules WHERE project=? ORDER BY priority DESC, id", (project,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM intent_rules ORDER BY project, priority DESC, id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/admin/intent-rules")
def create_intent_rule(data: dict):
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO intent_rules (project,intent_name,sub_intent,keywords,entities,priority) VALUES (?,?,?,?,?,?)",
        (data['project'], data['intent_name'], data.get('sub_intent', ''),
         data['keywords'], data.get('entities', ''), data.get('priority', 0))
    )
    conn.commit()
    rid = cur.lastrowid
    conn.close()
    return {"id": rid, "message": "意图规则已创建"}

@app.put("/api/admin/intent-rules/{rid}")
def update_intent_rule(rid: int, data: dict):
    conn = get_db()
    conn.execute(
        "UPDATE intent_rules SET project=?,intent_name=?,sub_intent=?,keywords=?,entities=?,priority=? WHERE id=?",
        (data['project'], data['intent_name'], data.get('sub_intent', ''),
         data['keywords'], data.get('entities', ''), data.get('priority', 0), rid)
    )
    conn.commit()
    conn.close()
    return {"message": "意图规则已更新"}

@app.delete("/api/admin/intent-rules/{rid}")
def delete_intent_rule(rid: int):
    conn = get_db()
    conn.execute("DELETE FROM intent_rules WHERE id=?", (rid,))
    conn.commit()
    conn.close()
    return {"message": "意图规则已删除"}

# ═══════════════════════════════════════════════════════════
#  Admin API — User Profiles
# ═══════════════════════════════════════════════════════════
@app.get("/api/admin/profiles")
def list_profiles():
    conn = get_db()
    rows = conn.execute("SELECT * FROM user_profiles ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/api/admin/profiles")
def create_profile(data: dict):
    conn = get_db()
    conn.execute(
        "INSERT INTO user_profiles (id,name,rfm_segment,preferences,budget,level) VALUES (?,?,?,?,?,?)",
        (data['id'], data['name'], data.get('rfm_segment', ''), data.get('preferences', ''),
         data.get('budget', ''), data.get('level', ''))
    )
    conn.commit()
    conn.close()
    return {"id": data['id'], "message": "用户画像已创建"}

@app.put("/api/admin/profiles/{pid}")
def update_profile(pid: str, data: dict):
    conn = get_db()
    conn.execute(
        "UPDATE user_profiles SET name=?,rfm_segment=?,preferences=?,budget=?,level=? WHERE id=?",
        (data['name'], data.get('rfm_segment', ''), data.get('preferences', ''),
         data.get('budget', ''), data.get('level', ''), pid)
    )
    conn.commit()
    conn.close()
    return {"message": "用户画像已更新"}

@app.delete("/api/admin/profiles/{pid}")
def delete_profile(pid: str):
    conn = get_db()
    conn.execute("DELETE FROM user_profiles WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    return {"message": "用户画像已删除"}

# ═══════════════════════════════════════════════════════════
#  Admin API — Delete chat history item
# ═══════════════════════════════════════════════════════════
@app.delete("/api/admin/chat-history/{chat_id}")
def delete_chat(chat_id: int):
    conn = get_db()
    conn.execute("DELETE FROM chat_history WHERE id=?", (chat_id,))
    conn.commit()
    conn.close()
    return {"message": "对话记录已删除"}

@app.delete("/api/admin/chat-history")
def clear_chat_history(project: str = ""):
    conn = get_db()
    if project:
        conn.execute("DELETE FROM chat_history WHERE project=?", (project,))
    else:
        conn.execute("DELETE FROM chat_history")
    conn.commit()
    conn.close()
    return {"message": "对话记录已清空"}

# ═══════════════════════════════════════════════════════════
#  Admin Panel Static
# ═══════════════════════════════════════════════════════════
@app.get("/admin")
def admin_panel():
    return FileResponse(BASE_DIR / "admin" / "index.html")

# ═══════════════════════════════════════════════════════════
#  Helpers
# ═══════════════════════════════════════════════════════════
def _save_chat(session_id: str, project: str, role: str, message: str, intent: str = None, confidence: float = None):
    try:
        conn = get_db()
        conn.execute(
            "INSERT INTO chat_history (session_id, project, role, message, intent, confidence) VALUES (?,?,?,?,?,?)",
            (session_id, project, role, message[:2000], intent, confidence)
        )
        conn.commit()
        conn.close()
    except Exception:
        pass

def _get_prompt(name: str) -> str:
    conn = get_db()
    row = conn.execute("SELECT content FROM prompts WHERE name=?", (name,)).fetchone()
    conn.close()
    return row['content'] if row else ""

def _detect_intent(text: str, project: str = 'customer_service'):
    """Use intent rules from database for dynamic intent detection."""
    conn = get_db()
    rules = conn.execute(
        "SELECT * FROM intent_rules WHERE project=? ORDER BY priority DESC",
        (project,)
    ).fetchall()
    conn.close()
    text_lower = text.lower()
    for rule in rules:
        keywords = rule['keywords'].split(',')
        if any(kw.strip() in text_lower for kw in keywords):
            entities = [e.strip() for e in rule['entities'].split(',') if e.strip()]
            return rule['intent_name'], rule['sub_intent'], entities
    return '通用咨询', '', []

def _detect_sentiment(text: str):
    urgent_words = ['急', '立刻', '马上', '投诉', '举报', '严重']
    neg_words = ['差', '烂', '坑', '骗', '垃圾', '失望', '生气', '无语', '慢']
    if any(w in text for w in urgent_words):
        return 'urgent'
    if any(w in text for w in neg_words):
        return 'negative'
    if '?' in text or '？' in text or '怎么' in text or '什么' in text:
        return 'neutral'
    return 'neutral'

def _extract_preferences(text: str):
    prefs = {'category': '综合', 'goal': '未指定', 'budget': '未指定', 'level': '未指定'}
    if any(w in text for w in ['增肌', '力量', '蛋白', '肌肉', '壮']):
        prefs['goal'] = '增肌'
        prefs['category'] = '营养补剂'
    elif any(w in text for w in ['减肥', '减脂', '瘦', '减重', '燃脂']):
        prefs['goal'] = '减脂'
        prefs['category'] = '有氧器材'
    elif any(w in text for w in ['瑜伽', '柔韧', '拉伸']):
        prefs['goal'] = '柔韧性'
        prefs['category'] = '瑜伽装备'
    if any(w in text for w in ['便宜', '低价', '入门', '基础', '新手', '初次', '刚']):
        prefs['budget'] = '低'
        prefs['level'] = '新手'
    elif any(w in text for w in ['贵', '高端', '专业', '高级']):
        prefs['budget'] = '高'
        prefs['level'] = '高级'
    elif any(w in text for w in ['中级', '进阶']):
        prefs['budget'] = '中'
        prefs['level'] = '中级'
    return prefs

def _build_recommendations(message: str, prefs: dict, rag_results: list):
    """Load products from database and rank by relevance."""
    conn = get_db()
    rows = conn.execute("SELECT * FROM products ORDER BY id").fetchall()
    conn.close()
    catalog = []
    for r in rows:
        tags = [t.strip() for t in r['tags'].split(',') if t.strip()]
        catalog.append({"name": r['name'], "emoji": r['emoji'], "price": r['price'], "original_price": r['original_price'], "tags": tags, "match_score": r['match_score'], "reason": r['reason']})
    if not catalog:
        catalog = [
        {"name": "乳清蛋白粉-基础款", "emoji": "🥛", "price": 299, "original_price": 399, "tags": ["高蛋白", "易吸收", "新手友好"], "match_score": 0.92, "reason": "75%蛋白质含量，适合训练后快速补充"},
        {"name": "智能跳绳-燃脂版", "emoji": "⭕", "price": 89, "original_price": 129, "tags": ["便携", "计数", "高效燃脂"], "match_score": 0.88, "reason": "每天15分钟高效燃脂，APP记录数据"},
        {"name": "专业瑜伽垫-加厚款", "emoji": "🧘", "price": 59, "original_price": 79, "tags": ["防滑", "加厚", "环保"], "match_score": 0.85, "reason": "6mm厚度保护关节，适合初学者"},
        {"name": "运动手环Pro", "emoji": "⌚", "price": 199, "original_price": 259, "tags": ["心率监测", "运动追踪", "防水"], "match_score": 0.82, "reason": "实时监控运动数据，科学指导训练"},
        {"name": "增肌蛋白粉-进阶版", "emoji": "💪", "price": 449, "original_price": 549, "tags": ["高纯度", "增肌配方", "BCAA"], "match_score": 0.78, "reason": "80%蛋白质+5g BCAA，适合增肌期"},
        {"name": "BodyPump杠铃课程", "emoji": "🏋️", "price": 199, "original_price": 299, "tags": ["力量训练", "全身塑形", "团课"], "match_score": 0.76, "reason": "60分钟全身力量训练，适合塑形"},
    ]
    if '减肥' in message or '减脂' in message:
        catalog.sort(key=lambda x: x['name'] == '智能跳绳-燃脂版', reverse=True)
    elif '增肌' in message or '蛋白' in message:
        catalog.sort(key=lambda x: '蛋白' in x['name'], reverse=True)
    elif '瑜伽' in message:
        catalog.sort(key=lambda x: '瑜伽' in x['name'], reverse=True)
    return catalog[:3]

# ═══════════════════════════════════════════════════════════
#  Main
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 80))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
