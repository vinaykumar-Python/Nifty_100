import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.append(str(ROOT / "src"))

from dashboard.utils.db import get_profit_loss

df = get_profit_loss()

print(df["company_id"].unique()[:10])

company = df[df["company_id"] == df["company_id"].iloc[0]]

print(company["year"])
print(company["year"].unique())
