import sqlite3
import pandas as pd
import numpy as np
import os
conn = sqlite3.connect("db/nifty100.db")
profit = pd.read_sql(
    "SELECT * FROM profit_loss",
    conn
)

print(profit.head())
profit.columns = profit.iloc[0]

profit = profit.iloc[1:]

profit.reset_index(
    drop=True,
    inplace=True
)

print(profit.head())

numeric_columns = [
    "sales",
    "net_profit",
    "eps"
]

for col in numeric_columns:

    profit[col] = pd.to_numeric(
        profit[col],
        errors="coerce"
    )

print(profit.dtypes)

profit = profit[
    profit["year"] != "TTM"
]

profit["year_num"] = (
    profit["year"]
    .str.extract(r"(\d{4})")
)

profit["year_num"] = pd.to_numeric(
    profit["year_num"]
)

print(
    profit[
        [
            "year",
            "year_num"
        ]
    ].head()
)

# -------------------------------------
# CAGR Function
# -------------------------------------

def calculate_cagr(start_value, end_value, years):

    if pd.isna(start_value) or pd.isna(end_value):
        return None, "INSUFFICIENT"
    if years <= 0:
        return None, "INVALID_PERIOD"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    cagr = (
        (end_value / start_value) ** (1 / years) - 1
    ) * 100

    return float(round(cagr,2)), "NORMAL"

profit["revenue_cagr_3yr"] = None
profit["revenue_cagr_3yr_flag"] = None

companies = profit["company_id"].unique()

print("Total Companies:", len(companies))


def generate_cagr(df, column_name, years, output_name):

    df[f"{output_name}_{years}yr"] = None
    df[f"{output_name}_{years}yr_flag"] = None

    companies = df["company_id"].unique()

    print(f"\nCalculating {output_name.upper()} {years} Year CAGR...")

    for company in companies:

        company_data = df[
    df["company_id"] == company
].sort_values("year_num")
        for index, row in company_data.iterrows():

            current_year = row["year_num"]

            previous = company_data[
                company_data["year_num"] == current_year - years
            ]

            if previous.empty:

                df.loc[index, f"{output_name}_{years}yr"] = None
                df.loc[index, f"{output_name}_{years}yr_flag"] = "INSUFFICIENT"

            else:

                start_value = previous.iloc[0][column_name]
                end_value = row[column_name]

                cagr, flag = calculate_cagr(
                    start_value,
                    end_value,
                    years
                )

                df.loc[index, f"{output_name}_{years}yr"] = cagr
                df.loc[index, f"{output_name}_{years}yr_flag"] = flag

    print(f"{output_name.upper()} {years} Year CAGR Completed")

    #---

generate_cagr(
    profit,
    "sales",
    3,
    "revenue_cagr"
)

generate_cagr(
    profit,
    "sales",
    5,
    "revenue_cagr"
)

generate_cagr(
    profit,
    "sales",
    10,
    "revenue_cagr"
)
generate_cagr(
    profit,
    "net_profit",
    3,
    "pat_cagr"
)

generate_cagr(
    profit,
    "net_profit",
    5,
    "pat_cagr"
)

generate_cagr(
    profit,
    "net_profit",
    10,
    "pat_cagr"
)
generate_cagr(
    profit,
    "eps",
    3,
    "eps_cagr"
)

generate_cagr(
    profit,
    "eps",
    5,
    "eps_cagr"
)

generate_cagr(
    profit,
    "eps",
    10,
    "eps_cagr"
)




print(
    profit[
        [
            "company_id",
            "year",
            "sales",
            "revenue_cagr_3yr",
            "revenue_cagr_3yr_flag",
            "pat_cagr_3yr",
            "pat_cagr_3yr_flag",
            "eps_cagr_3yr",
            "eps_cagr_3yr_flag"
        ]
    ].head(30)
)
os.makedirs("outputs", exist_ok=True)

profit.to_csv(
    "outputs/day10_cagr.csv",
    index=False
)

print("\nDay 10 CSV Saved Successfully")



