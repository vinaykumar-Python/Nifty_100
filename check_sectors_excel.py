import pandas as pd

df = pd.read_excel(
    "data/sectors.xlsx",
    header=None
)

print(df.head(10))
