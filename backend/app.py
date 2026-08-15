"""Flask API serving SuperKart product-store sales forecasts."""

import joblib
import pandas as pd
from flask import Flask, jsonify, request

superkart_api = Flask("SuperKart Sales Forecast API - By Utkarsh Agnihotri")

MODEL_PATH = "superkart_sales_forecast_model_v1_0.joblib"
model = joblib.load(MODEL_PATH)

FEATURE_COLUMNS = [
    "Product_Weight",
    "Product_Sugar_Content",
    "Product_Allocated_Area",
    "Product_MRP",
    "Store_Size",
    "Store_Location_City_Type",
    "Store_Type",
    "Product_Id_char",
    "Store_Age_Years",
    "Product_Type_Category",
]


@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart Sales Forecast API! - by Utkarsh Agnihotri"


@superkart_api.post("/v1/predict")
def predict_sales():
    """Online inference for a single product-store record."""
    payload = request.get_json()
    sample = {col: payload[col] for col in FEATURE_COLUMNS}
    input_frame = pd.DataFrame([sample])
    prediction = float(model.predict(input_frame)[0])
    return jsonify({"Sales": round(prediction, 2)})


@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():
    """Batch inference from an uploaded CSV file."""
    file = request.files["file"]
    input_data = pd.read_csv(file)

    predictions = model.predict(input_data[FEATURE_COLUMNS]).tolist()
    predictions = [round(float(value), 2) for value in predictions]

    if "Product_Id" in input_data.columns:
        keys = input_data["Product_Id"].astype(str).tolist()
    else:
        keys = [str(i) for i in range(len(predictions))]

    return dict(zip(keys, predictions))


if __name__ == "__main__":
    superkart_api.run(debug=True)
