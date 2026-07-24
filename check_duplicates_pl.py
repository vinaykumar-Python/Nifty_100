import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

pl = pd.read_sql("SELECT company_id, year FROM profit_loss", conn)

dup = (
    pl.groupby(["company_id", "year"])
      .size()
      .reset_index(name="count")
)

print(dup[dup["count"] > 1])

conn.close()
