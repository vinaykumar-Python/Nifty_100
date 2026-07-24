import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

print("\n===== COMPANIES =====")
companies = pd.read_sql("SELECT * FROM companies LIMIT 5", conn)
print(companies.columns.tolist())

print("\n===== FINANCIAL RATIOS =====")
ratios = pd.read_sql("SELECT * FROM financial_ratios LIMIT 5", conn)
print(ratios.columns.tolist())