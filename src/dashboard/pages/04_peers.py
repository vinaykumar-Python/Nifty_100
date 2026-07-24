import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.utils.db import (
    get_financial_table,
    get_peer_groups,
    get_peers
)

st.title("🤝 Peer Comparison")

financial = get_financial_table()

peer_groups = get_peer_groups()

# Handle either a full table or a distinct list
if "peer_group_name" in peer_groups.columns:
    groups = sorted(peer_groups["peer_group_name"].dropna().unique())
else:
    groups = sorted(peer_groups.iloc[:, 0].dropna().unique())

selected_group = st.selectbox(
    "Peer Group",
    groups
)

peers = get_peers(selected_group)

peer_ids = peers["company_id"].unique()

latest = (
    financial[
        financial["company_id"].isin(peer_ids)
    ]
    .sort_values("year")
    .groupby("company_id")
    .tail(1)
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

fig = px.bar(
    latest,
    x="company_id",
    y=metric,
    color="company_id",
    text_auto=".2f"
)

st.plotly_chart(fig, width="stretch")

st.dataframe(latest, width="stretch")