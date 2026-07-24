import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.utils.db import (
    get_companies,
    get_financial_table,
    get_marketcap,
    get_company_pros,
    get_documents,
    get_company_sector
)

st.title("🏢 Company Analysis")

companies = get_companies()
financial = get_financial_table()
market = get_marketcap()

company = st.selectbox(
    "Select Company",
    sorted(companies["company_name"].unique())
)

info = companies[
    companies.company_name == company
].iloc[0]

company_id = info["company_name"]

sector = get_company_sector(company_id)
pros = get_company_pros(company_id)
docs = get_documents(company_id)

st.header(company)

c1, c2 = st.columns([1,2])

with c1:

    if str(info["company_logo"]) != "nan":
        st.image(info["company_logo"], width=150)

with c2:

    st.subheader(company)

    st.write(info["about_company"])

    st.link_button("🌐 Visit Website", info["website"])

st.divider()

k1,k2,k3,k4 = st.columns(4)

k1.metric(
    "ROE",
    f"{info['roe_percentage']}%"
)

k2.metric(
    "ROCE",
    f"{info['roce_percentage']}%"
)

k3.metric(
    "Book Value",
    info["book_value"]
)

k4.metric(
    "Face Value",
    info["face_value"]
)

st.divider()

latest = (
    financial[
        financial.company_id == company_id
    ]
    .sort_values("year")
)

if not latest.empty:

    st.subheader("Financial Ratios")

    latest_ratio = latest.tail(1)

    st.dataframe(latest_ratio, width="stretch")

    metrics = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "free_cash_flow_cr"
    ]

    chart = latest[
        ["year"] + metrics
    ].melt(
        id_vars="year",
        var_name="Metric",
        value_name="Value"
    )

    fig = px.line(
        chart,
        x="year",
        y="Value",
        color="Metric",
        markers=True
    )

    st.plotly_chart(fig, width="stretch")

latest_market = (
    market[
        market.company_id == company_id
    ]
    .sort_values("year", ascending=True)
)   

if not latest_market.empty:

    st.subheader("Market Valuation")

    latest_market = latest_market.tail(1)

    st.dataframe(latest_market, width="stretch")

if not pros.empty:

    st.subheader("Pros")

    for p in pros["pros"].dropna():
        st.markdown(f"✅ {p}")

    st.subheader("Cons")

    for c in pros["cons"].dropna():
        st.markdown(f"❌ {c}")


if not docs.empty:

    st.subheader("Annual Reports")

    for _, row in docs.iterrows():
        st.link_button(
            f"{row['Year']} Annual Report",
            row["Annual_Report"]
        )