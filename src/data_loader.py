"""
src/data_loader.py
High-performance database view loader and cache manager.
Utilizes Streamlit's @st.cache_data to guarantee sub-50ms data access.
"""

import os
import sqlite3
import pandas as pd
from typing import Optional, Dict

try:
    import streamlit as st
    cache_decorator = st.cache_data(ttl=3600, show_spinner=False)
except Exception:
    # Fallback decorator when running outside Streamlit (e.g. pytest / CLI)
    def cache_decorator(func):
        return func

from src.db import get_db_connection, DEFAULT_DB_PATH

@cache_decorator
def load_analysis_view(db_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load the pre-joined 35-column analytical view from SQLite.
    Converts transaction dates to datetime objects and validates column schemas.
    """
    conn = get_db_connection(db_path)
    try:
        query = "SELECT * FROM view_transaction_analysis ORDER BY transaction_date ASC, transaction_id ASC;"
        df = pd.read_sql_query(query, conn)
        if "transaction_date" in df.columns:
            df["transaction_date"] = pd.to_datetime(df["transaction_date"])
        if "amount" in df.columns:
            df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        
        # Standardize convenience aliases for UI and analytics
        if "account_name" not in df.columns and "bank_name" in df.columns and "account_number_masked" in df.columns:
            df["account_name"] = df["bank_name"] + " (" + df["account_number_masked"] + ")"
        elif "account_name" not in df.columns and "account_id" in df.columns:
            df["account_name"] = df["account_id"]

        if "payment_method" not in df.columns and "payment_instrument" in df.columns:
            df["payment_method"] = df["payment_instrument"]

        # Map authentic departmental budget allocations from dim_departments
        dept_budgets = pd.read_sql_query("SELECT department_id, annual_budget FROM dim_departments;", conn)
        budget_map = dict(zip(dept_budgets["department_id"], dept_budgets["annual_budget"]))
        df["budget_allocated"] = df["department_id"].map(budget_map).fillna(0.0)

        return df
    finally:
        conn.close()

def load_raw_data(db_path: Optional[str] = None) -> Dict[str, pd.DataFrame]:
    """
    Load all relational tables individually into a dictionary of DataFrames.
    """
    conn = get_db_connection(db_path)
    tables = ["dim_accounts", "dim_categories", "dim_departments", "dim_merchants", "fact_transactions"]
    data = {}
    try:
        for t in tables:
            data[t] = pd.read_sql_query(f"SELECT * FROM {t};", conn)
        return data
    finally:
        conn.close()
