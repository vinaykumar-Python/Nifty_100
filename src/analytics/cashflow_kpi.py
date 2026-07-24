import sqlite3
import pandas as pd
import numpy as np
import os

conn = sqlite3.connect("db/nifty100.db")

cashflow = pd.read_sql(
    "SELECT * FROM cash_flow",
    conn
)

cashflow.columns = cashflow.iloc[0]

cashflow = cashflow.iloc[1:]

cashflow.reset_index(
    drop=True,
    inplace=True
)
print(cashflow.head())


numeric_columns = [
    "operating_activity",
    "investing_activity",
    "financing_activity",
    "sales",
    "operating_profit",
    "net_profit"
]

for col in numeric_columns:

    cashflow[col] = pd.to_numeric(
        cashflow[col],
        errors="coerce"
    )

cashflow = cashflow[
    cashflow["year"] != "TTM"
]

cashflow["year_num"] = (
    cashflow["year"]
    .str.extract(r"(\d{4})")
)

cashflow["year_num"] = pd.to_numeric(
    cashflow["year_num"]
)

cashflow["free_cash_flow"] = (
    cashflow["operating_activity"]
    +
    cashflow["investing_activity"]
)


cashflow["cfo_pat_ratio"] = np.where(

    (cashflow["net_profit"] == 0) |

    (cashflow["net_profit"].isna()),

    None,

    cashflow["operating_activity"] /

    cashflow["net_profit"]

)

cashflow = cashflow.sort_values(

    ["company_id", "year_num"]

)

cashflow["cfo_quality_score"] = (

    cashflow

    .groupby("company_id")["cfo_pat_ratio"]

    .transform(

        lambda x: x.rolling(5).mean()

    )

)
def classify_cfo_quality(score):

    if pd.isna(score):
        return None

    if score > 1:
        return "High Quality"

    elif score >= 0.5:
        return "Moderate"

    else:
        return "Accrual Risk"


cashflow["cfo_quality"] = (

    cashflow["cfo_quality_score"]

    .apply(classify_cfo_quality)

)
cashflow["capex_intensity"] = (

    abs(cashflow["investing_activity"])

    /

    cashflow["sales"]

) * 100
def classify_capex(x):

    if pd.isna(x):
        return None

    if x < 3:
        return "Asset Light"

    elif x <= 8:
        return "Moderate"

    else:
        return "Capital Intensive"


cashflow["capex_label"] = (

    cashflow["capex_intensity"]

    .apply(classify_capex)

)
cashflow["fcf_conversion"] = np.where(

    (cashflow["operating_profit"] == 0)

    |

    (cashflow["operating_profit"].isna()),

    None,

    (

        cashflow["free_cash_flow"]

        /

        cashflow["operating_profit"]

    ) * 100

)

def sign(x):

    if x > 0:
        return "+"

    elif x < 0:
        return "-"

    else:
        return "0"


cashflow["cfo_sign"] = cashflow["operating_activity"].apply(sign)

cashflow["cfi_sign"] = cashflow["investing_activity"].apply(sign)

cashflow["cff_sign"] = cashflow["financing_activity"].apply(sign)
def capital_pattern(cfo, cfi, cff, quality):

    pattern = (cfo, cfi, cff)

    if pattern == ("+", "-", "-"):

        if quality == "High Quality":

            return "Shareholder Returns"

        return "Reinvestor"

    elif pattern == ("+", "+", "-"):

        return "Liquidating Assets"

    elif pattern == ("-", "+", "+"):

        return "Distress Signal"

    elif pattern == ("-", "-", "+"):

        return "Growth Funded by Debt"

    elif pattern == ("+", "+", "+"):

        return "Cash Accumulator"

    elif pattern == ("-", "-", "-"):

        return "Pre-Revenue"

    elif pattern == ("+", "-", "+"):

        return "Mixed"

    else:

        return "Other"


cashflow["pattern_label"] = cashflow.apply(

    lambda row:

    capital_pattern(

        row["cfo_sign"],

        row["cfi_sign"],

        row["cff_sign"],

        row["cfo_quality"]

    ),

    axis=1

)
output = cashflow[
[
    "company_id",
    "year",
    "free_cash_flow",
    "cfo_pat_ratio",
    "cfo_quality_score",
    "cfo_quality",
    "capex_intensity",
    "capex_label",
    "fcf_conversion",
    "cfo_sign",
    "cfi_sign",
    "cff_sign",
    "pattern_label"
]
]
os.makedirs(
    "outputs",
    exist_ok=True
)

output.to_csv(
    "outputs/capital_allocation.csv",
    index=False
)
print(

    output.head(30)

)
print(cashflow.columns.tolist())
