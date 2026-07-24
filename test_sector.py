import sqlite3
import pandas as pd
import os

db_path = os.path.abspath("db/nifty100.db")
print("DB:", db_path)

conn = sqlite3.connect(db_path)

print(pd.read_sql("PRAGMA table_info(sectors)", conn))
print()
print(pd.read_sql("SELECT * FROM sectors LIMIT 5", conn))