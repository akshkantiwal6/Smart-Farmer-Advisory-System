"""
Clean latest government dataset.

Author: Aksh
"""

from pathlib import Path
import pandas as pd

INPUT_FOLDER = Path("data/incoming")
OUTPUT_FOLDER = Path("data/processed")

OUTPUT_FOLDER.mkdir(exist_ok=True)


def clean_latest():

    csv_files = list(INPUT_FOLDER.glob("*.csv"))

    if not csv_files:
        print(" No CSV found.")
        return None

    latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)

    print(f"Reading: {latest_file.name}")

    df = pd.read_csv(latest_file)

    # Remove duplicate rows
    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    print(f"Removed {before-after} duplicate rows")

    # Remove rows having missing prices
    df = df.dropna(subset=[
        "Min_x0020_Price",
        "Max_x0020_Price",
        "Modal_x0020_Price"
    ])

    # Convert Arrival Date
    df["Arrival_Date"] = pd.to_datetime(
        df["Arrival_Date"],
        dayfirst=True
    )

    # Convert prices
    price_cols = [
        "Min_x0020_Price",
        "Max_x0020_Price",
        "Modal_x0020_Price"
    ]

    for col in price_cols:
        df[col] = pd.to_numeric(df[col])

    output_file = OUTPUT_FOLDER / "cleaned_latest.csv"

    df.to_csv(output_file, index=False)

    print("\n Cleaning Complete")
    print(f"Rows : {len(df)}")
    print(f"Saved : {output_file}")

    return output_file


if __name__ == "__main__":
    clean_latest()