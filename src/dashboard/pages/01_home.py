
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
    
import streamlit as st
import plotly.express as px



from dashboard.utils.db import (
    get_companies,
    get_financial_table,
    get_marketcap,
    get_sectors
)

st.title("🏠 Nifty 100 Analytics Dashboard")

# -----------------------
# Load Data
# -----------------------

companies = get_companies()
financial = get_financial_table()
marketcap = get_marketcap()
sectors = get_sectors()

# -----------------------
# Sidebar
# -----------------------

years = sorted(financial["year"].dropna().unique(), reverse=True)

selected_year = st.sidebar.selectbox(
    "Select Financial Year",
    years
)

financial = financial[
    financial["year"] == selected_year
]

marketcap = marketcap[
    marketcap["year"] == selected_year
]

# -----------------------
# KPIs
# -----------------------

avg_roe = financial["return_on_equity_pct"].mean()

median_de = financial["debt_to_equity"].median()

median_revenue = financial["revenue_cagr_5yr"].median()

debt_free = (
    financial["debt_to_equity"] == 0
).sum()

median_pe = marketcap["pe_ratio"].median()

companies_count = companies.shape[0]

c1,c2,c3,c4,c5,c6 = st.columns(6)

c1.metric(
    "Average ROE",
    f"{avg_roe:.2f}%"
)

c2.metric(
    "Median P/E",
    f"{median_pe:.2f}"
)

c3.metric(
    "Median D/E",
    f"{median_de:.2f}"
)

c4.metric(
    "Companies",
    companies_count
)

c5.metric(
    "Revenue CAGR",
    f"{median_revenue:.2f}%"
)

c6.metric(
    "Debt Free",
    debt_free
)

st.divider()

# -----------------------
# Charts
# -----------------------

left,right = st.columns(2)

with left:

    st.subheader("Sector Distribution")

    sector_count = (
        sectors.groupby("broad_sector")
        .size()
        .reset_index(name="Companies")
    )

    fig = px.pie(
        sector_count,
        names="broad_sector",
        values="Companies",
        hole=.55
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

with right:

    st.subheader("🏆 Top 10 AI Recommended Companies")

top = (
    financial[
        [
            "company_id",
            "quality_score",
            "recommendation",
            "return_on_equity_pct",
            "revenue_cagr_5yr"
        ]
    ]
    .sort_values("quality_score", ascending=False)
    .head(10)
)

st.dataframe(top, width="stretch")