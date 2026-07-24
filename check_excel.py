import pandas as pd

df = pd.read_excel("data/companies.xlsx", header=None)

print(df.head(10))