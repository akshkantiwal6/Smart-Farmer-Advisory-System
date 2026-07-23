import streamlit as st
from textwrap import dedent


# ==========================================================
# PAGE TITLE
# ==========================================================

def page_title(title, subtitle=""):
    st.markdown(
        dedent(f"""
        <div class="fade">
            <div class="dashboard-title">{title}</div>
            <div class="dashboard-subtitle">{subtitle}</div>
        </div>
        """),
        unsafe_allow_html=True
    )


# ==========================================================
# GLASS CARD
# ==========================================================

def glass_card(title, body):
    st.markdown(
        dedent(f"""
        <div class="glass fade">
            <h3>{title}</h3>
            <br>
            {body}
        </div>
        """),
        unsafe_allow_html=True
    )


# ==========================================================
# KPI CARD
# ==========================================================

def kpi_card(title, value, subtitle=""):
    st.markdown(
        dedent(f"""
        <div class="kpi-card fade">
            <div class="kpi-title">{title}</div>
            <div class="kpi-value">{value}</div>
            <div class="kpi-sub">{subtitle}</div>
        </div>
        """),
        unsafe_allow_html=True
    )


# ==========================================================
# BADGE
# ==========================================================

def badge(text, color="blue"):

    colors = {
        "green": "badge-green",
        "orange": "badge-orange",
        "red": "badge-red",
        "blue": "badge-blue"
    }

    cls = colors.get(color, "badge-blue")

    st.markdown(
        dedent(f"""
        <span class="badge {cls}">
            {text}
        </span>
        """),
        unsafe_allow_html=True
    )


# ==========================================================
# SECTION
# ==========================================================

def section(title, subtitle=""):
    st.markdown(
        dedent(f"""
        <div class="section-title">{title}</div>
        <div class="section-subtitle">{subtitle}</div>
        """),
        unsafe_allow_html=True
    )


# ==========================================================
# METRIC ROW
# ==========================================================

def metric_row(label1, value1, label2, value2):

    c1, c2 = st.columns(2)

    with c1:
        st.metric(label1, value1)

    with c2:
        st.metric(label2, value2)