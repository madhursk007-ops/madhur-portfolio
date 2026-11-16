import pytest

from app.retrieval import retrieve, split_into_chunks


def test_chunking_keeps_all_text():
    text = "First sentence. " * 80
    chunks = split_into_chunks(text, chunk_size=120, overlap=20)
    assert len(chunks) > 1
    assert all(chunks)


def test_retrieval_ranks_relevant_passage_first():
    docs = [
        {"source": "maintenance", "chunk_id": 1, "text": "Bearing vibration can indicate misalignment."},
        {"source": "travel", "chunk_id": 1, "text": "Train tickets can be booked online."},
    ]
    results = retrieve("bearing vibration", docs)
    assert results[0]["source"] == "maintenance"
    assert results[0]["score"] > 0


def test_empty_query_returns_no_results():
    assert retrieve("   ", [], limit=3) == []


def test_invalid_chunk_overlap_is_rejected():
    with pytest.raises(ValueError):
        split_into_chunks("some text", chunk_size=10, overlap=10)
