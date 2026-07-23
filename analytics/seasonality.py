import pandas as pd


def analyze_seasonality(
    commodity,
    state,
    csv_path="data/processed/cleaned_agriculture.csv"
):
    """
    Analyze seasonal pricing pattern.
    Returns:
        dict
    """

    df = pd.read_csv(csv_path)

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month

    filtered = df[
        (df["commodity_name"] == commodity) &
        (df["state"] == state)
    ].copy()

    if filtered.empty:
        return {
            "status": "No Data"
        }

    latest_month = filtered["month"].max()

    seasonal_avg = filtered.groupby("month")["modal_price"].mean()

    current_month_avg = seasonal_avg.loc[latest_month]

    overall_avg = filtered["modal_price"].mean()

    score = 0

    if current_month_avg > overall_avg * 1.05:
        score = 15
        status = "Favourable"

    elif current_month_avg < overall_avg * 0.95:
        score = 5
        status = "Unfavourable"

    else:
        score = 10
        status = "Normal"

    return {

        "current_month": int(latest_month),

        "seasonal_average": round(current_month_avg, 2),

        "overall_average": round(overall_avg, 2),

        "seasonality_status": status,

        "seasonality_score": score

    }


# -----------------------------
# Test
# -----------------------------
if __name__ == "__main__":

    result = analyze_seasonality(
        commodity="Wheat",
        state="Rajasthan"
    )

    print(result)