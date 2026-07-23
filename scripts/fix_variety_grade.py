import sqlite3
import pandas as pd

DB_PATH = "database/agriculture.db"
CSV_PATH = "data/processed/cleaned_latest.csv"

print("Reading latest cleaned CSV...")

df = pd.read_csv(CSV_PATH)

# Rename columns
df = df.rename(columns={
    "Commodity": "commodity_name",
    "State": "state",
    "District": "district",
    "Market": "market",
    "Arrival_Date": "date",
    "Variety": "variety",
    "Grade": "grade"
})

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

updated = 0

for _, row in df.iterrows():

    cursor.execute("""
        UPDATE market_data
        SET variety = ?,
            grade = ?
        WHERE commodity_name = ?
          AND state = ?
          AND district = ?
          AND market = ?
          AND date = ?
          AND variety IS NULL
          AND grade IS NULL
    """, (
        row["variety"],
        row["grade"],
        row["commodity_name"],
        row["state"],
        row["district"],
        row["market"],
        row["date"]
    ))

    updated += cursor.rowcount

conn.commit()
conn.close()

print("="*50)
print(f"Rows Updated : {updated}")
print("Migration Complete")
print("="*50)