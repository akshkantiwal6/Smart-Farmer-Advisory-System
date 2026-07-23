from pathlib import Path
import pandas as pd

# Folder where latest government CSV is placed
INPUT_FOLDER = Path("data/incoming")

def validate_csv():

    # Find all CSV files
    csv_files = list(INPUT_FOLDER.glob("*.csv"))

    if not csv_files:
        print("❌ No CSV found in data/incoming/")
        return

    latest_file = max(csv_files, key=lambda x: x.stat().st_mtime)

    print("=" * 60)
    print("Checking:", latest_file.name)
    print("=" * 60)

    df = pd.read_csv(latest_file)

    print("\nRows    :", len(df))
    print("Columns :", len(df.columns))

    print("\nColumn Names:\n")

    for col in df.columns:
        print(col)

    print("\nFirst 5 Rows:\n")
    print(df.head())


if __name__ == "__main__":
    validate_csv()