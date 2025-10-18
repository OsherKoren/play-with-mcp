"""SQL query helpers for the expense tracker.

This module exposes async functions that run read queries against the
SQLite `expenses` table using the global `conn` provided by
`expense_tracker.resources.connection`.

Public functions:
- `select_total_expenses_for_month(month: int) -> float`
- `select_total_expenses_for_month_and_category(month: int, category: str) -> float`

Usage notes:
- Ensure `start_database()` from `connection` has been called before using
  these functions; they raise RuntimeError if the connection is not initialized.
"""

# !/usr/bin/env python

"""SQL queries for the expense tracker MCP server."""
import aiosqlite

from expense_tracker.resources.connection import conn


async def select_total_expenses_for_month(month: int) -> float:
    """Return the total expenses for a given month from the SQLite database."""
    assert conn, "Database connection is not initialized."
    async with conn:
        conn.row_factory = aiosqlite.Row
        month_str = f"{month:02d}"
        cursor = await conn.execute(
            """
            SELECT SUM(amount) as total
            FROM expenses
            WHERE strftime('%m', date) = ?;
            """,
            (month_str),
        )
        row = await cursor.fetchone()
        return row["total"] if row is not None else 0.0


async def select_total_expenses_for_month_and_category(
    month: int, category: str
) -> float:
    """Return the total expenses for a given month and category from the SQLite database."""
    assert conn, "Database connection is not initialized."
    async with conn:
        conn.row_factory = aiosqlite.Row
        month_str = f"{month:02d}"
        cursor = await conn.execute(
            """
            SELECT SUM(amount) as total
            FROM expenses
            WHERE strftime('%m', date) = ? AND category = ?;
            """,
            (month_str, category),
        )
        row = await cursor.fetchone()
        return row["total"] if row is not None else 0.0
