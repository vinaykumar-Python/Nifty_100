import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

sectors = pd.read_sql(
    "SELECT company_id,broad_sector FROM sectors",
    conn
)

conn.close()

financial_companies = sectors[
    sectors["broad_sector"] == "Financials"
]["company_id"]

ratios["high_leverage_flag"] = ratios.apply(
    lambda row:
    "Suppressed"
    if row["company_id"] in financial_companies.values
    else (
        "High"
        if row["debt_to_equity"] > 2
        else "Normal"
    ),
    axis=1
)

banks = ratios[
    ratios["company_id"].isin(financial_companies)
]

print(
    banks[
        [
            "company_id",
            "year",
            "debt_to_equity",
            "high_leverage_flag"
        ]
    ].head(50)
)