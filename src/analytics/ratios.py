import sqlite3
import numpy as np
import pandas as pd

# ==========================
# CONNECT TO DATABASE
# ==========================

conn = sqlite3.connect("db/nifty100.db")
# If your database is in the project root, use:
# conn = sqlite3.connect("nifty100.db")

# ==========================
# READ PROFIT & LOSS TABLE
# ==========================

profit = pd.read_sql("SELECT * FROM profit_loss", conn)

print("Before Cleaning")
print(profit.head())

# ==========================
# CLEAN HEADER
# ==========================

profit.columns = profit.iloc[0]
profit = profit.iloc[1:]
profit.reset_index(drop=True, inplace=True)

print("\nAfter Cleaning")
print(profit.head())

print("\nColumns")
print(profit.columns)

# ==========================
# CONVERT NUMERIC COLUMNS
# ==========================

numeric_columns = [
    "sales",
    "operating_profit",
    "opm_percentage",
    "other_income",
    "interest",
    "depreciation",
    "profit_before_tax",
    "tax_percentage",
    "net_profit",
    "eps",
    "dividend_payout"
]

for col in numeric_columns:
    profit[col] = pd.to_numeric(
        profit[col],
        errors="coerce"
    )

print("\nData Types")
print(profit.dtypes)

# ==========================
# NET PROFIT MARGIN
# ==========================

profit["net_profit_margin"] = profit.apply(
    lambda row:
    None
    if row["sales"] == 0
    else (row["net_profit"] / row["sales"]) * 100,
    axis=1
)

print("\nNet Profit Margin")

print(
    profit[
        [
            "company_id",
            "year",
            "sales",
            "net_profit",
            "net_profit_margin"
        ]
    ].head()
)

# ==========================
# OPERATING PROFIT MARGIN
# ==========================

profit["calculated_opm"] = profit.apply(
    lambda row:
    None
    if row["sales"] == 0
    else (row["operating_profit"] / row["sales"]) * 100,
    axis=1
)

print("\nOperating Profit Margin")

print(
    profit[
        [
            "company_id",
            "year",
            "operating_profit",
            "sales",
            "calculated_opm",
            "opm_percentage"
        ]
    ].head()
)

# ==========================
# OPM CROSS CHECK
# ==========================

print("\nChecking OPM Differences (>1%)")

mismatch = profit[
    abs(
        profit["calculated_opm"]
        -
        profit["opm_percentage"]
    ) > 1
]

print(mismatch[
    [
        "company_id",
        "year",
        "calculated_opm",
        "opm_percentage"
    ]
])



mismatch.to_csv(
    "output/opm_mismatch.csv",
    index=False
)

print("\nOPM mismatch saved.")

# ==========================
# CLOSE DATABASE
# ==========================
# ==========================
# READ BALANCE SHEET TABLE
# ==========================


# ==========================
# READ SECTORS
# ==========================

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

print("\nBefore Cleaning")
print(sectors.head())
print(sectors.columns)


# ==========================
# READ BALANCE SHEET
# ==========================

balance = pd.read_sql("SELECT * FROM balance_sheet", conn)

print("\n==============================")
print("BALANCE SHEET - BEFORE CLEANING")
print("==============================")
print(balance.head())

# First row becomes header
balance.columns = balance.iloc[0]

# Remove header row
balance = balance.iloc[1:]

# Reset index
balance.reset_index(drop=True, inplace=True)

print("\n==============================")
print("BALANCE SHEET - AFTER CLEANING")
print("==============================")
print(balance.head())

print("\n==============================")
print("BALANCE SHEET COLUMNS")
print("==============================")
print(balance.columns)

# ==========================
# CONVERT BALANCE SHEET COLUMNS
# ==========================

balance_numeric = [
    "equity_capital",
    "reserves",
    "borrowings",
    "other_liabilities",
    "total_liabilities",
    "fixed_assets",
    "cwip",
    "investments",
    "other_asset",
    "total_assets"
]

for col in balance_numeric:
    balance[col] = pd.to_numeric(balance[col], errors="coerce")





print("\nBalance Sheet Data Types")
print(balance.dtypes)
# ==========================
# MERGE TABLES
# ==========================

df = pd.merge(
    profit,
    balance,
    on=["company_id", "year"],
    how="inner"
)

print("\nMerged Data")
print(df.head())

df = pd.merge(
    df,
    sectors,
    on="company_id",
    how="left"
)
cashflow = pd.read_sql(
    "SELECT * FROM cash_flow",
    conn
)

cashflow.columns = cashflow.iloc[0]

cashflow = cashflow.iloc[1:]

cashflow.reset_index(
    drop=True,
    inplace=True
)
cash_numeric = [

    "operating_activity",

    "investing_activity",

    "financing_activity"

]

