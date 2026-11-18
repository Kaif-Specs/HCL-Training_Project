"""
src/stats_engine.py
Statistical Anomaly Detection & Vendor Concentration Engine.
Implements Parametric Z-Score, Non-Parametric Tukey's Fences, and Pareto 80/20 algorithms.
"""

import numpy as np
import pandas as pd
from typing import Tuple, List, Dict, Any

def calculate_z_score(val: float, mean: float, std: float) -> float:
    """Computes standard Z-Score with zero standard deviation guard."""
    if std <= 0.0:
        return 0.0
    return round((val - mean) / std, 2)

def calculate_iqr_bounds(values: list, k: float = 1.5) -> Tuple[float, float]:
    """Computes Tukey IQR lower and upper fence thresholds."""
    if not values:
        return 0.0, 0.0
    arr = np.array(values, dtype=float)
    q25, q75 = np.percentile(arr, 25), np.percentile(arr, 75)
    iqr = q75 - q25
    lower_bound = q25 - (k * iqr)
    upper_bound = q75 + (k * iqr)
    return round(float(lower_bound), 2), round(float(upper_bound), 2)

def calculate_hhi(shares: List[float]) -> float:
    """Computes Herfindahl-Hirschman Index (HHI) for concentration assessment."""
    if not shares:
        return 0.0
    return round(float(sum((s ** 2) for s in shares)), 2)

def detect_outliers_zscore(df: pd.DataFrame, threshold: float = 3.0) -> pd.DataFrame:
    """
    Detects parametric statistical anomalies using Z-scores on Debit amounts.
    Flags records where |Z| > threshold.
    """
    if df.empty or "amount" not in df.columns:
        return df

    out = df.copy()
    debit_mask = out["transaction_type"] == "Debit"
    debit_amounts = out.loc[debit_mask, "amount"]

    if len(debit_amounts) > 1:
        mean_val = float(debit_amounts.mean())
        std_val = float(debit_amounts.std(ddof=1))
        if std_val > 0.0:
            out.loc[debit_mask, "z_score"] = ((out.loc[debit_mask, "amount"] - mean_val) / std_val).round(2)
        else:
            out.loc[debit_mask, "z_score"] = 0.0
    else:
        out["z_score"] = 0.0

    out["z_score"] = out["z_score"].fillna(0.0)
    out["is_outlier_z"] = out["z_score"].abs() > threshold
    return out

def detect_outliers_tukey(df: pd.DataFrame, k: float = 1.5) -> pd.DataFrame:
    """
    Detects non-parametric anomalies using Tukey's Fences (Q3 + k * IQR).
    """
    if df.empty or "amount" not in df.columns:
        return df

    out = df.copy()
    debit_mask = out["transaction_type"] == "Debit"
    debit_amounts = out.loc[debit_mask, "amount"].tolist()

    if len(debit_amounts) >= 4:
        lb, ub = calculate_iqr_bounds(debit_amounts, k=k)
        out["tukey_upper_bound"] = ub
        out["is_outlier_tukey"] = debit_mask & (out["amount"] > ub)
    else:
        out["tukey_upper_bound"] = 0.0
        out["is_outlier_tukey"] = False

    return out

def compute_vendor_pareto(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes Pareto analysis (80/20 distribution) for vendor disbursements.
    Returns vendors sorted by total spend with cumulative percentage curve.
    """
    if df.empty or "merchant_name" not in df.columns:
        return pd.DataFrame()

    debits = df[df["transaction_type"] == "Debit"]
    vendor_spend = debits.groupby(["merchant_id", "merchant_name"])["amount"].agg(
        Total_Spend="sum",
        Transaction_Count="count"
    ).reset_index()

    vendor_spend = vendor_spend.sort_values(by="Total_Spend", ascending=False).reset_index(drop=True)
    total_debit = vendor_spend["Total_Spend"].sum()

    if total_debit > 0:
        vendor_spend["Spend_Pct"] = (vendor_spend["Total_Spend"] / total_debit * 100.0).round(2)
        vendor_spend["Cumulative_Spend"] = vendor_spend["Total_Spend"].cumsum()
        vendor_spend["Cumulative_Pct"] = (vendor_spend["Cumulative_Spend"] / total_debit * 100.0).round(2)
    else:
        vendor_spend["Spend_Pct"] = 0.0
        vendor_spend["Cumulative_Spend"] = 0.0
        vendor_spend["Cumulative_Pct"] = 0.0

    return vendor_spend
