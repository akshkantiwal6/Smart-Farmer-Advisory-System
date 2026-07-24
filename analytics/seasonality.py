from analytics.utils import get_filtered_data


def analyze_seasonality(commodity, state):
    """
    Analyze seasonal pricing pattern.
    Returns:
        dict
    """

    filtered = get_filtered_data(commodity, state)

    if filtered.empty:
        return {
            "status": "No Data"
        }

    latest_month = filtered["month"].max()

    seasonal_avg = filtered.groupby("month")["modal_price"].mean()

    current_month_avg = seasonal_avg.loc[latest_month]

    overall_avg = filtered["modal_price"].mean()

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


if __name__ == "__main__":
    result = analyze_seasonality(
        commodity="Wheat",
        state="Rajasthan"
    )

    print(result)