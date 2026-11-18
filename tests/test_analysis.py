"""
tests/test_analysis.py
Analytical Formulas & Statistical Methodology Test Suite
Tests KPI calculations, Z-scores, Tukey IQR fences, HHI, and MoM growth on tiny known golden fixtures.
Compatible with both pytest and python -m unittest.
"""

import unittest
import numpy as np

def calculate_net_cash_flow(inflows: float, outflows: float) -> float:
    return round(float(inflows - outflows), 2)

def calculate_credit_utilization(active_balance: float, credit_limit: float) -> float:
    if credit_limit <= 0.0:
        return 0.0
    return round((active_balance / credit_limit) * 100.0, 2)

def calculate_z_score(val: float, mean: float, std: float) -> float:
    if std <= 0.0:
        return 0.0
    return round((val - mean) / std, 2)

def calculate_iqr_bounds(values: list) -> tuple:
    arr = np.array(values, dtype=float)
    q25, q75 = np.percentile(arr, 25), np.percentile(arr, 75)
    iqr = q75 - q25
    lower_bound = q25 - 1.5 * iqr
    upper_bound = q75 + 1.5 * iqr
    return round(float(lower_bound), 2), round(float(upper_bound), 2)

def calculate_hhi(shares: list) -> float:
    """Herfindahl-Hirschman Index: sum of squared market share percentages."""
    return round(float(sum((s ** 2) for s in shares)), 2)

def calculate_mom_growth(current_spend: float, prior_spend: float) -> float:
    if prior_spend <= 0.0:
        return 0.0
    return round(((current_spend - prior_spend) / prior_spend) * 100.0, 2)

class TestAnalyticalFormulas(unittest.TestCase):
    def test_tc_t_06_net_cash_flow(self):
        """TC-T-06: Verify Net Cash Flow calculation on tiny known golden fixture."""
        inflows = 14250000.00
        outflows = 11825000.00
        expected_net = 2425000.00
        actual_net = calculate_net_cash_flow(inflows, outflows)
        self.assertEqual(actual_net, expected_net, "Net cash flow calculation mismatch")

    def test_tc_t_07_credit_utilization(self):
        """TC-T-07: Verify Credit Card Utilization formula across boundary conditions."""
        # Case 1: Standard usage (Safe Zone <70%)
        self.assertEqual(calculate_credit_utilization(1200000.0, 2500000.0), 48.00)
        # Case 2: Warning boundary (70%)
        self.assertEqual(calculate_credit_utilization(1750000.0, 2500000.0), 70.00)
        # Case 3: Critical boundary (>=85%)
        self.assertEqual(calculate_credit_utilization(2125000.0, 2500000.0), 85.00)
        # Case 4: Zero division guard
        self.assertEqual(calculate_credit_utilization(50000.0, 0.0), 0.0)

    def test_tc_t_08_z_score_calculation(self):
        """TC-T-08: Verify Parametric Z-Score computation."""
        # Mean = 1000, Std = 200
        # Value = 1700 => Z = (1700 - 1000) / 200 = 3.50 (Anomaly)
        self.assertEqual(calculate_z_score(1700.0, 1000.0, 200.0), 3.50)
        # Value = 1000 => Z = 0.00
        self.assertEqual(calculate_z_score(1000.0, 1000.0, 200.0), 0.00)

    def test_tc_t_09_iqr_bounds_calculation(self):
        """TC-T-09: Verify Non-parametric Tukey IQR fences."""
        # Sample dataset: [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        # Q25 = 32.5, Q75 = 77.5, IQR = 45.0
        # Upper Bound = 77.5 + 1.5 * 45.0 = 145.0
        # Lower Bound = 32.5 - 1.5 * 45.0 = -35.0
        data = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        lb, ub = calculate_iqr_bounds(data)
        self.assertEqual(lb, -35.0)
        self.assertEqual(ub, 145.0)

    def test_tc_t_10_hhi_concentration(self):
        """TC-T-10: Verify Herfindahl-Hirschman Index (HHI) for vendor market concentration."""
        # Two equal vendors with 50% share each: HHI = 50^2 + 50^2 = 5000 (Highly Concentrated)
        self.assertEqual(calculate_hhi([50.0, 50.0]), 5000.0)
        # Four equal vendors with 25% share each: HHI = 4 * 25^2 = 2500 (Moderate)
        self.assertEqual(calculate_hhi([25.0, 25.0, 25.0, 25.0]), 2500.0)

    def test_tc_t_11_mom_growth(self):
        """TC-T-11: Verify Month-over-Month percentage growth calculation."""
        # Prior = 100, Current = 125 => Growth = +25.0%
        self.assertEqual(calculate_mom_growth(125.0, 100.0), 25.00)
        # Prior = 100, Current = 80 => Delta = -20.0%
        self.assertEqual(calculate_mom_growth(80.0, 100.0), -20.00)
        # Prior = 0 (Zero division guard)
        self.assertEqual(calculate_mom_growth(100.0, 0.0), 0.0)

if __name__ == "__main__":
    unittest.main()
