import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

tables = pd.read_sql("""
SELECT name
FROM sqlite_master
WHERE type='table'
""", conn)

all_info=[]

for table in tables['name']:

    info = pd.read_sql(
        f"PRAGMA table_info({table})",
        conn
    )

    info['table_name']=table

    all_info.append(info)

dictionary=pd.concat(all_info)

dictionary.to_csv(
    "output/data_dictionary.csv",
    index=False
)

print("Exported Successfully")
