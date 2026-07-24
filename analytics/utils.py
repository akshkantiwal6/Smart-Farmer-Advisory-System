import sqlite3
import pandas as pd


def get_filtered_data(commodity, state):

    conn = sqlite3.connect("database/agriculture.db")

    query = """
    SELECT *
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

    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["month"] = df["date"].dt.month

    return df.sort_values("date")