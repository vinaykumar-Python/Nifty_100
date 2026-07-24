import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

query = """
SELECT
    p.company_id,
    p.year
FROM profit_loss p
LEFT JOIN balance_sheet b
ON p.company_id=b.company_id
AND p.year=b.year
LEFT JOIN cash_flow c
ON p.company_id=c.company_id
AND p.year=c.year
WHERE
b.company_id IS NULL
OR c.company_id IS NULL
ORDER BY p.company_id,p.year;
"""

missing = pd.read_sql(query, conn)

print(missing)
print("\nTotal Missing:", len(missing))

conn.close()
