"""Small, dependency-light retrieval layer for a document Q&A demo."""
import re
from collections import Counter


def split_into_chunks(text: str, chunk_size: int = 700, overlap: int = 100) -> list[str]:
    text = " ".join(text.split())
    if not text:
        return []
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        # Prefer a sentence boundary when it is reasonably close.
        boundary = text.rfind(". ", start, end)
        if boundary > start + chunk_size // 2 and end < len(text):
            end = boundary + 1
        chunks.append(text[start:end].strip())
        if end >= len(text):
            break
        start = max(end - overlap, start + 1)
    return chunks


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())


def retrieve(query: str, documents: list[dict], limit: int = 4) -> list[dict]:
    """Rank chunks using transparent TF-style lexical overlap.

    This baseline is intentionally simple and inspectable. It can later be
    compared with vector or hybrid retrieval on a labelled evaluation set.
    """
    query_terms = Counter(_tokens(query))
    if not query_terms:
        return []
    ranked = []
    for doc in documents:
        terms = Counter(_tokens(doc["text"]))
        overlap = sum(min(count, terms[term]) for term, count in query_terms.items())
        if overlap:
            ranked.append({**doc, "score": round(overlap / sum(query_terms.values()), 4)})
    ranked.sort(key=lambda item: (-item["score"], item["source"], item["chunk_id"]))
    return ranked[:limit]
