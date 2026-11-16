# Industrial Diagnostics Assistant

A small, explainable API that checks motor temperature, vibration and operating pressure readings and returns actionable first-line findings.

## Why this project exists

Industrial teams often need a quick way to turn raw sensor readings into a consistent first check. This project demonstrates API design, input validation, rule modelling, test coverage and explainable output.

## Current scope

- FastAPI service with interactive OpenAPI docs.
- Three transparent diagnostic rules.
- Warning and critical severity levels.
- Sensor values, thresholds and recommendations included in every finding.
- Input validation and tests for normal, warning, critical and missing-data cases.

**Engineering note:** Version 0.1 uses deterministic threshold rules. It is not a trained machine-learning model and does not replace a qualified maintenance engineer. The thresholds are illustrative and must be calibrated against the actual machine, manufacturer guidance and operating context before real use.

## Run locally

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for the API interface.

## Example request

```json
{
  "temperature_c": 82.0,
  "vibration_mm_s": 3.1,
  "pressure_bar": 5.2
}
```

Send it to `POST /analyse`. The response includes an overall status and a list of findings with the measured value, triggering threshold and suggested inspection.

## Tests

```bash
pytest -q
```

## API routes

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | Service overview |
| GET | `/health` | Health check |
| GET | `/rules` | Configured rules and thresholds |
| POST | `/analyse` | Analyse one sensor snapshot |

## Next engineering steps

1. Add a small time-series dataset and trend-based checks.
2. Add equipment profiles so thresholds are configurable per machine.
3. Compare rule output with labelled maintenance cases.
4. Add an optional ML anomaly detector only after collecting suitable data.
