import sqlite3
import pandas as pd


def get_filtered_data(commodity, state):
    """
    Load filtered data directly from SQLite database.
    """

    conn = sqlite3.connect("database/agriculture.db")

    query = """
    SELECT
        commodity_name,
        state,
        district,
        market,
        min_price,
        max_price,
        modal_price,
        date
    FROM market_data
    WHERE commodity_name = ?
      AND state = ?
    """

    df = pd.read_sql_query(
        query,
        conn,
        params=(commodity, state)
    )

    conn.close()

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month

    return df.sort_values("date")