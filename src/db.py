"""
src/db.py
Database connection manager for SQLite.
Enforces Write-Ahead Logging (WAL) and foreign key referential integrity.
"""

import os
import sqlite3
from typing import Optional

DEFAULT_DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "app.db")

def get_db_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """
    Establish and return a connection to the SQLite database.
    Enforces foreign key checks and safe journal mode for cloud deployment.
    """
    path = db_path or DEFAULT_DB_PATH
    if not os.path.exists(path):
        # Auto-initialize database if missing
        try:
            from src.generate_data import (
                generate_accounts,
                generate_categories,
                generate_departments,
                generate_merchants,
                generate_transactions,
                init_sqlite_db
            )
            accs = generate_accounts()
            cats = generate_categories()
            deps = generate_departments()
            merchs = generate_merchants()
            txns = generate_transactions(accs, cats, deps, merchs, target_count=300)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            init_sqlite_db(accs, cats, deps, merchs, txns)
        except Exception:
            pass

    if not os.path.exists(path):
        raise FileNotFoundError(f"Database file not found at: {path}")

    conn = sqlite3.connect(path, timeout=15.0)
    try:
        conn.execute("PRAGMA foreign_keys = ON;")
    except Exception:
        pass
    try:
        conn.execute("PRAGMA journal_mode = WAL;")
    except Exception:
        pass
    conn.row_factory = sqlite3.Row
    return conn
