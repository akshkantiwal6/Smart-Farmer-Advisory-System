import sqlite3
import pandas as pd
import streamlit as st


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

    st.write("Columns:", list(df.columns))
    st.write(df.head())

    if df.empty:
        return df

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.month

    st.write("Columns after processing:", list(df.columns))
    st.write(df.head())

    return df.sort_values("date")