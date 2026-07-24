import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("db/nifty100.db")

# Excel file mapping
files = {
    "companies": "data/companies.xlsx",
    "profit_loss": "data/profitandloss.xlsx",
    "balance_sheet": "data/balancesheet.xlsx",
    "cash_flow": "data/cashflow.xlsx",
    "ratios": "data/financial_ratios.xlsx",
    "stock_prices": "data/stock_prices.xlsx",
    "peer_comparison": "data/peer_groups.xlsx",
    "analysis": "data/analysis.xlsx",
    "documents": "data/documents.xlsx",
    "market_cap": "data/market_cap.xlsx",
    "pros_cons": "data/prosandcons.xlsx",
    "sectors": "data/sectors.xlsx"
}

# Load each Excel file into SQLite
for table_name, file in files.items():

    print(f"Loading {table_name}")

    try:

        # Files that contain a title row
        if table_name == "sectors":
            df = pd.read_excel(file)

        elif table_name in [
            "companies",
            "profit_loss",
            "balance_sheet",
            "cash_flow",
            "analysis",
            "documents",
            "pros_cons"
        ]:
            df = pd.read_excel(file, header=1)

        else:
            df = pd.read_excel(file)
  

        print(df.columns.tolist())

        df.to_sql(
            table_name,
            conn,
            if_exists="replace",
            index=False
        )

        print(f"{table_name} loaded successfully")

    except Exception as e:
        print(e)