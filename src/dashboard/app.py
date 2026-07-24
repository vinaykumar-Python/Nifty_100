import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Nifty 100 Analytics Dashboard")

st.sidebar.title("Navigation")

page = st.sidebar.radio(
    "Go to",
    [
        "🏠 Home",
        "🏢 Company Profile",
        "🔍 Screener",
        "🤝 Peer Comparison",
        "📈 Trend Analysis",
        "🏭 Sector Analysis",
        "💰 Capital Allocation",
        "📄 Annual Reports"
    ]
)

if page == "🏠 Home":
    st.switch_page("pages/01_home.py")

elif page == "🏢 Company Profile":
    st.switch_page("pages/02_profile.py")

elif page == "🔍 Screener":
    st.switch_page("pages/03_screener.py")

elif page == "🤝 Peer Comparison":
    st.switch_page("pages/04_peers.py")

elif page == "📈 Trend Analysis":
    st.switch_page("pages/05_trends.py")

elif page == "🏭 Sector Analysis":
    st.switch_page("pages/06_sectors.py")

elif page == "💰 Capital Allocation":
    st.switch_page("pages/07_capital.py")

elif page == "📄 Annual Reports":
    st.switch_page("pages/08_reports.py")




    import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "db/nifty100.db"


@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)


@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM companies", conn)


@st.cache_data(ttl=600)
def get_ratios():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM financial_ratios", conn)


@st.cache_data(ttl=600)
def get_profit_loss():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM profit_loss", conn)


@st.cache_data(ttl=600)
def get_balance_sheet():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM balance_sheet", conn)


@st.cache_data(ttl=600)
def get_cash_flow():
    conn = get_connection()
    return pd.read_sql("SELECT * FROM cash_flow", conn)