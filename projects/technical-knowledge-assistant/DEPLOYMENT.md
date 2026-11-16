# Deployment notes

## Render service

- Service: `technical-knowledge-assistant`
- Runtime: Python / FastAPI
- Build command: `cd projects/technical-knowledge-assistant && pip install -r requirements.txt`
- Start command: `cd projects/technical-knowledge-assistant && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check: `GET /health`

## Deploying updates

The Render service is connected to the `ai-engineering-projects-2026` branch with automatic deploys enabled. Push changes to this branch and confirm that a new deployment appears in the Render Events tab. After deployment, verify the home page, document upload, document listing, question answering, and document deletion.
