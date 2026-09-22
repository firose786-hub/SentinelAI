import re
from typing import List, Dict, Any, Tuple, Set
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .knowledge_base import KNOWLEDGE_BASE

CHUNK_TARGET_CHARS = 520
CHUNK_OVERLAP_SENTENCES = 1

STOPWORDS: Set[str] = set(
    "a an and are as at be by for from has have in is it its of on or that the to with which when this these those not no do does can may".split()
)


def tokenize(text: str) -> List[str]:
    cleaned = re.sub(r"[^a-z0-9_+#.-]+", " ", text.lower())
    tokens = cleaned.split()
    return [t for t in tokens if len(t) > 1 and t not in STOPWORDS]


def chunk_document(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    body = re.sub(r"\n+", " ", doc["body"])
    sentences = [s.strip() for s in re.split(r"(?<=[.;])\s+", body) if s.strip()]

    chunks = []
    buffer: List[str] = []
    length = 0

    def flush():
        nonlocal buffer, length
        if not buffer:
            return
        chunk_text = f"{doc['title']}. {' '.join(buffer)}"
        chunks.append({
            "id": f"{doc['id']}#{len(chunks)}",
            "docId": doc["id"],
            "title": doc["title"],
            "source": doc["source"],
            "tags": doc["tags"],
            "text": chunk_text,
        })
        buffer = buffer[-CHUNK_OVERLAP_SENTENCES:]
        length = sum(len(s) for s in buffer)

    for sentence in sentences:
        buffer.append(sentence)
        length += len(sentence)
        if length >= CHUNK_TARGET_CHARS:
            flush()

    if buffer:
        chunk_text = f"{doc['title']}. {' '.join(buffer)}"
        chunks.append({
            "id": f"{doc['id']}#{len(chunks)}",
            "docId": doc["id"],
            "title": doc["title"],
            "source": doc["source"],
            "tags": doc["tags"],
            "text": chunk_text,
        })

    return chunks


class VectorStore:
    def __init__(self):
        self.chunks: List[Dict[str, Any]] = []
        self.vectorizer: TfidfVectorizer = None
        self.matrix = None
        self._build_index()

    def _build_index(self):
        self.chunks = []
        corpus = []

        for doc in KNOWLEDGE_BASE:
            doc_chunks = chunk_document(doc)
            for c in doc_chunks:
                full_text = f"{c['text']} {' '.join(doc['tags'])}"
                self.chunks.append(c)
                corpus.append(full_text)

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            sublinear_tf=True,
            ngram_range=(1, 2),
            token_pattern=r"(?u)\b\w[\w-]+\b",
        )
        self.matrix = self.vectorizer.fit_transform(corpus)


_store_instance: VectorStore = None


def get_vector_store() -> VectorStore:
    global _store_instance
    if _store_instance is None:
        _store_instance = VectorStore()
    return _store_instance


def retrieve(query: str, k: int = 5) -> List[Dict[str, Any]]:
    store = get_vector_store()
    if not store.chunks or store.matrix is None:
        return []

    query_vec = store.vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, store.matrix)[0]

    scored = []
    for idx, sim in enumerate(similarities):
        if sim > 0.01:
            scored.append({
                "chunk": store.chunks[idx],
                "score": float(sim),
            })

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:k]


def format_context(results: List[Dict[str, Any]]) -> str:
    blocks = []
    for i, r in enumerate(results, 1):
        c = r["chunk"]
        blocks.append(f"[{i}] {c['title']} ({c['source']})\n{c['text']}")
    return "\n\n".join(blocks)


def citations_of(results: List[Dict[str, Any]]) -> List[str]:
    citations = []
    seen = set()
    for r in results:
        c = r["chunk"]
        cite = f"{c['title']} — {c['source']}"
        if cite not in seen:
            seen.add(cite)
            citations.append(cite)
    return citations


def knowledge_base_stats() -> Dict[str, int]:
    store = get_vector_store()
    return {
        "documents": len(KNOWLEDGE_BASE),
        "chunks": len(store.chunks),
        "dimensions": store.matrix.shape[1] if store.matrix is not None else 0,
    }
