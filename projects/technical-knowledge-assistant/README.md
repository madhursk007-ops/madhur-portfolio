# Technical Knowledge Assistant

A document-grounded Q&A API. It accepts text documents, splits them into overlapping passages, retrieves relevant passages for a question, and can optionally use an LLM to write an answer constrained to those passages.

## What is implemented

- Document ingestion with SQLite persistence.
- Overlapping text chunking.
- Transparent lexical retrieval baseline with relevance scores.
- Source title, chunk number and excerpt returned with every answer.
- Optional OpenAI Responses API generation.
- Honest retrieval-only mode when no API key is configured.
- Tests for chunking and retrieval.

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs.

## Try it

First add a document using `POST /documents`:

```json
{
  "title": "Motor Maintenance Notes",
  "text": "A motor bearing should be inspected when vibration increases. Misalignment and worn bearings are common causes of elevated vibration. Record vibration readings during routine maintenance and compare them with the equipment baseline."
}
```

Then ask a question using `POST /ask`:

```json
{
  "question": "What can cause elevated motor vibration?",
  "limit": 3
}
```

The response includes the answer mode and the retrieved source passages. To enable generated answers, copy `.env.example` to `.env`, set `OPENAI_API_KEY`, and export the variables in your shell before starting the API. Never commit a real API key.

## Tests

```bash
pytest -q
```

## Engineering decisions and limitations

The initial retriever uses lexical term overlap. It is intentionally easy to inspect and provides a baseline for later evaluation against embeddings or hybrid search. It is not semantic vector search. The optional generation step is constrained to retrieved excerpts, but LLM output still needs evaluation and can make mistakes. For production use, add authentication, document-level access controls, file parsing, rate limits, robust provider error handling, retrieval evaluation and audit logging.

## API routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | Service overview |
| GET | `/health` | Health check |
| POST | `/documents` | Ingest a text document |
| GET | `/documents` | List indexed document titles |
| POST | `/ask` | Retrieve passages and answer a question |
