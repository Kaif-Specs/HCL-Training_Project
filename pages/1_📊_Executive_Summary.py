"""
pages/1_📊_Executive_Summary.py
Screen UI-01: Executive Summary & Corporate Liquidity Overview.
Features top-tier KPI cards, Cash Flow Waterfall, and Category Outflow Donut.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.data_loader import load_analysis_view
from src.cleaner import clean_transaction_data
from src.analytics import compute_executive_kpis, compute_category_breakdown
from src.ui import render_tailwind_header, render_kpi_card, render_alert_box, apply_chart_theme

st.set_page_config(page_title="Executive Summary | NexGen", page_icon="📊", layout="wide")

# Ensure session state has data
if "clean_df" not in st.session_state:
    raw_df = load_analysis_view()
    clean_df, audit_log = clean_transaction_data(raw_df)
    st.session_state["raw_df"] = raw_df
    st.session_state["clean_df"] = clean_df
    st.session_state["audit_log"] = audit_log

df = st.session_state["clean_df"]

render_tailwind_header(
    title="Executive Financial Summary & Liquidity KPI Cockpit",
    subtitle="Consolidated Cash Flow Health, Revenue Inflows vs Expenditure Outflows (Q1–Q3 2024)",
    badge_text="Screen UI-01"
)

# 1. Sidebar Global Filters
st.sidebar.header("🔍 Global Dashboard Filters")

min_date = df["transaction_date"].min().date()
max_date = df["transaction_date"].max().date()

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

all_accounts = sorted(df["account_name"].unique())
selected_accounts = st.sidebar.multiselect("Select Accounts", options=all_accounts, default=all_accounts)

all_depts = sorted(df["department_name"].unique())
selected_depts = st.sidebar.multiselect("Select Departments", options=all_depts, default=all_depts)

# Apply Filters
start_date = pd.to_datetime(selected_dates[0]) if isinstance(selected_dates, (tuple, list)) and len(selected_dates) > 0 else pd.to_datetime(min_date)
end_date = pd.to_datetime(selected_dates[1]) if isinstance(selected_dates, (tuple, list)) and len(selected_dates) > 1 else pd.to_datetime(max_date)

filtered_df = df[
    (df["transaction_date"] >= start_date) &
    (df["transaction_date"] <= end_date) &
    (df["account_name"].isin(selected_accounts)) &
    (df["department_name"].isin(selected_depts))
]

# Guard against empty filter selection
if filtered_df.empty:
    st.warning("⚠️ No transaction records match your selected filter criteria. Please broaden your selection.")
    st.stop()

# 2. Executive KPIs
kpis = compute_executive_kpis(filtered_df)

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Gross Inflows (Credit)", f"₹{kpis['total_credit']:,.2f}", f"{kpis['credit_count']} Inflow Transactions", status="positive")
with c2:
    render_kpi_card("Gross Outflows (Debit)", f"₹{kpis['total_debit']:,.2f}", f"{kpis['debit_count']} Outflow Transactions", status="negative")
with c3:
    net_status = "positive" if kpis['net_cash_flow'] >= 0 else "negative"
    render_kpi_card("Net Cash Flow", f"₹{kpis['net_cash_flow']:,.2f}", "Surplus Cash Position" if kpis['net_cash_flow'] >= 0 else "Deficit Cash Burn", status=net_status)
with c4:
    ratio_status = "positive" if kpis['outflow_ratio'] < 80 else ("warning" if kpis['outflow_ratio'] <= 100 else "negative")
    render_kpi_card("Outflow-to-Inflow Ratio", f"{kpis['outflow_ratio']:.1f}%", "Healthy Operating Margin" if kpis['outflow_ratio'] < 80 else "Elevated Expenditure", status=ratio_status)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# 3. Visual Charts Row: Cash Flow Waterfall & Category Donut
ch_col1, ch_col2 = st.columns([6, 4])

with ch_col1:
    st.subheader("💧 Cash Flow Movement Waterfall")
    waterfall_fig = go.Figure(go.Waterfall(
        name="Cash Flow Movement",
        orientation="v",
        measure=["relative", "relative", "total"],
        x=["Gross Credit Inflows", "Gross Debit Outflows", "Net Liquidity Position"],
        textposition="outside",
        text=[f"₹{kpis['total_credit']/1e5:.2f}L", f"-₹{kpis['total_debit']/1e5:.2f}L", f"₹{kpis['net_cash_flow']/1e5:.2f}L"],
        y=[kpis['total_credit'], -kpis['total_debit'], kpis['net_cash_flow']],
        connector={"line": {"color": "#64748B"}},
        decreasing={"marker": {"color": "#F43F5E"}},
        increasing={"marker": {"color": "#10B981"}},
        totals={"marker": {"color": "#3B82F6"}}
    ))
    waterfall_fig.update_layout(title_text="Inflows vs Outflows vs Net Cash Surplus", height=380)
    apply_chart_theme(waterfall_fig)
    st.plotly_chart(waterfall_fig, use_container_width=True)

with ch_col2:
    st.subheader("🍩 Outflow Distribution by Category")
    debit_df = filtered_df[filtered_df["transaction_type"] == "Debit"]
    if not debit_df.empty:
        cat_agg = debit_df.groupby("category_name")["amount"].sum().reset_index()
        donut_fig = px.pie(
            cat_agg,
            values="amount",
            names="category_name",
            hole=0.55,
            color_discrete_sequence=px.colors.qualitative.Prism
        )
        donut_fig.update_traces(textposition="inside", textinfo="percent+label")
        donut_fig.update_layout(title_text="Expenditure Share (%)", height=380, showlegend=False)
        apply_chart_theme(donut_fig)
        st.plotly_chart(donut_fig, use_container_width=True)
    else:
        st.info("No debit expenditure records in the filtered window.")

# 4. Recent High-Value Transactions
st.subheader("📑 Top 5 Highest Value Transactions in Filtered View")
top_txns = filtered_df.sort_values(by="amount", ascending=False).head(5)[
    ["transaction_id", "transaction_date", "account_name", "merchant_name", "category_name", "transaction_type", "amount", "status"]
]
st.dataframe(top_txns, use_container_width=True, hide_index=True)