for col in cash_numeric:

    cashflow[col] = pd.to_numeric(

        cashflow[col],

        errors="coerce"

    )
    df = pd.merge(

    df,

    cashflow[

        [

            "company_id",

            "year",

            "operating_activity",

            "investing_activity",

            "financing_activity"

        ]

    ],

    on=["company_id","year"],

    how="left"

)
    

print(df.head())

# ==========================
# CONVERT MERGED DATA TO NUMERIC
# ==========================

numeric_cols = [
    "sales",
    "operating_profit",
    "other_income",
    "interest",
    "net_profit",
    "equity_capital",
    "reserves",
    "borrowings",
    "investments",
    "total_assets"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(
        df[col],
        errors="coerce"
    )

print("\nMerged Numeric Conversion Completed")

##ROE = Net Profit
 # ---------------------- ×100
# Equity Capital + Reserves

# ==========================
# RETURN ON EQUITY
# ==========================

df["return_on_equity_pct"] = df.apply(
    lambda row: None
    if (row["equity_capital"] + row["reserves"]) <= 0
    else (
        row["net_profit"] /
        (row["equity_capital"] + row["reserves"])
    ) * 100,
    axis=1
)

print("\nROE")
print(
    df[
        [
            "company_id",
            "year",
            "net_profit",
            "equity_capital",
            "reserves",
            "return_on_equity_pct"
        ]
    ].head()
)

# ==========================
# ROCE
# ==========================

df["ebit"] = (
    df["operating_profit"]
    +
    df["other_income"]
)

df["roce"] = df.apply(
    lambda row: None
    if (
        row["equity_capital"]
        +
        row["reserves"]
        +
        row["borrowings"]
    ) <= 0
    else (
        row["ebit"]
        /
        (
            row["equity_capital"]
            +
            row["reserves"]
            +
            row["borrowings"]
        )
    ) * 100,
    axis=1
)

print("\nROCE")

print(
    df[
        [
            "company_id",
            "year",
            "ebit",
            "borrowings",
            "roce"
        ]
    ].head()
)

# ==========================
# ROCE BENCHMARK
# ==========================

df["roce_benchmark"] = df.apply(
    lambda row:
    "Financial Sector Benchmark"
    if row["broad_sector"] == "Financials"
    else (
        "Good"
        if pd.notna(row["roce"]) and row["roce"] >= 15
        else "Needs Improvement"
    ),
    axis=1
)

print("\nROCE Benchmark")

print(
    df[
        [
            "company_id",
            "broad_sector",
            "roce",
            "roce_benchmark"
        ]
    ].head()
)

# ==========================
# ROA
# ==========================

# ==========================
# RETURN ON ASSETS
# ==========================

df["roa"] = df.apply(
    lambda row:
    None
    if row["total_assets"] <= 0
    else (
        row["net_profit"] /
        row["total_assets"]
    ) * 100,
    axis=1
)

print("\nROA")

print(
    df[
        [
            "company_id",
            "year",
            "roa"
        ]
    ].head()
)

df.rename(columns={
    "net_profit_margin": "net_profit_margin_pct",
    "calculated_opm": "operating_profit_margin_pct",
    "roce": "return_on_capital_employed_pct",
    "roa": "return_on_assets_pct"
}, inplace=True)

def new_func(df):
    profitability = new_func1(df)
    
    return profitability

def new_func1(df):
    profitability = df[
    [
        "company_id",
        "year",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "return_on_capital_employed_pct",
        "return_on_assets_pct"
    ]
]

    return profitability

profitability = new_func(df)

profitability.to_csv(
    "output/day08_profitability.csv",
    index=False
)

print("Day 08 CSV Saved")

# ==========================
# SAVE RESULT
# ==========================

# ===================================================
# DAY 09 - LEVERAGE & EFFICIENCY RATIOS
# ===================================================
# ==========================
# DEBT TO EQUITY RATIO
# ==========================

df["debt_to_equity"] = df.apply(
    lambda row: 0
    if row["borrowings"] == 0
    else (
        None
        if (row["equity_capital"] + row["reserves"]) <= 0
        else row["borrowings"] /
        (row["equity_capital"] + row["reserves"])
    ),
    axis=1
)

print("\nDebt To Equity")

print(
    df[
        [
            "company_id",
            "year",
            "borrowings",
            "equity_capital",
            "reserves",
            "debt_to_equity"
        ]
    ].head()
)

# ==========================
# INTEREST COVERAGE
# ==========================

df["interest_coverage"] = df.apply(
    lambda row:
    None
    if row["interest"] == 0
    else (
        (
            row["operating_profit"]
            +
            row["other_income"]
        )
        /
        row["interest"]
    ),
    axis=1
)

print(df[
    [
        "company_id",
        "interest",
        "interest_coverage"
    ]
].head())

# ==========================
# ICR WARNING
# ==========================

df["icr_warning"] = df["interest_coverage"].apply(
    lambda x:
    True
    if pd.notna(x) and x < 1.5
    else False
)

print("\nInterest Coverage Warning")

print(
    df[
        [
            "company_id",
            "interest_coverage",
            "icr_warning"
        ]
    ].head()
)

#Borrowings - Investments
# ==========================
# NET DEBT
# ==========================

df["net_debt"] = (
    df["borrowings"]
    -
    df["investments"]
)

print("\nNet Debt")

print(
    df[
        [
            "company_id",
            "borrowings",
            "investments",
            "net_debt"
        ]
    ].head()
)
#Sales / Total Assets
# ==========================
# ASSET TURNOVER
# ==========================

df["asset_turnover"] = df.apply(

    lambda row:

    None

    if row["total_assets"] == 0

    else row["sales"] / row["total_assets"],

    axis=1

)
df["free_cash_flow_cr"] = (

    df["operating_activity"]

    +

    df["investing_activity"]

)
df["capex_cr"] = abs(

    df["investing_activity"]

)
df["cash_from_operations_cr"] = (

    df["operating_activity"]

)
df["total_debt_cr"] = (

    df["borrowings"]

)
df["earnings_per_share"] = df["eps"]

df["book_value_per_share"] = np.where(

    df["equity_capital"]==0,

    None,

    (

        df["equity_capital"]

        +

        df["reserves"]

    )

    /

    df["equity_capital"]

)

df["dividend_payout_ratio_pct"] = (

    df["dividend_payout"]

)



print("\nAsset Turnover")

print(

    df[
        [
            "company_id",
            "sales",
            "total_assets",
            "asset_turnover"
        ]
    ].head()

)
# ==========================
# DEBT FREE LABEL
# ==========================

df["icr_label"] = df["interest"].apply(
    lambda x: "Debt Free" if x == 0 else ""
)

print("\nDebt Free Label")

print(
    df[
        [
            "company_id",
            "interest",
            "icr_label"
        ]
    ].head()
)


# ==========================
# HIGH LEVERAGE FLAG
# ==========================

df["high_leverage_flag"] = df.apply(
    lambda row:
    (
        row["debt_to_equity"] > 5
        and row["broad_sector"] != "Financials"
    )
    if pd.notna(row["debt_to_equity"])
    else False,
    axis=1
)

print("\nHigh Leverage")

print(
    df[
        [
            "company_id",
            "broad_sector",
            "debt_to_equity",
            "high_leverage_flag"
        ]
    ].head()
)

# ==========================
# FINANCIAL SECTOR CHECK
# ==========================

financial = df[
    df["broad_sector"] == "Financials"
]
financial.to_csv(
    "output/financial_sector_review.csv",
    index=False
)

print("\nFinancial Companies")

print(
    financial[
        [
            "company_id",
            "debt_to_equity",
            "high_leverage_flag"
        ]
    ].head()
)

df.rename(columns={

    "net_profit_margin": "net_profit_margin_pct",

    "calculated_opm": "operating_profit_margin_pct",

    "roce": "return_on_capital_employed_pct",

    "roa": "return_on_assets_pct"

}, inplace=True)

financial_ratios = df[

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

    "earnings_per_share",

    "book_value_per_share",

    "dividend_payout_ratio_pct",

    "total_debt_cr",

    "cash_from_operations_cr",

    "revenue_cagr_5yr",

    "pat_cagr_5yr",

    "eps_cagr_5yr",

    "composite_quality_score"

    ]

]

