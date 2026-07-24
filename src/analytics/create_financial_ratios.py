import sqlite3
import pandas as pd
import numpy as np

conn = sqlite3.connect("db/nifty100.db")

pl = pd.read_sql("SELECT * FROM profit_loss", conn)
bs = pd.read_sql("SELECT * FROM balance_sheet", conn)
cf = pd.read_sql("SELECT * FROM cash_flow", conn)

# Remove duplicate company-year records
pl = pl.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

bs = bs.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

cf = cf.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

# Convert numeric columns
for df in [pl, bs, cf]:
    for col in df.columns:
        if col not in ["id", "company_id", "year"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")

# Merge all statements
financial = (
    pl.merge(bs, on=["company_id", "year"], how="inner")
      .merge(cf, on=["company_id", "year"], how="inner")
)

financial = financial.drop_duplicates(
    subset=["company_id", "year"],
    keep="first"
)

print("Final merged rows:", len(financial))


print("Merged rows :", len(financial))


print(financial.head())

# -------------------------
# PROFITABILITY RATIOS
# -------------------------

financial["net_profit_margin_pct"] = (
    financial["net_profit"] / financial["sales"]
) * 100

financial["operating_profit_margin_pct"] = (
    financial["operating_profit"] / financial["sales"]
) * 100

financial["return_on_equity_pct"] = (
    financial["net_profit"] /
    (financial["equity_capital"] + financial["reserves"])
) * 100


# -------------------------
# LEVERAGE RATIOS
# -------------------------

financial["debt_to_equity"] = (
    financial["borrowings"] /
    (financial["equity_capital"] + financial["reserves"])
)

financial["interest_coverage"] = (
    financial["operating_profit"] /
    financial["interest"]
)


# -------------------------
# EFFICIENCY
# -------------------------

financial["asset_turnover"] = (
    financial["sales"] /
    financial["total_assets"]
)


# -------------------------
# CASH FLOW
# -------------------------

financial["free_cash_flow_cr"] = (
    financial["operating_activity"] +
    financial["investing_activity"]
)

financial["capex_cr"] = abs(
    financial["investing_activity"]
)

financial["cash_from_operations_cr"] = (
    financial["operating_activity"]
)

financial["total_debt_cr"] = (
    financial["borrowings"]
)


# -------------------------
# SHAREHOLDER RATIOS
# -------------------------

financial["earnings_per_share"] = financial["eps"]

financial["book_value_per_share"] = (
    (financial["equity_capital"] + financial["reserves"])
    /
    financial["equity_capital"]
)

financial["dividend_payout_ratio_pct"] = (
    financial["dividend_payout"]
)


# -----------------------------------
# SORT DATA
# -----------------------------------

financial = financial.sort_values(
    ["company_id", "year"]
)

# -----------------------------------
# 5 YEAR REVENUE CAGR
# -----------------------------------

financial["revenue_cagr_5yr"] = (
    financial.groupby("company_id")["sales"]
    .transform(lambda x: ((x / x.shift(5)) ** (1/5) - 1) * 100)
)

# -----------------------------------
# 5 YEAR PAT CAGR
# -----------------------------------

financial["pat_cagr_5yr"] = (
    financial.groupby("company_id")["net_profit"]
    .transform(lambda x: ((x / x.shift(5)) ** (1/5) - 1) * 100)
)

# -----------------------------------
# 5 YEAR EPS CAGR
# -----------------------------------

financial["eps_cagr_5yr"] = (
    financial.groupby("company_id")["eps"]
    .transform(lambda x: ((x / x.shift(5)) ** (1/5) - 1) * 100)
)


financial["composite_quality_score"] = (
    financial[
        [
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "asset_turnover"
        ]
    ]
    .fillna(0)
    .mean(axis=1)
)
financial.to_sql(
    "financial_table",
    conn,
    if_exists="replace",
    index=False
)

financial[
    [
        "company_id",
        "year",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "capex_cr",
        "cash_from_operations_cr",
        "total_debt_cr",
        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",
        "revenue_cagr_5yr",
        "pat_cagr_5yr",
        "eps_cagr_5yr",
        "composite_quality_score"
    ]
].to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print("financial_table created successfully.")
print("financial_ratios updated successfully.")
print("Rows:", len(financial))





