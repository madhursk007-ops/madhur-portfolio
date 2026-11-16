from pathlib import Path
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "vehicles.csv"
NUMERIC = ["year", "km_driven", "engine_cc", "owner_count"]
CATEGORICAL = ["brand", "fuel", "transmission"]

def load_data():
    return pd.read_csv(DATA_PATH)

def build_model():
    preprocess = ColumnTransformer([
        ("numeric", StandardScaler(), NUMERIC),
        ("categorical", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
    ])
    return Pipeline([("preprocess", preprocess), ("regressor", Ridge(alpha=1.0))])

def train_model():
    data = load_data()
    X = data[NUMERIC + CATEGORICAL]
    y = data["price_lakh"]
    model = build_model()
    model.fit(X, y)
    return model, data

def estimate_price(year, km_driven, engine_cc, owner_count, brand, fuel, transmission):
    model, data = train_model()
    sample = pd.DataFrame([{
        "year": year, "km_driven": km_driven, "engine_cc": engine_cc,
        "owner_count": owner_count, "brand": brand, "fuel": fuel,
        "transmission": transmission,
    }])
    estimate = float(model.predict(sample)[0])
    return max(0.25, estimate), data
