import pandas as pd


def get_filtered_data(
    commodity,
    state,
    csv_path="data/processed/cleaned_agriculture.csv"
):
    """
    Load dataset and return filtered data.
    """

    df = pd.read_csv(csv_path)

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month

    filtered = df[
        (df["commodity_name"] == commodity) &
        (df["state"] == state)
    ].copy()

    filtered = filtered.sort_values("date")

    return filtered