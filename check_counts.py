import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "profit_loss",
    "balance_sheet",
    "cash_flow",
    "financial_ratios"
]

for table in tables:
    count = pd.read_sql(
        f"SELECT COUNT(*) AS total FROM {table}",
        conn
    )
    print(table)
    print(count)
    print()

conn.close()
