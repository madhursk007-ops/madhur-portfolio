"""Document-grounded Q&A API and web interface."""
import os
import sqlite3
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .retrieval import retrieve, split_into_chunks

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
DB_PATH = Path(os.getenv("KNOWLEDGE_DB", "knowledge.db"))
MAX_UPLOAD_BYTES = 200_000

app = FastAPI(
    title="Technical Knowledge Assistant",
    description="Upload technical notes, retrieve relevant passages, and answer with source references.",
    version="0.2.0",
)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
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


def store_document(title: str, text: str) -> int:
    clean_title = Path(title.strip()).name[:160]
    if not clean_title:
        raise HTTPException(status_code=422, detail="A document title is required.")
    chunks = split_into_chunks(text)
    if not chunks:
        raise HTTPException(status_code=422, detail="The document does not contain readable text.")
    with connect() as db:
        # Re-uploading the same title replaces its previous indexed content.
        db.execute("DELETE FROM chunks WHERE source = ?", (clean_title,))
        for index, chunk in enumerate(chunks):
            db.execute(
                "INSERT INTO chunks (id, source, chunk_id, text) VALUES (?, ?, ?, ?)",
                (str(uuid4()), clean_title, index + 1, chunk),
            )
    return len(chunks)


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "service": "technical-knowledge-assistant"}


@app.post("/documents")
def add_document(payload: DocumentInput):
    chunks_added = store_document(payload.title, payload.text)
    return {"source": Path(payload.title.strip()).name, "chunks_added": chunks_added}


@app.post("/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    filename = Path(file.filename or "").name
    if Path(filename).suffix.lower() not in {".txt", ".md"}:
        raise HTTPException(status_code=415, detail="Upload a .txt or .md file.")
    content = await file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File is too large. Maximum size is 200 KB.")
    try:
        text = content.decode("utf-8-sig").strip()
    except UnicodeDecodeError:
        raise HTTPException(status_code=422, detail="The file must be UTF-8 encoded.")
    if len(text) < 40:
        raise HTTPException(status_code=422, detail="Add at least 40 characters of readable text.")
    chunks_added = store_document(filename, text)
    return {"source": filename, "chunks_added": chunks_added}


@app.get("/documents")
def list_documents():
    with connect() as db:
        rows = db.execute(
            "SELECT source, COUNT(*) AS chunks FROM chunks GROUP BY source ORDER BY source"
        ).fetchall()
    return {"documents": [dict(row) for row in rows]}


@app.delete("/documents/{source}")
def delete_document(source: str):
    with connect() as db:
        cursor = db.execute("DELETE FROM chunks WHERE source = ?", (source,))
        deleted = cursor.rowcount
    if not deleted:
        raise HTTPException(status_code=404, detail="Document not found.")
    return {"deleted": source}


def generate_answer(question: str, passages: list[dict]) -> tuple[str, str]:
    if not passages:
        return "I couldn't find a relevant passage in the documents provided.", "no_context"

    context = "\\n\\n".join(
        f"[{i}] Source: {p['source']} (chunk {p['chunk_id']})\\n{p['text']}"
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
                        "content": f"Question: {question}\\n\\nExcerpts:\\n{context}",
                    },
                ],
            )
            return response.output_text, "retrieval_plus_generation"
        except Exception:
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
        rows = db.execute("SELECT source, chunk_id, text FROM chunks").fetchall()
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
