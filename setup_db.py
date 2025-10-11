"""Setup script for initializing the database."""

import sqlite3
from datetime import date, timedelta
import random

# Connect to (or create) SQLite database
conn = sqlite3.connect("expense_tracker_mcp_server/resources/expenses.db")
cursor = conn.cursor()

# Drop table if it exists
cursor.execute("DROP TABLE IF EXISTS expenses")

# Create the expenses table
cursor.execute("""
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    category TEXT NOT NULL,
    description TEXT,
    amount REAL NOT NULL
)
""")

# Define sample categories and descriptions
categories = {
    "Food": ["Groceries", "Dinner", "Coffee", "Snacks"],
    "Transport": ["Bus ticket", "Taxi ride", "Fuel refill"],
    "Entertainment": ["Movie", "Streaming subscription", "Concert ticket"],
    "Utilities": ["Electric bill", "Water bill", "Internet plan"],
    "Health": ["Pharmacy", "Doctor visit", "Gym membership"],
    "Shopping": ["Clothes", "Electronics", "Books"]
}

# Generate 20 demo expenses for October 2025
start_date = date(2025, 10, 1)
demo_expenses = []

for i in range(20):
    random_category = random.choice(list(categories.keys()))
    description = random.choice(categories[random_category])
    random_day = start_date + timedelta(days=random.randint(0, 29))
    amount = round(random.uniform(10, 250), 2)

    demo_expenses.append(
        (str(random_day), random_category, description, amount)
    )

# Insert demo data
cursor.executemany("""
INSERT INTO expenses (date, category, description, amount)
VALUES (?, ?, ?, ?)
""", demo_expenses)

conn.commit()

# Verify results
print("✅ Demo 'expenses' table created successfully!\n")
print("Inserted rows:")
for row in cursor.execute("SELECT * FROM expenses ORDER BY date"):
    print(row)

conn.close()
