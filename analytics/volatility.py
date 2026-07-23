from analytics.utils import get_filtered_data


def analyze_volatility(commodity, state):
    """
    Analyze market price volatility.

    Returns:
        dict
    """

    filtered = get_filtered_data(commodity, state)

    if filtered.empty:
        return {
            "status": "No Data"
        }

    prices = filtered["modal_price"]

    std = prices.std()
    mean = prices.mean()

    cv = (std / mean) * 100

    if cv < 10:
        status = "Low"
        score = 20

    elif cv < 20:
        status = "Moderate"
        score = 12

    else:
        status = "High"
        score = 5

    return {

        "average_price": round(mean, 2),
        "std_deviation": round(std, 2),
        "coefficient_variation": round(cv, 2),

        "volatility_status": status,
        "volatility_score": score

    }


if __name__ == "__main__":

    result = analyze_volatility(

        commodity="Wheat",
        state="Rajasthan"

    )

    print(result)