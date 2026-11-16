# Technical Knowledge Assistant

A document-grounded Q&A application with a browser interface and FastAPI backend. Upload technical notes, index their text into overlapping passages, ask questions, and inspect the source excerpts returned by the retriever.

## Live demo

https://technical-knowledge-assistant.onrender.com

## What is implemented

- Browser-based Knowledge Desk served by FastAPI.
- Upload UTF-8 `.txt` and `.md` files (maximum 200 KB each).
- Paste text directly into the library.
- SQLite-backed passage indexing and document listing.
- Replace a document by uploading or adding text with the same title.
- Delete indexed documents from the library.
- Ask questions and inspect source title, chunk number, excerpt, and relevance score.
- Optional OpenAI Responses API generation when `OPENAI_API_KEY` is configured.
- Explicit retrieval-only mode when no API key is configured.
- API documentation at `/docs`.

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000 for the web interface or http://127.0.0.1:8000/docs for the API docs.

## How to use

1. Upload a UTF-8 `.txt` or `.md` file, or paste at least 40 characters of notes.
2. Check that the document appears in Your library.
3. Enter a question in Research assistant.
4. Review the response and the supporting passages, including their document names and chunk numbers.
5. Remove documents from the library when they are no longer needed.

The JSON API is also available:

- `POST /documents` — ingest a title and text.
- `POST /documents/upload` — upload a text or Markdown file.
- `GET /documents` — list indexed documents.
- `DELETE /documents/{source}` — remove a document.
- `POST /ask` — retrieve relevant passages and return an answer.

## Optional generated answers

Copy `.env.example` to `.env` and set `OPENAI_API_KEY` and optionally `OPENAI_MODEL`. Never commit a real API key. Without a key, the app clearly labels its output as a retrieval-only preview rather than pretending a language model generated it.

## Tests

```bash
pytest -q
```

## Engineering decisions and limitations

The initial retriever uses lexical term overlap. It is intentionally inspectable and provides a baseline for later evaluation against embeddings or hybrid search; it is not semantic vector search. The optional generation step is instructed to use only retrieved excerpts, but LLM output still needs evaluation and can make mistakes.

Only UTF-8 TXT and Markdown uploads are supported; PDF and DOCX parsing are not implemented. The SQLite database uses the `KNOWLEDGE_DB` environment variable or a local `knowledge.db` file. On a hosting platform with an ephemeral filesystem, indexed documents may be lost when the instance is replaced or restarted; configure a persistent disk and set `KNOWLEDGE_DB` to its mounted path for durable hosted storage.

For production use, add authentication, document-level access controls, rate limits, retrieval evaluation, audit logging, and a persistent storage strategy.
