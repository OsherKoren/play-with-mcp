"""Setup script for initializing the database."""

import random
import sqlite3
from calendar import monthrange
from datetime import date, timedelta
from pathlib import Path

DB_PATH = Path("expense_tracker/resources/expenses.db")
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

# Connect to (or create) SQLite database
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Create the expenses table if it doesn’t exist
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL
)
"""
)

# Define sample categories and descriptions
categories = {
    "Food": ["Groceries", "Dinner", "Coffee", "Snacks"],
    "Transport": ["Bus ticket", "Taxi ride", "Fuel refill"],
    "Entertainment": ["Movie", "Streaming subscription", "Concert ticket"],
    "Utilities": ["Electric bill", "Water bill", "Internet plan"],
    "Health": ["Pharmacy", "Doctor visit", "Gym membership"],
    "Shopping": ["Clothes", "Electronics", "Books"],
}


def generate_expenses_for_month(year: int, month: int, count: int = 20):
    """Generate random expense entries for a given month."""

    start_date = date(year, month, 1)
    _, days_in_month = monthrange(year, month)

    data = []
    for _ in range(count):
        random_category = random.choice(list(categories.keys()))
        description = random.choice(categories[random_category])
        random_day = start_date + timedelta(days=random.randint(0, days_in_month - 1))
        amount = round(random.uniform(10, 250), 2)
        data.append((str(random_day), random_category, description, amount))
    return data


# Generate demo data for August, September, October 2025 (20 rows each)
demo_expenses = (
    generate_expenses_for_month(2025, 8)
    + generate_expenses_for_month(2025, 9)
    + generate_expenses_for_month(2025, 10)
)

# Insert demo data
cursor.executemany(
    """
INSERT INTO expenses (date, category, description, amount)
VALUES (?, ?, ?, ?)
""",
    demo_expenses,
)

conn.commit()

# Verify results (show first 10 rows)
print("✅ Demo 'expenses' table created successfully!\n")
for row in cursor.execute("SELECT * FROM expenses ORDER BY date LIMIT 10"):
    print(row)

conn.close()
