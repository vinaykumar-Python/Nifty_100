import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from dashboard.utils.db import (
    get_profit_loss,
    get_financial_table
)

st.title("📈 Trend Analysis")

pl = get_profit_loss()
ratios = get_financial_table()

df = pl.merge(
    ratios,
    on=["company_id", "year"],
    how="left"
)

companies = sorted(df["company_id"].dropna().unique())

ticker = st.selectbox("Select Company", companies)

metrics = st.multiselect(
    "Select Metrics",
    [
        "sales",
        "net_profit",
        "return_on_equity_pct",
        "operating_profit_margin_pct",
        "free_cash_flow_cr",
        "debt_to_equity",
        "asset_turnover",
    ],
    default=["sales"]
)

company = df[df.company_id == ticker].sort_values("year")
latest = company.iloc[-1]

c1, c2 = st.columns(2)

c1.metric(
    "AI Quality Score",
    f"{latest['quality_score']:.1f}"
)

c2.metric(
    "Recommendation",
    latest["recommendation"]
)

if metrics:
    plot_df = company[["year"] + metrics].melt(
        id_vars="year",
        var_name="Metric",
        value_name="Value"
    )

    fig = px.line(
        plot_df,
        x="year",
        y="Value",
        color="Metric",
        markers=True,
        title=f"{ticker} Financial Trends"
    )

    st.plotly_chart(fig, width="stretch")
