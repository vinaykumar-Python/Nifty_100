import sqlite3

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS companies(
symbol TEXT,
company_name TEXT,
sector TEXT
)
""")

conn.commit()
conn.close()

print("Database created successfully")
