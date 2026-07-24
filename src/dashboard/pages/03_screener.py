import streamlit as st
import pandas as pd
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.utils.db import get_screener_data

st.title("🔎 AI Stock Screener")

df = get_screener_data()

st.sidebar.header("Filters")

sector = st.sidebar.selectbox(
    "Sector",
    ["All"] + sorted(df["broad_sector"].dropna().unique().tolist())
)

roe = st.sidebar.slider(
    "Minimum ROE %",
    0,
    50,
    15
)

de = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    5.0,
    1.0
)

revenue = st.sidebar.slider(
    "Minimum Revenue CAGR %",
    -20,
    50,
    10
)

score = st.sidebar.slider(
    "Minimum Quality Score",
    0,
    100,
    40
)

if sector != "All":
    df = df[df["broad_sector"] == sector]

df = df[
    (df["return_on_equity_pct"] >= roe)
    &
    (df["debt_to_equity"] <= de)
    &
    (df["revenue_cagr_5yr"] >= revenue)
    &
    (df["composite_quality_score"] >= score)
]

st.success(f"{len(df)} Companies Found")

st.dataframe(
    df[
        [
            "company_name",
            "broad_sector",
            "return_on_equity_pct",
            "debt_to_equity",
            "revenue_cagr_5yr",
            "composite_quality_score"
        ]
    ].sort_values(
        "composite_quality_score",
        ascending=False
    ),
    width="stretch"
)