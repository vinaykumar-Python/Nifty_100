import streamlit as st
import plotly.express as px
import pandas as pd
from sklearn.linear_model import LinearRegression
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.utils.db import get_profit_loss


def forecast_next_3_years(df, metric):

    df = df[["year", metric]].copy()

    # remove TTM
    df = df[~df["year"].astype(str).str.contains("TTM", na=False)]

    # keep only year number
    df["year"] = (
        df["year"]
        .astype(str)
        .str.extract(r"(\d{4})")[0]
    )

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df[metric] = pd.to_numeric(df[metric], errors="coerce")

    df = df.dropna()

    if len(df) < 3:
        return None

    df["year"] = df["year"].astype(int)

    X = df[["year"]]
    y = df[metric]

    model = LinearRegression()
    model.fit(X, y)

    future = pd.DataFrame({
        "year": [
            df["year"].max() + 1,
            df["year"].max() + 2,
            df["year"].max() + 3,
        ]
    })

    future[metric] = model.predict(future)

    history = df.copy()
    history["Type"] = "Historical"

    future["Type"] = "Forecast"

    result = pd.concat(
        [history, future],
        ignore_index=True
    )

    return result


st.title("🤖 AI Forecasting")

pl = get_profit_loss()

company = st.selectbox(
    "Company",
    sorted(pl.company_id.unique())
)

metric = st.selectbox(
    "Metric",
    [
        "sales",
        "net_profit",
        "operating_profit"
    ]
)

company_df = pl[
    pl.company_id == company
]

forecast = forecast_next_3_years(
    company_df,
    metric
)

if forecast is None:

    st.warning("Not enough historical data.")

else:

    fig = px.line(
        forecast,
        x="year",
        y=metric,
        color="Type",
        markers=True,
        title=f"{company} {metric} Forecast"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

    st.dataframe(
        forecast,
        width="stretch"
    )