import pandas as pd
import joblib
import os
import sqlite3

from sklearn.preprocessing import LabelEncoder

# -----------------------------
# Load cleaned dataset
# -----------------------------
conn = sqlite3.connect("database/agriculture.db")

query = """
SELECT
    commodity_name,
    state,
    district,
    market,
    min_price,
    max_price,
    modal_price,
    date
FROM market_data
"""

df = pd.read_sql(query, conn)

conn.close()

# -----------------------------
# Date Feature Engineering
# -----------------------------
df["date"] = pd.to_datetime(df["date"])

df["year"] = df["date"].dt.year
df["month"] = df["date"].dt.month
df["day"] = df["date"].dt.day
df["day_of_week"] = df["date"].dt.dayofweek

# -----------------------------
# Encode categorical columns
# -----------------------------
categorical_cols = [
    "commodity_name",
    "state",
    "district",
    "market"
]

encoders = {}

for col in categorical_cols:
    encoder = LabelEncoder()
    df[col] = encoder.fit_transform(df[col].astype(str))

    encoders[col] = encoder

# -----------------------------
# Save encoders
# -----------------------------
os.makedirs("ml/model", exist_ok=True)

joblib.dump(
    encoders,
    "ml/model/label_encoders.pkl"
)

# -----------------------------
# Select Features
# -----------------------------
features = [
    "commodity_name",
    "state",
    "district",
    "market",
    "year",
    "month",
    "day",
    "day_of_week"
]

target = "modal_price"

# Save feature list
joblib.dump(
    features,
    "ml/model/feature_columns.pkl"
)

# Save processed dataset
processed = df[features + [target]]

processed.to_csv(
    "ml/model/processed_data.csv",
    index=False
)

print("=" * 50)
print("PREPROCESSING COMPLETED")
print("=" * 50)

print("Rows :", processed.shape[0])
print("Columns :", processed.shape[1])

print("\nSaved Files")

print("✔ processed_data.csv")
print("✔ label_encoders.pkl")
print("✔ feature_columns.pkl")