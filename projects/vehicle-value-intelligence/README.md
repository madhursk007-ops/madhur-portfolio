# Vehicle Value Intelligence

An end-to-end machine-learning demo that estimates used-car prices from age, mileage, engine capacity, ownership history, brand, fuel, and transmission.

## Stack
- Python, pandas, scikit-learn
- Ridge regression in a preprocessing pipeline
- Streamlit interface
- pytest

## Run locally
```bash
cd projects/vehicle-value-intelligence
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app/main.py
```

## Model and limitations
The model is trained on the included small, illustrative dataset. It demonstrates feature preprocessing, categorical encoding, regression, and inference; it is not trained on live listings and must not be treated as a market appraisal. Improve it with a larger, licensed, representative dataset and evaluate it on a held-out test set before any real-world use.

## Tests
```bash
PYTHONPATH=. pytest -q
```
