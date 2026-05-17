"""
Simple RAG engine using pure Python — no external ML dependencies.
Uses TF-IDF-like scoring with character n-grams for Chinese text retrieval.
"""
import re
import math
import os
import json
from collections import Counter
from database import get_db

CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.rag_cache')


class RAGEngine:
    def __init__(self):
        self.docs = []  # list of {id, text}
        self._load_or_rebuild()

    def _load_or_rebuild(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        cache_file = os.path.join(CACHE_DIR, 'rag_index.json')
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    self.docs = json.load(f)
                return
            except Exception:
                pass
        self.rebuild_index()

    def rebuild_index(self):
        conn = get_db()
        rows = conn.execute(
            "SELECT id, question, answer, keywords FROM knowledge_entries"
        ).fetchall()
        conn.close()
        self.docs = []
        for r in rows:
            text = f"{r['question']} {r['keywords']} {r['answer'][:200]}"
            self.docs.append({'id': r['id'], 'text': text})
        cache_file = os.path.join(CACHE_DIR, 'rag_index.json')
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(self.docs, f, ensure_ascii=False)

    def _tokenize(self, text: str):
        """Split Chinese text into character bigrams + individual chars."""
        text = text.lower().strip()
        # Character bigrams
        bigrams = [text[i:i+2] for i in range(len(text)-1)]
        # Also single chars for short queries
        chars = list(text)
        return bigrams + chars

    def _score(self, query: str, doc_text: str) -> float:
        """Compute TF-IDF-like similarity score between query and document."""
        q_tokens = self._tokenize(query)
        d_tokens = self._tokenize(doc_text)
        if not q_tokens or not d_tokens:
            return 0.0

        q_counter = Counter(q_tokens)
        d_counter = Counter(d_tokens)

        # IDF approximation: rarity boost for longer tokens
        score = 0.0
        for token, q_count in q_counter.items():
            if token in d_counter:
                tf = d_counter[token] / len(d_tokens)
                # Boost: longer n-grams get higher weight
                weight = len(token)
                score += q_count * tf * weight * 10

        # Length normalization
        score = score / (1 + math.log(len(d_tokens) + 1))
        return score

    def search(self, query: str, top_k: int = 5):
        if not self.docs:
            return []

        scored = []
        for doc in self.docs:
            s = self._score(query, doc['text'])
            if s > 0.001:
                scored.append((doc['id'], s))

        scored.sort(key=lambda x: x[1], reverse=True)
        top = scored[:top_k]

        results = []
        conn = get_db()
        for doc_id, score in top:
            row = conn.execute(
                """SELECT ke.id, ke.question, ke.answer, ke.keywords, c.name as category
                   FROM knowledge_entries ke
                   LEFT JOIN categories c ON ke.category_id = c.id
                   WHERE ke.id = ?""",
                (doc_id,)
            ).fetchone()
            if row:
                # Normalize score to 0-1 range
                norm_score = min(1.0, round(score / (1 + score), 3))
                results.append({
                    'id': row['id'],
                    'question': row['question'],
                    'answer': row['answer'],
                    'keywords': row['keywords'],
                    'category': row['category'] or '未分类',
                    'score': norm_score,
                })
        conn.close()
        return results

    def get_context_for_llm(self, query: str, top_k: int = 5) -> str:
        results = self.search(query, top_k)
        if not results:
            return ""
        parts = []
        for i, r in enumerate(results, 1):
            parts.append(f"[参考{i}] 分类:{r['category']} | 问题:{r['question']}\n回答:{r['answer']}")
        return "\n\n".join(parts)


rag_engine = RAGEngine()
