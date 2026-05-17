import httpx
import json
from database import get_db

DEEPSEEK_BASE = "https://api.deepseek.com"

def get_deepseek_config():
    conn = get_db()
    api_key = conn.execute("SELECT value FROM settings WHERE key='deepseek_api_key'").fetchone()
    model = conn.execute("SELECT value FROM settings WHERE key='deepseek_model'").fetchone()
    conn.close()
    return {
        'api_key': (api_key['value'] if api_key else ''),
        'model': (model['value'] if model else 'deepseek-chat'),
    }

async def chat_stream(messages: list, system_prompt: str = "", temperature: float = 0.7):
    config = get_deepseek_config()
    if not config['api_key']:
        yield "data: " + json.dumps({"error": "请先在管理后台配置DeepSeek API Key"}, ensure_ascii=False) + "\n\n"
        yield "event: done\ndata: " + json.dumps({"session_id": ""}) + "\n\n"
        return

    full_messages = []
    if system_prompt:
        full_messages.append({"role": "system", "content": system_prompt})
    full_messages.extend(messages)

    async with httpx.AsyncClient(timeout=60.0) as client:
        async with client.stream(
            "POST",
            f"{DEEPSEEK_BASE}/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {config['api_key']}",
                "Content-Type": "application/json",
            },
            json={
                "model": config['model'],
                "messages": full_messages,
                "temperature": temperature,
                "max_tokens": 2048,
                "stream": True,
            },
        ) as resp:
            if resp.status_code != 200:
                body = await resp.aread()
                yield "data: " + json.dumps({"error": f"API错误 {resp.status_code}: {body.decode()[:200]}"}, ensure_ascii=False) + "\n\n"
                yield "event: done\ndata: " + json.dumps({"session_id": ""}) + "\n\n"
                return

            async for line in resp.aiter_lines():
                if line.startswith("data: "):
                    chunk = line[6:]
                    if chunk == "[DONE]":
                        return
                    try:
                        data = json.loads(chunk)
                        delta = data.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            yield f"event: token\ndata: {json.dumps({'text': content})}\n\n"
                    except json.JSONDecodeError:
                        continue
