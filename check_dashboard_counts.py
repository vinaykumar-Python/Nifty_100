import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = [
    "companies",
    "sectors",
    "financial_table",
    "market_cap"
]

for table in tables:
    print(f"\n{table}")
    df = pd.read_sql(f"SELECT COUNT(*) AS total FROM {table}", conn)
    print(df)