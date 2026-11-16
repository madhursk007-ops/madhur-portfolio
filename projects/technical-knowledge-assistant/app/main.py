"""Document-grounded Q&A API with optional hosted LLM generation."""
import os
import sqlite3
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .retrieval import retrieve, split_into_chunks

DB_PATH = Path(os.getenv("KNOWLEDGE_DB", "knowledge.db"))
app = FastAPI(
    title="Technical Knowledge Assistant",
    description="Retrieve relevant document passages and answer with source references.",
    version="0.1.0",
)


def connect():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            chunk_id INTEGER NOT NULL,
            text TEXT NOT NULL
        )
    """)
    return connection


class DocumentInput(BaseModel):
    title: str = Field(min_length=1, max_length=160)
    text: str = Field(min_length=40, max_length=50000)


class QuestionInput(BaseModel):
    question: str = Field(min_length=3, max_length=1000)
    limit: int = Field(default=4, ge=1, le=8)


@app.get("/health")
def health():
    return {"status": "ok", "service": "technical-knowledge-assistant"}


@app.post("/documents")
def add_document(payload: DocumentInput):
    chunks = split_into_chunks(payload.text)
    with connect() as db:
        for index, chunk in enumerate(chunks):
            db.execute(
                "INSERT INTO chunks (id, source, chunk_id, text) VALUES (?, ?, ?, ?)",
                (str(uuid4()), payload.title.strip(), index + 1, chunk),
            )
    return {"source": payload.title.strip(), "chunks_added": len(chunks)}


@app.get("/documents")
def list_documents():
    with connect() as db:
        rows = db.execute(
            "SELECT source, COUNT(*) AS chunks FROM chunks GROUP BY source ORDER BY source"
        ).fetchall()
    return {"documents": [dict(row) for row in rows]}


def generate_answer(question: str, passages: list[dict]) -> tuple[str, str]:
    if not passages:
        return "I couldn't find a relevant passage in the documents provided.", "no_context"

    context = "\n\n".join(
        f"[{i}] Source: {p['source']} (chunk {p['chunk_id']})\n{p['text']}"
        for i, p in enumerate(passages, start=1)
    )
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            response = client.responses.create(
                model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"),
                input=[
                    {
                        "role": "system",
                        "content": (
                            "Answer only from the supplied excerpts. If the excerpts "
                            "do not support an answer, say so. Cite supporting excerpts "
                            "using [1], [2], etc. Do not invent facts."
                        ),
                    },
                    {
                        "role": "user",
                        "content": f"Question: {question}\n\nExcerpts:\n{context}",
                    },
                ],
            )
            return response.output_text, "retrieval_plus_generation"
        except Exception as exc:
            # A configured but unavailable provider must not silently masquerade
            # as successful generation.
            return (
                "The relevant passages were retrieved, but answer generation failed. "
                f"Check the model configuration. Retrieved context: {context}",
                "retrieval_only_generation_error",
            )

    excerpts = " ".join(p["text"] for p in passages[:2])
    return (
        "No OPENAI_API_KEY is configured, so this is a retrieval-only preview, "
        "not a generated answer. Relevant passages: " + excerpts,
        "retrieval_only",
    )


@app.post("/ask")
def ask(payload: QuestionInput):
    with connect() as db:
        rows = db.execute(
            "SELECT source, chunk_id, text FROM chunks"
        ).fetchall()
    documents = [dict(row) for row in rows]
    passages = retrieve(payload.question, documents, payload.limit)
    answer, mode = generate_answer(payload.question, passages)
    return {
        "question": payload.question,
        "answer": answer,
        "mode": mode,
        "sources": [
            {
                "title": p["source"],
                "chunk": p["chunk_id"],
                "relevance_score": p["score"],
                "excerpt": p["text"][:240],
            }
            for p in passages
        ],
    }


@app.get("/")
def home():
    return {
        "message": "Technical Knowledge Assistant API",
        "docs": "/docs",
        "workflow": ["POST /documents", "POST /ask"],
    }
