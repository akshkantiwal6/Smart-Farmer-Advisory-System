import subprocess
import sqlite3
from datetime import date, datetime
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from streamlit.components.v1 import html

from ui.charts import (
    price_trend_chart,
    monthly_average_chart
)

from analytics.trend import analyze_trend
from analytics.seasonality import analyze_seasonality
from analytics.volatility import analyze_volatility
from analytics.advisory_score import generate_advisory

from ml.predict import predict_price

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="Smart Farmer Advisory System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# LOAD CSS
# ----------------------------------------------------

css_path = Path(__file__).parent / "assets" / "style.css"

with open(css_path, encoding="utf-8") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )

# ----------------------------------------------------
# THEME COLOURS (used by gauges / score bars below)
# ----------------------------------------------------

BLUE = "#3b82f6"
CYAN = "#22d3ee"
TEAL = "#2dd4bf"
PURPLE = "#818cf8"
WARNING = "#f59e0b"
DANGER = "#f43f5e"

# Maximum possible points per analytics/advisory_score.py
# (trend max 20+15=35, seasonality max 15, volatility max 20)
MAX_TREND_SCORE = 35
MAX_SEASONALITY_SCORE = 15
MAX_VOLATILITY_SCORE = 20
MAX_TOTAL_SCORE = MAX_TREND_SCORE + MAX_SEASONALITY_SCORE + MAX_VOLATILITY_SCORE

NAV_ITEMS = [
    "🏠 Dashboard",
    "🔮 Prediction",
    "📊 Analytics",
    "📋 Records",
    "ℹ About"
]

PAGE_HEADERS = {
    "🏠 Dashboard": ("Dashboard Overview", "Real-Time Agricultural Price Analytics"),
    "🔮 Prediction": ("AI Price Prediction", "Machine Learning Powered Forecast"),
    "📊 Analytics": ("Market Analytics", "Deep Dive Into Price Patterns"),
    "📋 Records": ("Latest Market Records", "Raw Market Data Explorer"),
    "ℹ About": ("About This Project", "Smart Farmer Advisory System"),
}

# ----------------------------------------------------
# DATA
# ----------------------------------------------------

@st.cache_data
def load_data():

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
    """

    df = pd.read_sql(query, conn)

    conn.close()

    df = df.rename(columns={
        "commodity_name": "Commodity",
        "state": "State",
        "district": "District",
        "market": "Market",
        "modal_price": "Modal_Price",
        "min_price": "Min_Price",
        "max_price": "Max_Price",
        "date": "Arrival_Date"
    })

    df["Arrival_Date"] = pd.to_datetime(df["Arrival_Date"])

    return df


@st.cache_data
def get_last_updated():

    conn = sqlite3.connect("database/agriculture.db")

    query = """
    SELECT MAX(date) AS last_updated
    FROM market_data
    """

    last_updated = pd.read_sql(query, conn)

    conn.close()

    return last_updated.iloc[0]["last_updated"]


df = load_data()
last_updated = get_last_updated()

# ----------------------------------------------------
# HELPERS
# ----------------------------------------------------

def rupees(value):
    return f"₹{value:,.2f}"


def latest_price(data):
    return data.sort_values("Arrival_Date")["Modal_Price"].iloc[-1]


def average_price(data):
    return data["Modal_Price"].mean()


def total_records(data):
    return len(data)


def get_commodities():
    return sorted(df["Commodity"].dropna().unique())


def get_states(commodity):
    temp = df[df["Commodity"] == commodity]
    return sorted(temp["State"].dropna().unique())


def get_districts(commodity, state):
    temp = df[
        (df["Commodity"] == commodity)
        &
        (df["State"] == state)
    ]
    return sorted(temp["District"].dropna().unique())


def get_markets(commodity, state, district):
    temp = df[
        (df["Commodity"] == commodity)
        &
        (df["State"] == state)
        &
        (df["District"] == district)
    ]
    return sorted(temp["Market"].dropna().unique())


# ----------------------------------------------------
# UI HELPERS (visual only — no business logic here)
# ----------------------------------------------------

def status_color(status_text):
    """Map an analytics status string to a theme colour."""
    positive = {"Increasing", "Favourable", "Low"}
    neutral = {"Stable", "Normal", "Moderate"}
    negative = {"Decreasing", "Unfavourable", "High"}

    if status_text in positive:
        return TEAL
    if status_text in neutral:
        return CYAN
    if status_text in negative:
        return DANGER
    return BLUE


def render_score_bar(label, value, max_value, color=CYAN):
    """Custom gradient progress bar (used for score breakdowns)."""

    pct = 0 if max_value == 0 else max(0, min(100, (value / max_value) * 100))

    st.markdown(
        f"""<div class="score-row">
