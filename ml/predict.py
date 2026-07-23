import joblib
import pandas as pd

# -----------------------------
# Load Model
# -----------------------------
model = joblib.load("ml/model/random_forest.pkl")

encoders = joblib.load("ml/model/label_encoders.pkl")

feature_columns = joblib.load("ml/model/feature_columns.pkl")


# -----------------------------
# Prediction Function
# -----------------------------
def predict_price(
    commodity,
    state,
    district,
    market,
    year,
    month,
    day
):

    # Remove extra spaces
    commodity = commodity.strip()
    state = state.strip()
    district = district.strip()
    market = market.strip()

    # Encode categorical inputs
    try:
        commodity = encoders["commodity_name"].transform([commodity])[0]
        state = encoders["state"].transform([state])[0]
        district = encoders["district"].transform([district])[0]
        market = encoders["market"].transform([market])[0]

    except ValueError as e:
        raise ValueError(
            "Invalid Commodity / State / District / Market.\n"
            "Please enter values available in the dataset."
        ) from e

    # Date feature
    day_of_week = pd.Timestamp(
        year=year,
        month=month,
        day=day
    ).dayofweek

    # Input dataframe
    sample = pd.DataFrame([{
        "commodity_name": commodity,
        "state": state,
        "district": district,
        "market": market,
        "year": year,
        "month": month,
        "day": day,
        "day_of_week": day_of_week
    }])

    # Ensure correct column order
    sample = sample[feature_columns]

    prediction = model.predict(sample)[0]

    return round(prediction, 2)


# -----------------------------
# Terminal Mode
# -----------------------------
if __name__ == "__main__":

    print("=" * 50)
    print("SMART FARMER PRICE PREDICTION")
    print("=" * 50)

    commodity = input("Commodity : ").strip()
    state = input("State : ").strip()
    district = input("District : ").strip()
    market = input("Market : ").strip()

    year = int(input("Year : "))
    month = int(input("Month : "))
    day = int(input("Day : "))

    try:
        price = predict_price(
            commodity,
            state,
            district,
            market,
            year,
            month,
            day
        )

        print("\n" + "=" * 50)
        print("PREDICTION RESULT")
        print("=" * 50)
        print(f"Predicted Modal Price : ₹ {price:.2f}")

    except Exception as e:
        print("\nERROR:")
        print(e)