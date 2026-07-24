import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

print(pd.read_sql("PRAGMA table_info(financial_ratios)", conn))

print("\n")

print(pd.read_sql("""
SELECT company_id,
       year,
       debt_to_equity,
       interest_coverage,
       free_cash_flow_cr,
       composite_quality_score
FROM financial_ratios
LIMIT 10
""", conn))

conn.close()
