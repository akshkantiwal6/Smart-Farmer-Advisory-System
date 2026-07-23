import streamlit as st


def metric_card(title, value, icon="📊", change=None, color="#35F0A5"):
    """
    Professional KPI Card
    """

    change_html = ""

    if change:
        change_html = f"""
        <div style="
            margin-top:12px;
            color:{color};
            font-size:15px;
            font-weight:600;">
            {change}
        </div>
        """

    st.markdown(
        f"""
        <div style="
            background:linear-gradient(145deg,#242B56,#1D2346);
            border:1px solid rgba(255,255,255,.08);
            border-radius:20px;
            padding:24px;
            min-height:160px;
            box-shadow:0 12px 35px rgba(0,0,0,.35);
            transition:.3s;
        ">

            <div style="
                display:flex;
                justify-content:space-between;
                align-items:center;
            ">

                <div style="
                    color:#AAB7E8;
                    font-size:16px;
                    font-weight:500;">
                    {title}
                </div>

                <div style="
                    width:48px;
                    height:48px;
                    border-radius:50%;
                    background:rgba(55,216,255,.15);
                    display:flex;
                    align-items:center;
                    justify-content:center;
                    font-size:22px;">
                    {icon}
                </div>

            </div>

            <div style="
                margin-top:25px;
                font-size:42px;
                font-weight:700;
                color:white;
                line-height:1;">
                {value}
            </div>

            {change_html}

        </div>
        """,
        unsafe_allow_html=True
    )


def recommendation_card(title, recommendation, description):

    colors = {
        "BUY": "#35F0A5",
        "HOLD": "#FFD54F",
        "WAIT": "#FF5C7A"
    }

    color = colors.get(recommendation, "#35F0A5")

    st.markdown(
        f"""
        <div style="
            background:#242B56;
            border-left:6px solid {color};
            border-radius:20px;
            padding:25px;
            min-height:180px;
        ">

            <div style="
                color:#AAB7E8;
                font-size:18px;
                font-weight:600;">
                {title}
            </div>

            <div style="
                margin-top:15px;
                font-size:42px;
                color:{color};
                font-weight:800;">
                {recommendation}
            </div>

            <div style="
                margin-top:18px;
                color:#D8DEF7;
                font-size:16px;
                line-height:1.6;">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


def info_card(title, value):

    st.markdown(
        f"""
        <div style="
            background:#242B56;
            border-radius:18px;
            padding:20px;
            text-align:center;
            border:1px solid rgba(255,255,255,.08);
        ">

            <div style="
                color:#9FB2E3;
                font-size:15px;">
                {title}
            </div>

            <div style="
                margin-top:10px;
                color:white;
                font-size:30px;
                font-weight:700;">
                {value}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )