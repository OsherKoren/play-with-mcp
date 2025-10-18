"""Database connection helpers for the expense tracker.

This module manages the application's aiosqlite connection instance used by
other modules in `expense_tracker.resources`.

Public API
- `conn`: global aiosqlite.Connection | None — the live connection once started
- `start_database()` -> None — initialize `conn` (must be called before queries)
- `shutdown_database()` -> None — close `conn` when shutting down

Notes
- The SQLite file is located at `expense_tracker/resources/expenses.db`.
- Call `start_database()` during application startup and `shutdown_database()`
  during shutdown to manage the connection lifecycle.
"""

# !/usr/bin/env python

from pathlib import Path

import aiosqlite

from expense_tracker.logger import log

BASE_DIR = Path(__file__).parent.resolve()
DB_PATH = BASE_DIR / "expenses.db"
conn: aiosqlite.Connection | None = None


async def start_database() -> None:
    """Initialize the global asynchronous SQLite connection.

    This function opens an aiosqlite connection to the database file at
    `DB_PATH` and assigns it to the module-level `conn` variable. Call this
    during application startup before running any queries.

    Side effects:
    - Sets the module-level `conn` variable to an `aiosqlite.Connection`.
    - Logs a success message on initialization.

    Returns:
        None
    """
    global conn
    conn = await aiosqlite.connect(str(DB_PATH))
    log.success("Initialized the SQLite connection ".center(40))


async def shutdown_database():
    """Close the global SQLite connection if it is open and clear `conn`.

    If no connection is present, this function is a no-op. After closing the
    connection it sets the module-level `conn` to `None` and logs shutdown info.

    Returns:
        None
    """
    global conn
    if conn is None:
        return

    await conn.close()
    log.info(" Shutting Down Database connection".center(40))
    conn = None
