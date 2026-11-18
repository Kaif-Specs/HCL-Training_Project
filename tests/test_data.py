"""
tests/test_data.py
Database and Data Layer Integrity Test Suite
Verifies: SQLite existence, row counts, PK uniqueness, FK referential integrity, domain constraints.
Compatible with both pytest and python -m unittest.
"""

import os
import sqlite3
import unittest

DB_PATH = os.path.join(r"d:\HCL_Project", "data", "app.db")

class TestDatabaseIntegrity(unittest.TestCase):
    def setUp(self):
        self.assertTrue(os.path.exists(DB_PATH), f"Database file not found at {DB_PATH}")
        self.conn = sqlite3.connect(DB_PATH)
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.conn.close()

    def test_tc_t_01_sqlite_connection(self):
        """TC-T-01: Verify SQLite connection and readable schema."""
        self.cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [r[0] for r in self.cur.fetchall()]
        expected_tables = ["dim_accounts", "dim_categories", "dim_departments", "dim_merchants", "fact_transactions"]
        for t in expected_tables:
            self.assertIn(t, tables, f"Expected table '{t}' missing from database")

    def test_tc_t_02_row_counts(self):
        """TC-T-02: Verify expected row counts across dimensions and fact table."""
        expected_counts = {
            "dim_accounts": 8,
            "dim_categories": 8,
            "dim_departments": 5,
            "dim_merchants": 25
        }
        for table, expected_cnt in expected_counts.items():
            self.cur.execute(f"SELECT COUNT(*) FROM {table};")
            actual_cnt = self.cur.fetchone()[0]
            self.assertEqual(actual_cnt, expected_cnt, f"Table {table} row count mismatch")

        # Verify fact table has planned volume (>= 300 rows)
        self.cur.execute("SELECT COUNT(*) FROM fact_transactions;")
        fact_cnt = self.cur.fetchone()[0]
        self.assertGreaterEqual(fact_cnt, 300, f"fact_transactions has insufficient rows: {fact_cnt}")

        # Verify view has identical row count and 35 columns
        self.cur.execute("SELECT COUNT(*) FROM view_transaction_analysis;")
        view_cnt = self.cur.fetchone()[0]
        self.assertEqual(view_cnt, fact_cnt, "view_transaction_analysis row count must match fact_transactions")

    def test_tc_t_03_primary_key_uniqueness(self):
        """TC-T-03: Verify primary key uniqueness across all tables."""
        pk_map = {
            "dim_accounts": "account_id",
            "dim_categories": "category_id",
            "dim_departments": "department_id",
            "dim_merchants": "merchant_id",
            "fact_transactions": "transaction_id"
        }
        for table, pk_col in pk_map.items():
            self.cur.execute(f"SELECT COUNT({pk_col}), COUNT(DISTINCT {pk_col}) FROM {table};")
            total_cnt, distinct_cnt = self.cur.fetchone()
            self.assertEqual(total_cnt, distinct_cnt, f"Duplicate primary keys detected in {table}.{pk_col}")

    def test_tc_t_04_foreign_key_integrity(self):
        """TC-T-04: Verify foreign key referential integrity (zero orphan records)."""
        self.cur.execute("PRAGMA foreign_key_check;")
        fk_violations = self.cur.fetchall()
        self.assertEqual(len(fk_violations), 0, f"Foreign key integrity violations detected: {fk_violations}")

    def test_tc_t_05_domain_constraints(self):
        """TC-T-05: Verify non-negativity of amounts and valid categorical enums."""
        # Non-negative amounts
        self.cur.execute("SELECT COUNT(*) FROM fact_transactions WHERE amount <= 0.00;")
        non_pos_count = self.cur.fetchone()[0]
        self.assertEqual(non_pos_count, 0, "Non-positive transaction amounts found")

        # Valid transaction types
        self.cur.execute("SELECT DISTINCT transaction_type FROM fact_transactions;")
        types = {r[0] for r in self.cur.fetchall()}
        self.assertTrue(types.issubset({"Credit", "Debit"}), f"Invalid transaction_type found: {types}")

        # Valid statuses
        self.cur.execute("SELECT DISTINCT status FROM fact_transactions;")
        statuses = {r[0] for r in self.cur.fetchall()}
        self.assertTrue(statuses.issubset({"Success", "Failed", "Declined"}), f"Invalid status found: {statuses}")

if __name__ == "__main__":
    unittest.main()
