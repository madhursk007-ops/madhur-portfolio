# Vehicle Value Intelligence

An interactive used-car price estimation demo built to demonstrate an end-to-end machine-learning workflow. Users can explore a small vehicle dataset, inspect feature distributions, and estimate a sample vehicle's value through a Streamlit dashboard.

## Live demo

https://vehicle-value-intelligence.onrender.com

## Features

- Interactive Streamlit dashboard with Overview, Price Estimator, and Dataset Explorer tabs.
- Vehicle inputs: model year, kilometers driven, engine capacity, previous owners, brand, fuel, and transmission.
- Scikit-learn pipeline with numeric standardization, one-hot encoding, and Ridge regression.
- Sample dataset exploration with brand/fuel filters and a mileage-versus-price scatter plot.
- Cached model loading to avoid retraining on every Streamlit rerun.
- Automated tests for dataset shape and prediction behavior.

## Technology

- Python
- Streamlit
- pandas
- scikit-learn
- pytest

## Run locally

```bash
cd projects/vehicle-value-intelligence
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app/main.py
```

## Model workflow

1. Load the CSV dataset from `data/vehicles.csv`.
2. Standardize numeric features: year, kilometers driven, engine capacity, and owner count.
3. One-hot encode categorical features: brand, fuel, and transmission.
4. Fit a Ridge regression estimator.
5. Pass user-selected vehicle attributes through the same fitted pipeline to generate an estimate.

## Dataset and limitations

The included dataset contains only 24 illustrative records. It is intentionally small and is not a representative sample of the Indian used-car market. The model has not been validated on a sufficiently large, independent, current dataset. Predictions are for demonstrating preprocessing and regression only; they must not be used as a buying, selling, financing, or insurance valuation.

A stronger next version should use a larger licensed dataset, document collection dates and geography, create a train/validation/test split, report MAE and R², compare baseline models, and monitor performance drift.

## Tests

```bash
PYTHONPATH=. pytest -q
```

## Repository layout

```text
vehicle-value-intelligence/
├── app/
│   ├── main.py
│   └── model.py
├── data/
│   └── vehicles.csv
├── tests/
│   └── test_model.py
├── requirements.txt
└── README.md
```
