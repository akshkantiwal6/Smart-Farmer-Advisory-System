import plotly.express as px
import streamlit as st

# ==========================================================
# THEME COLOURS
# ==========================================================

CYAN = "#22d3ee"
TEAL = "#2dd4bf"
BLUE = "#3b82f6"
PURPLE = "#818cf8"
TEXT_MUTED = "#8b93b8"
GRID_COLOR = "rgba(148,163,184,0.10)"


# ==========================================================
# COMMON LAYOUT
# ==========================================================

def apply_layout(fig, height=420):

    fig.update_layout(

        template="plotly_dark",

        height=height,

        paper_bgcolor="rgba(0,0,0,0)",

        plot_bgcolor="rgba(0,0,0,0)",

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),

        title_x=0.02,

        title_font=dict(
            size=16,
            color="#e7ecff"
        ),

        font=dict(
            size=13,
            color=TEXT_MUTED,
            family="Poppins, sans-serif"
        ),

        legend=dict(
            bgcolor="rgba(0,0,0,0)"
        ),

        hoverlabel=dict(
            bgcolor="#161e46",
            font_color="#e7ecff",
            bordercolor="rgba(120,150,255,.25)"
        )

    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        color=TEXT_MUTED
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=GRID_COLOR,
        zeroline=False,
        color=TEXT_MUTED
    )

    return fig


# ==========================================================
# PRICE TREND
# ==========================================================

def price_trend_chart(df):

    temp = df.sort_values(
        "Arrival_Date"
    )

    fig = px.line(

        temp,

        x="Arrival_Date",

        y="Modal_Price",

        title="Historical Price Trend",

        markers=True

    )

    fig.update_traces(

        line=dict(
            width=4,
            color=CYAN
        ),

        marker=dict(
            size=6,
            color=BLUE,
            line=dict(width=1, color=CYAN)
        ),

        fill="tozeroy",

        fillcolor="rgba(34,211,238,0.10)"

    )

    apply_layout(fig, 430)

    st.plotly_chart(

        fig,

        use_container_width=True

    )


# ==========================================================
# MONTHLY AVERAGE
# ==========================================================

def monthly_average_chart(df):

    temp = df.copy()

    temp["Month"] = temp[
        "Arrival_Date"
    ].dt.strftime("%b")

    temp = (

        temp

        .groupby("Month")["Modal_Price"]

        .mean()

        .reset_index()

    )

    fig = px.bar(

        temp,

        x="Month",

        y="Modal_Price",

        title="Monthly Average Price"

    )

    fig.update_traces(
        marker=dict(
            color=temp["Modal_Price"],
            colorscale=[[0, BLUE], [0.5, CYAN], [1, TEAL]],
            line=dict(width=0)
        ),
        marker_cornerradius=8
    )

    apply_layout(fig, 430)

    st.plotly_chart(

        fig,

        use_container_width=True

    )