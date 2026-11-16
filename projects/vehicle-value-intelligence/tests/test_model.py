from app.model import estimate_price, load_data, train_model

def test_dataset_has_required_columns():
    data = load_data()
    assert {"brand", "year", "km_driven", "price_lakh"}.issubset(data.columns)
    assert len(data) >= 20

def test_model_trains_and_predicts_positive_value():
    model, data = train_model()
    row = data.iloc[[0]][["year", "km_driven", "engine_cc", "owner_count", "brand", "fuel", "transmission"]]
    prediction = float(model.predict(row)[0])
    assert prediction > 0

def test_estimate_price_returns_positive_value():
    price, _ = estimate_price(2020, 45000, 1500, 1, "Hyundai", "Petrol", "Automatic")
    assert price > 0
