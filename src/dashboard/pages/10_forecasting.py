import streamlit as st
import plotly.express as px
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.utils.db import (
    get_profit_loss
)

from analytics.forecast import forecast_next_3_years

st.title("🤖 AI Forecasting")

pl = get_profit_loss()

company = st.selectbox(
    "Company",
    sorted(pl.company_id.unique())
)

metric = st.selectbox(
    "Forecast",
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
        markers=True,
        title=f"{company} {metric} Forecast"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.dataframe(
        forecast,
        use_container_width=True
    )
    