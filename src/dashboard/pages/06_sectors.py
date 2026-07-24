import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from dashboard.utils.db import (
    get_financial_table,
    get_sectors
)

st.title("🏭 Sector Analysis")

financial = get_financial_table()
sectors = get_sectors()

df = financial.merge(
    sectors,
    on="company_id"
)

sector = st.selectbox(
    "Sector",
    sorted(df["broad_sector"].dropna().unique())
)

metric = st.selectbox(
    "Metric",
    [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "asset_turnover",
        "composite_quality_score"
    ]
)

result = (
    df[df["broad_sector"] == sector]
    .groupby("company_id")[metric]
    .mean()
    .reset_index()
)

fig = px.bar(
    result,
    x="company_id",
    y=metric,
    color=metric
)

st.plotly_chart(fig, width="stretch")