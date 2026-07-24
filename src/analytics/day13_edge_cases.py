import sqlite3
import pandas as pd
import os
import os

print(os.path.abspath("db/nifty100.db"))

conn = sqlite3.connect("db/nifty100.db")

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

companies = pd.read_sql(
    """
    SELECT
        company_id,
        roe_percentage,
        roce_percentage
    FROM companies
    """,
    conn
)

conn.close()

# Latest year only
latest = ratios.sort_values("year").groupby("company_id").tail(1)

merged = latest.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

log_lines = []

for _, row in merged.iterrows():

    # ---------- ROE ----------
    try:
        roe_diff = abs(
            float(row["return_on_equity_pct"])
            -
            float(row["roe_percentage"])
        )

        if roe_diff > 5:

            log_lines.append(
                f"{row['company_id']} | ROE | "
                f"Calculated={row['return_on_equity_pct']:.2f} | "
                f"Source={row['roe_percentage']:.2f} | "
                f"Difference={roe_diff:.2f}% | "
                f"Category=Data Source Issue"
            )

    except:
        pass

    # ---------- ROCE ----------
    try:
        roce = row["operating_profit"] / (
            row["equity_capital"]
            +
            row["reserves"]
            +
            row["borrowings"]
        ) * 100

        roce_diff = abs(
            roce
            -
            float(row["roce_percentage"])
        )

        if roce_diff > 5:

            log_lines.append(
                f"{row['company_id']} | ROCE | "
                f"Calculated={roce:.2f} | "
                f"Source={row['roce_percentage']:.2f} | "
                f"Difference={roce_diff:.2f}% | "
                f"Category=Formula Difference"
            )

    except:
        pass

os.makedirs("output", exist_ok=True)

with open(
    "output/ratio_edge_cases.log",
    "w"
) as f:

    for line in log_lines:
        f.write(line + "\n")

print("Log created successfully")
print("Total anomalies:", len(log_lines))