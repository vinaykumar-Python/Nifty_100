import sqlite3

conn = sqlite3.connect("db/nifty100.db")

conn.execute("""
CREATE TABLE IF NOT EXISTS portfolio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_id TEXT,
    quantity INTEGER,
    buy_price REAL,
    buy_date TEXT
)
""")

conn.commit()

print("Portfolio table created successfully!")

conn.close()