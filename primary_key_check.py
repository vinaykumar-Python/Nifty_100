import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = pd.read_sql("""
SELECT name
FROM sqlite_master
WHERE type='table'
""", conn)

for table in tables['name']:

    info = pd.read_sql(
        f"PRAGMA table_info({table})",
        conn
    )

    print("\n", table)
    print(info[['name','pk']])