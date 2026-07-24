import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM sectors LIMIT 10",
    conn
)

print(df.columns.tolist())
print(df.head())

conn.close()
