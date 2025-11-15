"""Generate a monthly expenses report keyed by month (YYYY-MM).

Output structure example:
{
  "report_name": "monthly_expenses_report",
  "last_updated": "2025-11-15",
  "2025-10": {
    "total": "2302.59",
    "per_category": [ {"category":"Shopping","total":"653.98"}, ... ]
  },
  "2025-09": { ... }
}
"""

import json
import sqlite3
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "expense_tracker" / "db" / "expenses.db"
OUT_PATH = BASE_DIR / "expense_tracker" / "resources" / "monthly_expenses_report.json"

# SQL helpers
ALL_MONTHS_SQL = (
    "SELECT DISTINCT strftime('%Y-%m', date) AS month "
    "FROM tbl_expenses "
    "ORDER BY month DESC"
)
TOTAL_FOR_MONTH_SQL = (
    "SELECT COALESCE(SUM(amount), 0) FROM tbl_expenses WHERE strftime('%Y-%m', date)=?"
)
PER_CATEGORY_SQL = (
    "SELECT category, COALESCE(SUM(amount), 0) as total "
    "FROM tbl_expenses "
    "WHERE strftime('%Y-%m', date)=? "
    "GROUP BY category "
    "ORDER BY total DESC"
)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute(ALL_MONTHS_SQL)
months = [r[0] for r in cursor.fetchall()]
now = date.today().isoformat()

output = {
    "report_name": "monthly_expenses_report",
    "last_updated": now,
}

for m in months:
    # total for the month
    cursor.execute(TOTAL_FOR_MONTH_SQL, (m,))
    total = float(cursor.fetchone()[0] or 0)

    # per-category totals ordered desc (include ALL categories)
    cursor.execute(PER_CATEGORY_SQL, (m,))
    per_category_rows = cursor.fetchall()

    # Format totals as strings with exactly two decimal places
    per_category = [
        {"category": row[0], "total": f"{float(row[1]):.2f}"}
        for row in per_category_rows
    ]

    month_block = {
        "total": f"{total:.2f}",
        "per_category": per_category,
    }

    output[m] = month_block

# Ensure output dir exists and write
OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2)

print(f"Wrote report to {OUT_PATH}")
print(json.dumps(output, indent=2))

conn.close()
