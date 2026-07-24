import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

cf = pd.read_sql("SELECT company_id, year FROM cash_flow", conn)

dup = (
    cf.groupby(["company_id", "year"])
      .size()
      .reset_index(name="count")
)

dup = dup[dup["count"] > 1]

print(dup)

conn.close()
