import pandas as pd

# Load dataset
df = pd.read_csv("data/raw/agriculture.csv")

print("Original Shape:", df.shape)

# Remove missing values
df = df.dropna()

# Remove duplicate rows
df = df.drop_duplicates()

# Convert date column
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Remove rows where date conversion failed
df = df.dropna(subset=["date"])

# Remove negative prices (if any)
price_cols = ["min_price", "max_price", "modal_price"]

for col in price_cols:
    df = df[df[col] >= 0]

# Remove extra spaces
text_cols = ["commodity_name", "state", "district", "market"]

for col in text_cols:
    df[col] = df[col].astype(str).str.strip()

# Save cleaned dataset
output_path = "data/processed/cleaned_agriculture.csv"
df.to_csv(output_path, index=False)

print("Cleaned Shape:", df.shape)
print("Saved to:", output_path)
print("Cleaning Completed Successfully!")