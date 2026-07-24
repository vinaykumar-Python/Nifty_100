import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.utils.db import (
    get_companies,
    get_portfolio,
    add_portfolio
)

st.title("💼 Portfolio Tracker")

companies = get_companies()

with st.form("portfolio"):

    company = st.selectbox(
        "Company",
        sorted(companies["company_name"].unique())
    )

    qty = st.number_input(
        "Quantity",
        min_value=1
    )

    price = st.number_input(
        "Buy Price",
        min_value=1.0
    )

    date = st.date_input("Purchase Date")

    submit = st.form_submit_button("Add Investment")

if submit:

    add_portfolio(
        company,
        qty,
        price,
        str(date)
    )

    st.success("Investment Added")

portfolio = get_portfolio()

if not portfolio.empty:

    portfolio["Investment"] = (
        portfolio["quantity"] *
        portfolio["buy_price"]
    )

    st.dataframe(
        portfolio,
        width="stretch"
    )

    st.metric(
        "Total Investment",
        f"₹{portfolio['Investment'].sum():,.2f}"
    )