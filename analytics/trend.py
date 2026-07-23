from analytics.utils import get_filtered_data


def analyze_trend(commodity, state):
    """
    Analyze price trend for a commodity.
    Returns:
        dict
    """

    filtered = get_filtered_data(commodity, state)

    if filtered.empty:
        return {
            "status": "No Data"
        }

    last30 = filtered.tail(min(30, len(filtered)))
    last90 = filtered.tail(min(90, len(filtered)))

    avg30 = last30["modal_price"].mean()
    avg90 = last90["modal_price"].mean()

    trend30 = (
        (last30.iloc[-1]["modal_price"] -
         last30.iloc[0]["modal_price"])
        /
        last30.iloc[0]["modal_price"]
    ) * 100

    trend90 = (
        (last90.iloc[-1]["modal_price"] -
         last90.iloc[0]["modal_price"])
        /
        last90.iloc[0]["modal_price"]
    ) * 100

    score = 0

    if trend30 > 5:
        score += 20
        status30 = "Increasing"

    elif trend30 < -5:
        status30 = "Decreasing"

    else:
        score += 10
        status30 = "Stable"

    if trend90 > 5:
        score += 15
        status90 = "Increasing"

    elif trend90 < -5:
        status90 = "Decreasing"

    else:
        score += 8
        status90 = "Stable"

    return {

        "average_30": round(avg30, 2),
        "average_90": round(avg90, 2),

        "trend_30": round(trend30, 2),
        "trend_90": round(trend90, 2),

        "status_30": status30,
        "status_90": status90,

        "trend_score": score

    }


if __name__ == "__main__":

    result = analyze_trend(
        commodity="Wheat",
        state="Rajasthan"
    )

    print(result)