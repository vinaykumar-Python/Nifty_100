import pandas as pd

def calculate_quality_score(df):

    score = (
        df["return_on_equity_pct"].fillna(0) * 0.35 +
        df["net_profit_margin_pct"].fillna(0) * 0.20 +
        df["revenue_cagr_5yr"].fillna(0) * 0.20 +
        (100 - df["debt_to_equity"].fillna(0) * 20) * 0.15 +
        df["asset_turnover"].fillna(0) * 10 * 0.10
    )

    return score.round(2)


def recommendation(score):

    if score >= 40:
        return "🟢 Strong Buy"

    if score >= 30:
        return "🟢 Buy"

    if score >= 20:
        return "🟡 Hold"

    return "🔴 Avoid"