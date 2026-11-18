"""
pages/3_📈_Cash_Flow_Trends.py
Screen UI-03: Longitudinal Cash Flow Dynamics & Trend Analytics.
Analyzes monthly disbursement rhythms, moving averages, and cumulative liquidity curves.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.data_loader import load_analysis_view
from src.cleaner import clean_transaction_data
from src.analytics import compute_monthly_trends
from src.ui import render_tailwind_header, render_kpi_card, render_alert_box, apply_chart_theme

st.set_page_config(page_title="Cash Flow Trends | NexGen", page_icon="📈", layout="wide")

try:
    if "clean_df" not in st.session_state:
        raw_df = load_analysis_view()
        clean_df, audit_log = clean_transaction_data(raw_df)
        try:
            st.session_state["raw_df"] = raw_df
            st.session_state["clean_df"] = clean_df
            st.session_state["audit_log"] = audit_log
        except Exception:
            pass
        df = clean_df
    else:
        df = st.session_state["clean_df"]
except Exception:
    raw_df = load_analysis_view()
    df, _ = clean_transaction_data(raw_df)

render_tailwind_header(
    title="Longitudinal Cash Flow Rhythms & Temporal Trend Analytics",
    subtitle="Monthly Inflow vs Outflow Velocity, 30-Day Moving Averages & Cumulative Liquidity (Q1–Q3 2024)",
    badge_text="Screen UI-03"
)

monthly_df = compute_monthly_trends(df)

if monthly_df.empty:
    st.warning("Insufficient temporal data to compute monthly trends.")
    st.stop()

# 1. Monthly Performance Visual
st.subheader("📊 Monthly Inflows (Credit) vs Outflows (Debit)")
fig_monthly = go.Figure()
fig_monthly.add_trace(go.Bar(
    x=monthly_df["YearMonth"],
    y=monthly_df["Credit"],
    name="Inflow (Credit)",
    marker_color="#10B981"
))
fig_monthly.add_trace(go.Bar(
    x=monthly_df["YearMonth"],
    y=monthly_df["Debit"],
    name="Outflow (Debit)",
    marker_color="#F43F5E"
))
fig_monthly.add_trace(go.Scatter(
    x=monthly_df["YearMonth"],
    y=monthly_df["Debit_30d_MA"],
    name="Debit 30-Day Moving Avg",
    mode="lines+markers",
    line=dict(color="#FBBF24", width=3, dash="dot")
))
fig_monthly.update_layout(
    barmode="group",
    title="Monthly Operating Cash Flow & Moving Average Benchmark",
    height=400,
    xaxis_title="Calendar Month",
    yaxis_title="Amount (₹)"
)
apply_chart_theme(fig_monthly)
st.plotly_chart(fig_monthly, use_container_width=True)

# 2. Cumulative Net Liquidity Curve
st.subheader("🌊 Cumulative Net Liquidity Growth Curve")
fig_cum = go.Figure()
fig_cum.add_trace(go.Scatter(
    x=monthly_df["YearMonth"],
    y=monthly_df["Cumulative_Net"],
    mode="lines+markers",
    name="Cumulative Net Cash Flow",
    line=dict(color="#3B82F6", width=3),
    fill="tozeroy",
    fillcolor="rgba(59, 130, 246, 0.15)"
))
fig_cum.add_hline(y=0, line_dash="dash", line_color="#EF4444", annotation_text="Break-Even Baseline")
fig_cum.update_layout(
    title="Cumulative Cash Retention Progression (₹)",
    height=350,
    xaxis_title="Month",
    yaxis_title="Cumulative Net (₹)"
)
apply_chart_theme(fig_cum)
st.plotly_chart(fig_cum, use_container_width=True)

# 3. Monthly Financial Rollup Table
st.subheader("📑 Monthly Aggregated Ledger Statement")
st.dataframe(
    monthly_df.style.format({
        "Credit": "₹{:,.2f}",
        "Debit": "₹{:,.2f}",
        "Net_Cash_Flow": "₹{:,.2f}",
        "Cumulative_Net": "₹{:,.2f}",
        "Debit_30d_MA": "₹{:,.2f}"
    }),
    use_container_width=True
)
