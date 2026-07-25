import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.append(str(ROOT / "src"))

from dashboard.utils.db import get_profit_loss

df = get_profit_loss()

print(df.columns.tolist())