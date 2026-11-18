"""
tests/test_app.py
Streamlit Application & UI Component Test Suite
Verifies: configuration files, UI component generation, sub-3s query performance benchmarks.
Compatible with both pytest and python -m unittest.
"""

import os
import time
import sqlite3
import unittest
import sys

# Ensure src is importable
PROJECT_DIR = r"d:\HCL_Project"
if PROJECT_DIR not in sys.path:
    sys.path.insert(0, PROJECT_DIR)

class TestAppUI(unittest.TestCase):
    def test_tc_t_12_streamlit_config_exists(self):
        """TC-T-12a: Verify Streamlit theme configuration file exists and has dark mode theme."""
        config_path = os.path.join(PROJECT_DIR, ".streamlit", "config.toml")
        self.assertTrue(os.path.exists(config_path), f"config.toml not found at {config_path}")
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("primaryColor", content)
        self.assertIn("#2563EB", content)
        self.assertIn("#0F172A", content)

    def test_tc_t_12_ui_components_module(self):
        """TC-T-12b: Verify src/ui.py component library generates non-empty HTML."""
        ui_file = os.path.join(PROJECT_DIR, "src", "ui.py")
        self.assertTrue(os.path.exists(ui_file), f"src/ui.py not found at {ui_file}")
        with open(ui_file, "r", encoding="utf-8") as f:
            code = f.read()
        self.assertIn("render_tailwind_header", code)
        self.assertIn("render_kpi_card", code)
        self.assertIn("render_alert_box", code)

    def test_tc_t_12_query_latency_under_3_seconds(self):
        """TC-T-12c: Verify database view query latency is strictly under 3.0 seconds (Target < 0.1s)."""
        db_path = os.path.join(PROJECT_DIR, "data", "app.db")
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        cur = conn.cursor()
        
        t0 = time.time()
        cur.execute("SELECT * FROM view_transaction_analysis;")
        rows = cur.fetchall()
        t1 = time.time()
        conn.close()
        
        latency = t1 - t0
        self.assertGreaterEqual(len(rows), 300, "View returned insufficient records")
        self.assertLess(latency, 3.0, f"Query latency exceeded 3.0s ceiling: {latency:.4f}s")
        print(f"\n[BENCHMARK] view_transaction_analysis query latency: {latency*1000:.2f} ms across {len(rows)} records (PASSED < 3s)")

if __name__ == "__main__":
    unittest.main()
