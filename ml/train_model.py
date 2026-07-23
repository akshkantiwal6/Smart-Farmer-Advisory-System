import json
import time
import os
import joblib
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# -----------------------------
# Load processed data
# -----------------------------
df = pd.read_csv("ml/model/processed_data.csv")

# Features and Target
X = df.drop(columns=["modal_price"])
y = df["modal_price"]

# -----------------------------
# Train Test Split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# -----------------------------
# Random Forest Model
# -----------------------------
model = RandomForestRegressor(
    n_estimators=50,
    max_depth=20,
    min_samples_split=5,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)

print("=" * 50)
print("TRAINING MODEL...")
print("=" * 50)

start = time.time()

model.fit(X_train, y_train)

end = time.time()

# -----------------------------
# Prediction
# -----------------------------
y_pred = model.predict(X_test)

# -----------------------------
# Evaluation
# -----------------------------
mae = mean_absolute_error(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5
r2 = r2_score(y_test, y_pred)

# -----------------------------
# Save Model
# -----------------------------
joblib.dump(
    model,
    "ml/model/random_forest.pkl",
    compress=3
)

# -----------------------------
# Save Metrics
# -----------------------------
metrics = {
    "MAE": round(mae, 2),
    "RMSE": round(rmse, 2),
    "R2_Score": round(r2, 4)
}

with open("ml/metrics.json", "w") as f:
    json.dump(metrics, f, indent=4)

# -----------------------------
# Feature Importance
# -----------------------------
importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

importance.to_csv(
    "ml/feature_importance.csv",
    index=False
)

# -----------------------------
# Model Size
# -----------------------------
size_mb = os.path.getsize(
    "ml/model/random_forest.pkl"
) / (1024 * 1024)

# -----------------------------
# Output
# -----------------------------
print("\n" + "=" * 50)
print("MODEL TRAINED SUCCESSFULLY")
print("=" * 50)

print(f"Training Time : {end-start:.2f} sec")
print(f"Model Size    : {size_mb:.2f} MB")

print(f"\nMAE       : {mae:.2f}")
print(f"RMSE      : {rmse:.2f}")
print(f"R2 Score  : {r2:.4f}")

print("\nSaved Files")
print("✔ random_forest.pkl")
print("✔ metrics.json")
print("✔ feature_importance.csv")