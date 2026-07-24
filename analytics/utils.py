import sqlite3
import pandas as pd
import streamlit as st


def get_filtered_data(commodity, state):
    st.write("DEBUG: utils.py loaded")

    conn = sqlite3.connect("database/agriculture.db")

    st.write("DEBUG: DB connected")

    query = """
    SELECT *
    FROM market_data
    LIMIT 5
    """

    df = pd.read_sql_query(query, conn)

    st.write(df.head())

    conn.close()

    return df