"""
src/analytics.py
Core Financial Analytics Engine for Credit vs Debit Analysis.
Implements executive KPI formulas, category breakdowns, departmental utilization, and monthly rollups.
"""

import pandas as pd
import numpy as np
from typing import Dict, Any

def calculate_net_cash_flow(inflows: float, outflows: float) -> float:
    """Computes Net Cash Flow = Inflows (Credit) - Outflows (Debit)."""
    return round(float(inflows - outflows), 2)

def calculate_credit_utilization(active_balance: float, credit_limit: float) -> float:
    """Computes credit limit utilization percentage with zero-division safety."""
    if credit_limit <= 0.0:
        return 0.0
    return round(float((active_balance / credit_limit) * 100.0), 2)

def calculate_mom_growth(current_spend: float, prior_spend: float) -> float:
    """Computes Month-over-Month percentage spend growth."""
    if prior_spend <= 0.0:
        return 0.0
    return round(float(((current_spend - prior_spend) / prior_spend) * 100.0), 2)

def compute_executive_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Computes top-level executive financial metrics:
    - Gross Inflow (Credit)
    - Gross Outflow (Debit)
    - Net Cash Flow (Inflow - Outflow)
    - Outflow to Inflow Ratio (Debit / Credit %)
    - Total Volume & Average Ticket Size
    """
    if df.empty:
        return {
            "total_credit": 0.0,
            "total_debit": 0.0,
            "net_cash_flow": 0.0,
            "outflow_ratio": 0.0,
            "transaction_count": 0,
            "avg_transaction_val": 0.0,
            "credit_count": 0,
            "debit_count": 0
        }

    credit_mask = df["transaction_type"] == "Credit"
    debit_mask = df["transaction_type"] == "Debit"

    total_credit = float(df.loc[credit_mask, "amount"].sum())
    total_debit = float(df.loc[debit_mask, "amount"].sum())
    net_flow = calculate_net_cash_flow(total_credit, total_debit)
    outflow_ratio = round((total_debit / total_credit * 100.0), 2) if total_credit > 0 else 0.0

    return {
        "total_credit": round(total_credit, 2),
        "total_debit": round(total_debit, 2),
        "net_cash_flow": net_flow,
        "outflow_ratio": outflow_ratio,
        "transaction_count": len(df),
        "avg_transaction_val": round(float(df["amount"].mean()), 2),
        "credit_count": int(credit_mask.sum()),
        "debit_count": int(debit_mask.sum())
    }

def compute_category_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregates spend and inflow by financial category.
    """
    if df.empty or "category_name" not in df.columns:
        return pd.DataFrame()

    grouped = df.groupby(["category_name", "transaction_type"])["amount"].agg(
        Total_Amount="sum",
        Transaction_Count="count"
    ).reset_index()

    total_debit = df.loc[df["transaction_type"] == "Debit", "amount"].sum()
    if total_debit > 0:
        grouped["Debit_Share_Pct"] = grouped.apply(
            lambda r: round((r["Total_Amount"] / total_debit * 100.0), 2) if r["transaction_type"] == "Debit" else 0.0,
            axis=1
        )
    else:
        grouped["Debit_Share_Pct"] = 0.0

    return grouped.sort_values(by="Total_Amount", ascending=False).reset_index(drop=True)

def compute_account_balances(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarizes liquidity and transaction volume by account.
    """
    if df.empty or "account_name" not in df.columns:
        return pd.DataFrame()

    pivot = df.pivot_table(
        index=["account_id", "account_name", "account_type", "bank_name"],
        columns="transaction_type",
        values="amount",
        aggfunc="sum",
        fill_value=0.0
    ).reset_index()

    if "Credit" not in pivot.columns:
        pivot["Credit"] = 0.0
    if "Debit" not in pivot.columns:
        pivot["Debit"] = 0.0

    pivot["Net_Movement"] = pivot["Credit"] - pivot["Debit"]
    return pivot.sort_values(by="Net_Movement", ascending=False).reset_index(drop=True)

def compute_monthly_trends(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes monthly temporal cash flow aggregates and 30-day moving averages.
    """
    if df.empty or "transaction_date" not in df.columns:
        return pd.DataFrame()

    temp = df.copy()
    temp["YearMonth"] = temp["transaction_date"].dt.to_period("M").astype(str)

    monthly = temp.pivot_table(
        index="YearMonth",
        columns="transaction_type",
        values="amount",
        aggfunc="sum",
        fill_value=0.0
    ).reset_index()

    if "Credit" not in monthly.columns:
        monthly["Credit"] = 0.0
    if "Debit" not in monthly.columns:
        monthly["Debit"] = 0.0

    monthly["Net_Cash_Flow"] = monthly["Credit"] - monthly["Debit"]
    monthly["Cumulative_Net"] = monthly["Net_Cash_Flow"].cumsum()
    monthly["Debit_30d_MA"] = monthly["Debit"].rolling(window=2, min_periods=1).mean()

    return monthly.sort_values(by="YearMonth").reset_index(drop=True)

def compute_department_spend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Evaluates departmental operational expenditures against assigned quarterly budgets.
    """
    if df.empty or "department_name" not in df.columns:
        return pd.DataFrame()

    debit_df = df[df["transaction_type"] == "Debit"]
    dept_agg = debit_df.groupby("department_name")["amount"].agg(Actual_Spend="sum").reset_index()

    # Merge budget info if available
    if "budget_allocated" in df.columns:
        budgets = df.groupby("department_name")["budget_allocated"].first().reset_index()
        dept_agg = pd.merge(dept_agg, budgets, on="department_name", how="left")
    else:
        dept_agg["budget_allocated"] = 0.0

    dept_agg["Variance"] = dept_agg["budget_allocated"] - dept_agg["Actual_Spend"]
    dept_agg["Utilization_Pct"] = dept_agg.apply(
        lambda r: round((r["Actual_Spend"] / r["budget_allocated"] * 100.0), 2) if r["budget_allocated"] > 0 else 0.0,
        axis=1
    )

    return dept_agg.sort_values(by="Actual_Spend", ascending=False).reset_index(drop=True)
