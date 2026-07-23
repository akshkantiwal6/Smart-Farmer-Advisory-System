from analytics.trend import analyze_trend
from analytics.seasonality import analyze_seasonality
from analytics.volatility import analyze_volatility


def generate_advisory(commodity, state):
    """
    Generate final advisory score by combining
    Trend + Seasonality + Volatility.
    """

    trend = analyze_trend(commodity, state)
    seasonality = analyze_seasonality(commodity, state)
    volatility = analyze_volatility(commodity, state)

    if (
        trend.get("status") == "No Data"
        or seasonality.get("status") == "No Data"
        or volatility.get("status") == "No Data"
    ):
        return {
            "status": "No Data"
        }

    total_score = (
        trend["trend_score"]
        + seasonality["seasonality_score"]
        + volatility["volatility_score"]
    )

    if total_score >= 50:
        recommendation = "GOOD"

    elif total_score >= 35:
        recommendation = "HOLD"

    else:
        recommendation = "WAIT"

    return {

        "trend_score": trend["trend_score"],

        "seasonality_score":
        seasonality["seasonality_score"],

        "volatility_score":
        volatility["volatility_score"],

        "total_score": total_score,

        "recommendation": recommendation

    }


if __name__ == "__main__":

    result = generate_advisory(

        commodity="Wheat",
        state="Rajasthan"

    )

    print(result)