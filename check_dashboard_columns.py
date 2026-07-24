import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.append(str(ROOT / "src"))

from dashboard.utils.db import get_financial_table

df = get_financial_table()

print(df.columns.tolist())
print(df.head())
