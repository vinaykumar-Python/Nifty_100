import streamlit as st
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.utils.db import get_financial_table
from analytics.ai_stock_score import (
    calculate_quality_score,
    recommendation
)

st.title("🤖 AI Stock Recommendation")

df = get_financial_table()

latest = (
    df.sort_values("year")
      .groupby("company_id")
      .tail(1)
      .copy()
)

latest["quality_score"] = calculate_quality_score(latest)

latest["recommendation"] = latest["quality_score"].apply(recommendation)

st.dataframe(
    latest[
        [
            "company_id",
            "quality_score",
            "recommendation",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "revenue_cagr_5yr",
            "debt_to_equity"
        ]
    ].sort_values(
        "quality_score",
        ascending=False
    ),
    use_container_width=True
)