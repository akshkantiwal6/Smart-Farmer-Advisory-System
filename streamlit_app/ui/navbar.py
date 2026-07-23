import streamlit as st


def navbar(
    commodity,
    state,
    district,
    market
):
    """
    Professional Top Navigation Bar
    """

    st.markdown(
        f"""
        <style>

        .top-navbar{{
            width:100%;
            height:80px;

            background:linear-gradient(
                90deg,
                #242B56,
                #1D2346
            );

            border:1px solid rgba(255,255,255,.08);

            border-radius:20px;

            display:flex;

            justify-content:space-between;

            align-items:center;

            padding:0 28px;

            margin-bottom:25px;

            box-shadow:
            0 10px 35px rgba(0,0,0,.35);
        }}

        .nav-left{{
            display:flex;
            align-items:center;
            gap:18px;
        }}

        .logo-circle{{
            width:55px;
            height:55px;

            border-radius:50%;

            background:linear-gradient(
                135deg,
                #35F0A5,
                #37D8FF
            );

            display:flex;
            justify-content:center;
            align-items:center;

            font-size:28px;

            box-shadow:
            0 0 20px rgba(55,216,255,.35);
        }}

        .project-title{{
            color:white;
            font-size:24px;
            font-weight:700;
        }}

        .project-subtitle{{
            color:#9FB2E3;
            font-size:14px;
            margin-top:3px;
        }}

        .nav-right{{
            display:flex;
            align-items:center;
            gap:12px;
        }}

        .pill{{
            background:#2C356A;

            color:white;

            padding:10px 18px;

            border-radius:999px;

            font-size:14px;

            border:1px solid rgba(255,255,255,.08);
        }}

        .status{{
            background:#35F0A5;

            width:10px;
            height:10px;

            border-radius:50%;

            display:inline-block;

            margin-right:8px;
        }}

        </style>

        <div class="top-navbar">

            <div class="nav-left">

                <div class="logo-circle">
                    🌾
                </div>

                <div>

                    <div class="project-title">
                        Smart Farmer Advisory System
                    </div>

                    <div class="project-subtitle">
                        AI Powered Agricultural Market Intelligence
                    </div>

                </div>

            </div>

            <div class="nav-right">

                <div class="pill">
                    🌾 {commodity}
                </div>

                <div class="pill">
                    📍 {state}
                </div>

                <div class="pill">
                    🏙 {district}
                </div>

                <div class="pill">
                    🏪 {market}
                </div>

                <div class="pill">
                    <span class="status"></span>
                    LIVE
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )