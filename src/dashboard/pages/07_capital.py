import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from dashboard.utils.db import get_financial_table

st.title("💰 Capital Allocation")

df = get_financial_table()

company = st.selectbox(
    "Company",
    sorted(df["company_id"].unique())
)

data = df[df.company_id == company].sort_values("year")

fig = px.bar(
    data,
    x="year",
    y=[
        "free_cash_flow_cr",
        "capex_cr",
        "cash_from_operations_cr"
    ],
    barmode="group"
)

st.plotly_chart(fig, width="stretch")