financial_ratios.to_csv(
    "output/day09_leverage_efficiency.csv",
    index=False
)

print("\nDatabase Connection Closed")
print("\nDay 09 Completed Successfully")


import os

os.makedirs("output", exist_ok=True)

print("\n==============================")
print("DAY 09 SUMMARY")
print("==============================")
print("Financial Companies :", len(financial))

print("Total Records :", len(df))

print("Debt Free Companies :", (df["icr_label"]=="Debt Free").sum())

print("High Leverage Companies :", df["high_leverage_flag"].sum())

print("Interest Warning Companies :", df["icr_warning"].sum())

cagr = pd.read_csv(

    "outputs/day10_cagr.csv"

)

df = pd.merge(

    df,

    cagr[

        [

            "company_id",

            "year",

            "revenue_cagr_5yr",

            "pat_cagr_5yr",

            "eps_cagr_5yr"

        ]

    ],

    on=[

        "company_id",

        "year"

    ],

    how="left"

)

columns = [

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
"earnings_per_share",
"book_value_per_share",
"dividend_payout_ratio_pct",
"total_debt_cr",
"cash_from_operations_cr",
"revenue_cagr_5yr",
"pat_cagr_5yr",
"eps_cagr_5yr",
"composite_quality_score"

]

financial_ratios = df[columns]

financial_ratios.to_sql(

    "financial_ratios",

    conn,

    if_exists="replace",

    index=False

)

print("financial_ratios table updated")

count = pd.read_sql(

    "SELECT COUNT(*) AS rows FROM financial_ratios",

    conn

)

print(count)
conn.close()