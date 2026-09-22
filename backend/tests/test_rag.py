from backend.app.rag.knowledge_base import KNOWLEDGE_BASE
from backend.app.rag.rag_engine import (
    tokenize,
    chunk_document,
    retrieve,
    format_context,
    citations_of,
    knowledge_base_stats,
)


def test_tokenize_removes_stopwords():
    tokens = tokenize("The quick brown fox jumps over the lazy dog")
    assert "the" not in tokens
    assert "quick" in tokens
    assert "brown" in tokens


def test_chunking_creates_valid_chunks():
    doc = KNOWLEDGE_BASE[0]
    chunks = chunk_document(doc)
    assert len(chunks) >= 1
    assert chunks[0]["docId"] == doc["id"]
    assert doc["title"] in chunks[0]["text"]


def test_retrieval_sql_injection():
    results = retrieve("SQL injection string concatenation vulnerability", k=5)
    assert len(results) > 0
    top_title = results[0]["chunk"]["title"].lower()
    assert "injection" in top_title or "sql" in top_title


def test_retrieval_embedded_secrets():
    results = retrieve("API key embedded directly in source code", k=5)
    assert len(results) > 0
    titles = " ".join(r["chunk"]["title"].lower() for r in results)
    assert "secret" in titles or "credential" in titles or "cryptographic" in titles


def test_knowledge_base_stats():
    stats = knowledge_base_stats()
    assert stats["documents"] == len(KNOWLEDGE_BASE)
    assert stats["chunks"] >= len(KNOWLEDGE_BASE)
    assert stats["dimensions"] >= 500
