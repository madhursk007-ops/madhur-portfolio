import streamlit as st
from model import train_model, estimate_price

st.set_page_config(page_title="Vehicle Value Intelligence", page_icon="🚗", layout="wide")
st.title("🚗 Vehicle Value Intelligence")
st.caption("A machine-learning demo that estimates used-car prices from vehicle attributes.")
model, data = train_model()
c1, c2, c3 = st.columns(3)
c1.metric("Training records", f"{len(data):,}")
c2.metric("Brands covered", data["brand"].nunique())
c3.metric("Median listed value", f"₹{data['price_lakh'].median():.2f} lakh")
st.divider()
st.subheader("Estimate a vehicle's value")
with st.form("estimate"):
    left, right = st.columns(2)
    with left:
        brand = st.selectbox("Brand", sorted(data.brand.unique()))
        year = st.slider("Model year", 2012, 2025, 2020)
        km = st.number_input("Kilometers driven", 0, 250000, 45000, step=5000)
        engine = st.selectbox("Engine capacity (cc)", sorted(data.engine_cc.unique()), index=2)
    with right:
        fuel = st.selectbox("Fuel", sorted(data.fuel.unique()))
        transmission = st.selectbox("Transmission", sorted(data.transmission.unique()))
        owners = st.selectbox("Number of previous owners", [1, 2, 3, 4], index=0)
    submitted = st.form_submit_button("Estimate price", type="primary")
if submitted:
    price, _ = estimate_price(year, km, engine, owners, brand, fuel, transmission)
    st.success(f"Estimated value: ₹{price:.2f} lakh")
    st.caption("This is an educational estimate from a small illustrative dataset, not a verified market valuation.")
st.divider()
st.subheader("Explore the sample data")
st.dataframe(data, use_container_width=True, hide_index=True)
