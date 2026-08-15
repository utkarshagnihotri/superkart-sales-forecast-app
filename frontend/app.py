import pandas as pd
import requests
import streamlit as st

BACKEND_URL = "http://backend:7860"

st.title("SuperKart Sales Forecast - By Utkarsh Agnihotri")

st.subheader("Online Prediction")

Product_Weight = st.number_input("Product Weight", min_value=0.0, value=12.66)
Product_Sugar_Content = st.selectbox(
    "Product Sugar Content", ["Low Sugar", "Regular", "No Sugar"]
)
Product_Allocated_Area = st.number_input(
    "Product Allocated Area", min_value=0.0, max_value=1.0, value=0.07, format="%.4f"
)
Product_MRP = st.number_input("Product MRP", min_value=0.0, value=150.0)
Store_Size = st.selectbox("Store Size", ["High", "Medium", "Small"])
Store_Location_City_Type = st.selectbox(
    "Store Location City Type", ["Tier 1", "Tier 2", "Tier 3"]
)
Store_Type = st.selectbox(
    "Store Type",
    ["Departmental Store", "Food Mart", "Supermarket Type1", "Supermarket Type2"],
)
Product_Id_char = st.selectbox("Product Id Prefix", ["FD", "DR", "NC"])
Store_Age_Years = st.number_input("Store Age (Years)", min_value=0, value=16, step=1)
Product_Type_Category = st.selectbox(
    "Product Type Category", ["Perishables", "Non Perishables"]
)

product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category,
}

if st.button("Predict", type="primary"):
    response = requests.post(f"{BACKEND_URL}/v1/predict", json=product_data)
    if response.status_code == 200:
        predicted_sales = response.json()["Sales"]
        st.success(f"Predicted Product Store Sales Total: {predicted_sales:.2f}")
    else:
        st.error("Unable to reach the SuperKart prediction API.")

st.subheader("Batch Prediction")
uploaded_file = st.file_uploader(
    "Upload a CSV file with the model feature columns (optional Product_Id for keys)",
    type=["csv"],
)

if uploaded_file is not None:
    if st.button("Predict Batch", type="primary"):
        response = requests.post(
            f"{BACKEND_URL}/v1/predictbatch", files={"file": uploaded_file}
        )
        if response.status_code == 200:
            st.success("Batch predictions completed!")
            st.write(response.json())
        else:
            st.error("Unable to reach the SuperKart batch prediction API.")
