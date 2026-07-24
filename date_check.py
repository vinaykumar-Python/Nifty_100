import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql("""
SELECT MIN(date) start_date,
MAX(date) end_date
FROM stock_prices
""", conn)

print(df)