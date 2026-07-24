import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = pd.read_sql("""
SELECT name
FROM sqlite_master
WHERE type='table'
""", conn)

for table in tables['name']:

    df = pd.read_sql(f"SELECT * FROM {table}", conn)

    dup = df.duplicated().sum()

    print(f"{table} -> Duplicates = {dup}")

conn.close()