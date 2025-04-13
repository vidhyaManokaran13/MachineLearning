from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import pickle
import matplotlib.pyplot as plt
import os

app = FastAPI()

# CORS config
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
model = pickle.load(open("zillow_model.pkl", "rb"))

@app.post("/predict")
async def predict(
    bedrooms: int = Form(...),
    bathrooms: int = Form(...),
    sqft: float = Form(...),
    future_year: int = Form(...)
):
    current_year = 2025
    years_ahead = max(future_year - current_year, 0)

    input_data = [[bedrooms, bathrooms, sqft, current_year]]
    prediction = model.predict(input_data)[0]
    future_price = prediction * (1.05 ** years_ahead)

    return {"predicted_price": round(future_price)}


@app.post("/history-predict")
async def history_predict(
    bedrooms: int = Form(...),
    bathrooms: int = Form(...),
    sqft: float = Form(...),
    yearBuilt: int = Form(...),
    future_year: int = Form(...)
):
    current_year = 2025
    future_year = max(future_year, current_year)
    input_data = [[bedrooms, bathrooms, sqft, current_year]]

    years = list(range(yearBuilt, future_year + 1))
    base_price = model.predict(input_data)[0]

    prices = [round(base_price * (1.05 ** (y - current_year))) for y in years]

    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(years, prices, marker='o', linestyle='-', color='teal')
    plt.title("Predicted House Price Trend")
    plt.xlabel("Year")
    plt.ylabel("Price (INR)")
    plt.grid(True)

    # Save the plot
    image_path = "static/history_plot.png"
    os.makedirs("static", exist_ok=True)
    plt.savefig(image_path)
    plt.close()

    return FileResponse(image_path, media_type="image/png")