<div class="score-row-head">
<span>{label}</span>
<span class="val">{value} / {max_value}</span>
</div>
<div class="score-track">
<div class="score-fill" style="width:{pct}%; background:linear-gradient(90deg, {color}, {CYAN});"></div>
</div>
</div>""",
        unsafe_allow_html=True
    )


def badge_for_recommendation(text):
    mapping = {
        "BUY": ("badge-teal", "🟢"),
        "SELL": ("badge-teal", "🟢"),
        "HOLD": ("badge-orange", "🟡"),
        "WAIT": ("badge-red", "🔴"),
    }
    cls, icon = mapping.get(text, ("badge-blue", "🔵"))
    st.markdown(
        f'<span class="badge {cls}">{icon} Recommendation : {text}</span>',
        unsafe_allow_html=True
    )


def mini_gauges(items, height=190):
    """
    Row of small circular percentage gauges — mirrors the
    percentage rings shown at the top of the reference dashboard.
    items: list of (label, value, max_value, color)
    """

    fig = go.Figure()
    n = len(items)

    for i, (label, value, max_value, color) in enumerate(items):
        pct = 0 if max_value == 0 else round((value / max_value) * 100)
        display_text = f"{value} / {max_value}"
        gap = 0.035
        x0 = i / n + gap
        x1 = (i + 1) / n - gap

        fig.add_trace(go.Indicator(
            mode="gauge+number",
            value=value,
            number={"prefix": "","suffix": "","valueformat": "","font": {"size": 22, "color": "#e7ecff"}},
            title={"text": label, "font": {"size": 12.5, "color": "#8b93b8"}},
            gauge={
                "axis": {"visible": False, "range": [0, max_value]},
                "bar": {"color": color, "thickness": 0.28},
                "bgcolor": "rgba(255,255,255,0.06)",
                "borderwidth": 0,
            },
            domain={"x": [x0, x1], "y": [0, 1]}
        ))

    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=35, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins, sans-serif")
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def total_score_gauge(score, max_score, height=260):
    """Large half-donut gauge for the overall advisory score."""

    pct = 0 if max_score == 0 else round((score / max_score) * 100)

    if pct >= 60:
        color = TEAL
    elif pct >= 35:
        color = WARNING
    else:
        color = DANGER

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"size": 34, "color": "#e7ecff"}, "suffix": f" / {max_score}"},
        gauge={
            "axis": {"range": [0, max_score], "visible": False},
            "bar": {"color": color, "thickness": 0.3},
            "bgcolor": "rgba(255,255,255,0.06)",
            "borderwidth": 0,
        },
        domain={"x": [0, 1], "y": [0, 1]}
    ))

    fig.update_layout(
        height=height,
        margin=dict(l=20, r=20, t=10, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins, sans-serif", color="#e7ecff")
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


# ----------------------------------------------------
# SIDEBAR — filters only (navigation lives in the top bar)
# ----------------------------------------------------

with st.sidebar:

    st.markdown(
        """<div class="sidebar-top">
<div class="avatar">🌾</div>
<div class="sidebar-title">Smart Farmer</div>
<div class="sidebar-subtitle">AI Market Intelligence</div>
</div>""",
        unsafe_allow_html=True
    )

    st.markdown("<div class='sidebar-label'>Commodity</div>", unsafe_allow_html=True)

    commodity = st.selectbox(
        "Commodity",
        get_commodities(),
        key="commodity",
        label_visibility="collapsed"
    )

    st.markdown("<div class='sidebar-label'>State</div>", unsafe_allow_html=True)

    state = st.selectbox(
        "State",
        get_states(commodity),
        key="state",
        label_visibility="collapsed"
    )

    st.markdown("<div class='sidebar-label'>District</div>", unsafe_allow_html=True)

    district = st.selectbox(
        "District",
        get_districts(
            commodity,
            state
        ),
        key="district",
        label_visibility="collapsed"
    )

    st.markdown("<div class='sidebar-label'>Market</div>", unsafe_allow_html=True)

    market = st.selectbox(
        "Market",
        get_markets(
            commodity,
            state,
            district
        ),
        key="market",
        label_visibility="collapsed"
    )

    st.markdown("<div class='sidebar-label'>Prediction Date</div>", unsafe_allow_html=True)

    selected_date = st.date_input(
        "Prediction Date",
        value=date.today(),
        min_value=date.today()
    )
# ----------------------------------------------------
# FILTER DATA
# ----------------------------------------------------

filtered = df[
    (df["Commodity"] == commodity)
    &
    (df["State"] == state)
    &
    (df["District"] == district)
    &
    (df["Market"] == market)
].copy()

# ----------------------------------------------------
# TOP NAVBAR — branding + page navigation + profile
# ----------------------------------------------------

if "page" not in st.session_state:
    st.session_state.page = NAV_ITEMS[0]

brand_col, *nav_cols, profile_col = st.columns(
    [2.6] + [1] * len(NAV_ITEMS) + [0.6]
)

with brand_col:
    st.markdown(
        """<div class="nav-left">
<div class="logo"></div>
<div>
<div class="project-name">Smart Farmer Advisory System</div>
<div class="project-desc">AI Powered Market Intelligence Dashboard</div>
</div>
</div>""",
        unsafe_allow_html=True
    )

for col, item in zip(nav_cols, NAV_ITEMS):
    with col:
        is_active = st.session_state.page == item
        if st.button(
            item,
            key=f"nav_{item}",
            use_container_width=True,
            type="primary" if is_active else "secondary"
        ):
            st.session_state.page = item
            st.rerun()

with profile_col:
    st.markdown('<div class="profile"></div>', unsafe_allow_html=True)

page = st.session_state.page

st.write("")

# ----------------------------------------------------
# PAGE HEADER (title changes per page)
# ----------------------------------------------------

header_title, header_subtitle = PAGE_HEADERS.get(page, PAGE_HEADERS["🏠 Dashboard"])


st.markdown(
    f"""<div class="dashboard-header">
<div>
<div class="dashboard-title">{header_title}</div>
<div class="dashboard-subtitle">{header_subtitle}</div>
</div>
<div class="dashboard-status">Version 1.0</div>
</div>""",
    unsafe_allow_html=True
)

# ----------------------------------------------------
# SHARED ANALYTICS
# (computed once, before page routing, so every page
#  — Dashboard, Prediction, etc. — can use them)
# ----------------------------------------------------

if filtered.empty:
    st.error("No data available for selected filters.")
    st.stop()

trend = analyze_trend(commodity, state)

seasonality = analyze_seasonality(commodity, state)

volatility = analyze_volatility(commodity, state)

advisory = generate_advisory(commodity, state)

# If user selects today or past date,
# show actual historical price

if selected_date <= date.today():

    historical = filtered[
        filtered["Arrival_Date"].dt.date == selected_date
    ]

    if not historical.empty:
        predicted_price = historical["Modal_Price"].iloc[-1]
        prediction_type = "Historical"

    else:
        predicted_price = latest_price(filtered)
        prediction_type = "Historical"

else:

    if selected_date < date.today():
        st.warning("⚠️ Please select today or a future date for price prediction.")
        st.stop()


current_price = latest_price(filtered)
avg_price = average_price(filtered)

if selected_date == date.today():

    predicted_price = current_price
    prediction_type = "Current"

elif selected_date > date.today():

    predicted_price = predict_price(
        commodity=commodity,
        state=state,
        district=district,
        market=market,
        year=selected_date.year,
        month=selected_date.month,
        day=selected_date.day
    )

    prediction_type = "Predicted"

else:

    st.warning("⚠️ Please select today or a future date for price prediction.")
    st.stop()

change = predicted_price - current_price

if current_price != 0:
    percent = (change / current_price) * 100
else:
    percent = 0

records = total_records(filtered)
# ====================================================
# PAGE ROUTING
# ====================================================

if page == "🏠 Dashboard":

    st.subheader("🔄 Government Data")

    st.caption(
        f"📅 Last Updated : {datetime.now().strftime('%Y-%m-%d • %I:%M %p')}"
    )

    st.caption(
        "After downloading the latest government CSV into data/incoming/, click below."
    )

    if st.button("Update Government Data", use_container_width=True):

        with st.spinner("Updating database and retraining model..."):

            result = subprocess.run(
                ["python", "scripts/update_pipeline.py"],
                capture_output=True,
                text=True
            )

        if result.returncode == 0:

            st.cache_data.clear()

            st.success("✅ Government data updated successfully!")

            st.toast("Latest government data loaded!", icon="🌾")

            st.rerun()

        else:

            st.error("❌ Update failed")

            st.code(result.stderr)

    st.divider()
    # ----------------------------------------------------
    # KPI ROW
    # ----------------------------------------------------

    k1, k2, k3, k4 = st.columns(4)

    with k1:
        st.metric(" Current Price", rupees(current_price))

    with k2:
        st.metric(
            " Predicted Price",
            rupees(predicted_price)
        )

    with k3:
        st.metric("📈 Average Price", rupees(avg_price))

    with k4:
        st.metric("📦 Records", f"{records:,}")

    st.write("")

    # ----------------------------------------------------
    # RECOMMENDATION SECTION
    # ----------------------------------------------------

    left, right = st.columns([2, 1])

    # Recommendation based on predicted price
    if percent > 5:
        recommendation = "HOLD"
    elif percent >= -5:
        recommendation = "MONITOR"
    else:
        recommendation = "SELL NOW"

    with left:

        st.subheader("🤖 AI Recommendation")
        st.caption("AI recommendation based on predicted future market price.")

        badge_for_recommendation(recommendation)

        st.write("")

        mini_gauges([
            ("Price Trend", trend["trend_score"], MAX_TREND_SCORE, status_color(trend["status_30"])),
            ("Seasonality Pattern", seasonality["seasonality_score"], MAX_SEASONALITY_SCORE, status_color(seasonality["seasonality_status"])),
            ("Price Stability", volatility["volatility_score"], MAX_VOLATILITY_SCORE, status_color(volatility["volatility_status"])),
        ])

    with right:

        st.subheader("📊 Market Analysis Score")
        st.caption("Calculated using historical price trend, seasonal pattern and price stability.")

        total_score_gauge(
            advisory["total_score"],
            MAX_TOTAL_SCORE,
            height=200
        )

        render_score_bar(
            "Price Trend",
            advisory["trend_score"],
            MAX_TREND_SCORE,
            BLUE
        )

        render_score_bar(
            "Seasonal Pattern",
            advisory["seasonality_score"],
            MAX_SEASONALITY_SCORE,
            CYAN
        )

        render_score_bar(
            "Price Stability",
            advisory["volatility_score"],
            MAX_VOLATILITY_SCORE,
            TEAL
        )

    st.divider()
    # ----------------------------------------------------
    # CHARTS
    # ----------------------------------------------------

    st.subheader("📈 Market Analytics")

    # ----------------------------------------------------
    # PRICE TREND
    # ----------------------------------------------------

    chart1, chart2 = st.columns(2)

    with chart1:
        price_trend_chart(filtered)

    # ----------------------------------------------------
    # MONTHLY AVERAGE
    # ----------------------------------------------------

    with chart2:
        monthly_average_chart(filtered)

    st.caption("🌾 Smart Farmer Advisory System • AI + Machine Learning + Data Analytics")

# ====================================================
# PREDICTION PAGE
# ====================================================

elif page == "🔮 Prediction":

    c1, c2 = st.columns(2)

    with c1:
        st.metric("Current Market Price", rupees(current_price))

        if prediction_type == "Historical":
            st.info("Showing historical government market price.")
            st.metric(
                "📜 Historical Price",
                rupees(predicted_price)
            )
        else:
            st.success("Showing AI predicted future price.")
            st.metric(
                "🤖 Predicted Price",
                rupees(predicted_price)
            )

    with c2:
        change = predicted_price - current_price

        if current_price != 0:
            percent = (change / current_price) * 100
        else:
            percent = 0

        st.metric(
            "Expected Change",
            f"{percent:.2f}%",
            f"₹{change:.2f}"
        )

        if percent > 5:
            st.success("🟢 BUY")
        elif percent >= -5:
            st.warning("🟡 HOLD")
        else:
            st.error("🔴 WAIT")

    st.divider()

    st.subheader("Prediction Reason")

    mini_gauges([
        ("Price Trend", trend["trend_score"], MAX_TREND_SCORE, status_color(trend["status_30"])),
        ("Seasonal Pattern", seasonality["seasonality_score"], MAX_SEASONALITY_SCORE, status_color(seasonality["seasonality_status"])),
        ("Price Stability", volatility["volatility_score"], MAX_VOLATILITY_SCORE, status_color(volatility["volatility_status"])),
    ])

    r1, r2, r3 = st.columns(3)

    r1.metric("Trend", trend["status_30"])
    r2.metric("Seasonality", seasonality["seasonality_status"])
    r3.metric("Volatility", volatility["volatility_status"])

# ====================================================
# ANALYTICS PAGE
# ====================================================

elif page == "📊 Analytics":

    c1, c2 = st.columns(2)

    with c1:
        price_trend_chart(filtered)

    with c2:
        monthly_average_chart(filtered)

    st.write("")

    c3, c4 = st.columns(2)

    with c3:

        score_df = pd.DataFrame({
            "Category": [
                "Trend",
                "Seasonality",
                "Volatility"
            ],
            "Score": [
                advisory["trend_score"],
                advisory["seasonality_score"],
                advisory["volatility_score"]
            ]
        })

        fig = px.pie(
            score_df,
            names="Category",
            values="Score",
            hole=.6,
            color="Category",
            color_discrete_map={
                "Trend": BLUE,
                "Seasonality": CYAN,
                "Volatility": TEAL
            }
        )

        fig.update_traces(
            textfont=dict(color="#e7ecff", size=13),
            marker=dict(line=dict(color="#0a0e27", width=2))
        )

        fig.update_layout(
            template="plotly_dark",
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins, sans-serif", color="#8b93b8"),
            legend=dict(bgcolor="rgba(0,0,0,0)")
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with c4:

        fig = px.histogram(
            filtered,
            x="Modal_Price",
            nbins=30
        )

        fig.update_traces(
            marker=dict(color=CYAN, line=dict(width=0)),
            marker_cornerradius=6
        )

        fig.update_layout(
            template="plotly_dark",
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Poppins, sans-serif", color="#8b93b8")
        )

        fig.update_yaxes(gridcolor="rgba(148,163,184,0.10)")
        fig.update_xaxes(showgrid=False)

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    st.write("")

    year_df = filtered.copy()

    year_df["Year"] = year_df["Arrival_Date"].dt.year

    year_df = (
        year_df
        .groupby("Year")["Modal_Price"]
        .mean()
        .reset_index()
    )

    fig = px.area(
        year_df,
        x="Year",
        y="Modal_Price"
    )

    fig.update_traces(
        line=dict(color=TEAL, width=3),
        fillcolor="rgba(45,212,191,0.15)"
    )

    fig.update_layout(
        template="plotly_dark",
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins, sans-serif", color="#8b93b8")
    )

    fig.update_yaxes(gridcolor="rgba(148,163,184,0.10)")
    fig.update_xaxes(showgrid=False)

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# ====================================================
# RECORDS PAGE
# ====================================================

elif page == "📋 Records":

    table = (
        filtered
        .sort_values(
            "Arrival_Date",
            ascending=False
        )
        .head(100)
    )

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

    csv = table.to_csv(index=False).encode()

    st.download_button(
        "⬇ Download CSV",
        csv,
        "market_records.csv",
        "text/csv"
    )

# ====================================================
# ABOUT PAGE
# ====================================================

elif page == "ℹ About":

    st.title("📘 Project Overview")
    st.caption("Smart Farmer Advisory System - AI Powered Agricultural Market Intelligence")

    st.markdown("---")

    st.subheader("🎯 Objective")

    st.write("""
The Smart Farmer Advisory System is designed to help farmers make better selling
decisions by combining Artificial Intelligence with historical market analysis.

Instead of relying only on today's market price, the system predicts future prices
and analyzes historical market behaviour to provide a smarter recommendation.
""")

    st.markdown("---")

    st.subheader("⚙️ How It Works")

    st.markdown("""
1. Government Agmarknet market data is collected.
2. Data is cleaned and stored in a SQLite database.
3. A Random Forest machine learning model predicts future prices.
4. Historical market analytics calculate:
   - Price Trend
   - Seasonal Pattern
   - Price Stability
5. The system generates an AI recommendation:
   - HOLD
   - MONITOR
   - SELL NOW
""")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🧠 AI Modules")

        st.markdown("""
- Future Price Prediction
- AI Recommendation
- Historical Market Analysis
- Interactive Dashboard
""")

    with col2:

        st.subheader("🛠 Technologies Used")

        st.markdown("""
- Python
- Streamlit
- Pandas
- Plotly
- SQLite
- Scikit-Learn
- Random Forest
- Joblib
""")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("📂 Dataset")

        st.write("""
**Source**

Government of India

Agmarknet Agricultural Market Dataset

Historical commodity price data used for
machine learning and market analysis.
""")

    with col2:

        st.subheader("🎓 Project Information")

        st.write("""
Academic Machine Learning Project

B.Tech CSE (Artificial Intelligence)

Developed as a Smart Farmer Decision Support System.
""")

    st.markdown("---")

    st.info(
        "This system combines AI-based future price prediction with historical "
        "market analytics to help farmers make more informed selling decisions."
    )