"""
pages/2_💳_Credit_vs_Debit.py
Screen UI-02: Credit vs Debit Comparative Analysis.
Features transaction volume vs monetary value comparisons, payment channel distributions, and category ratios.
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
from src.ui import render_tailwind_header, render_kpi_card, apply_chart_theme

st.set_page_config(page_title="Credit vs Debit Comparison | NexGen", page_icon="💳", layout="wide")

if "clean_df" not in st.session_state:
    raw_df = load_analysis_view()
    clean_df, audit_log = clean_transaction_data(raw_df)
    st.session_state["raw_df"] = raw_df
    st.session_state["clean_df"] = clean_df
    st.session_state["audit_log"] = audit_log

df = st.session_state["clean_df"]

render_tailwind_header(
    title="Credit Inflows vs Debit Outflows Comparative Analysis",
    subtitle="Monetary Value, Transaction Frequency, and Payment Mode Channel Disaggregation",
    badge_text="Screen UI-02"
)

# 1. Comparative Volume vs Value Metrics
credit_df = df[df["transaction_type"] == "Credit"]
debit_df = df[df["transaction_type"] == "Debit"]

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Credit Transaction Count", f"{len(credit_df):,}", "Inflow Events", status="positive", height=110)
with c2:
    render_kpi_card("Debit Transaction Count", f"{len(debit_df):,}", "Disbursement Events", status="negative", height=110)
with c3:
    render_kpi_card("Avg Credit Ticket Size", f"₹{credit_df['amount'].mean():,.2f}", "Client / Contract Inflows", status="positive", height=110)
with c4:
    render_kpi_card("Avg Debit Ticket Size", f"₹{debit_df['amount'].mean():,.2f}", "Operational Expenses", status="neutral", height=110)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# 2. Dual Side-by-Side Visuals
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Transaction Count vs Monetary Value")
    type_summary = df.groupby("transaction_type").agg(
        Count=("transaction_id", "count"),
        Total_Value=("amount", "sum")
    ).reset_index()

    fig_val = px.bar(
        type_summary,
        x="transaction_type",
        y="Total_Value",
        color="transaction_type",
        text_auto=".2s",
        color_discrete_map={"Credit": "#10B981", "Debit": "#F43F5E"},
        labels={"Total_Value": "Total Amount (₹)", "transaction_type": "Transaction Type"}
    )
    fig_val.update_layout(title="Total Amount (₹) by Transaction Type", height=360)
    apply_chart_theme(fig_val)
    st.plotly_chart(fig_val, use_container_width=True)

with col2:
    st.subheader("💳 Outflow Distribution by Payment Channel")
    if "payment_method" in debit_df.columns:
        pm_agg = debit_df.groupby("payment_method")["amount"].agg(Total_Amount="sum", Count="count").reset_index()
        fig_pm = px.bar(
            pm_agg,
            x="Total_Amount",
            y="payment_method",
            orientation="h",
            text_auto=".2s",
            color="Total_Amount",
            color_continuous_scale="Blues",
            labels={"Total_Amount": "Disbursed Amount (₹)", "payment_method": "Payment Method"}
        )
        fig_pm.update_layout(title="Debit Volume by Payment Mode", height=360, coloraxis_showscale=False)
        apply_chart_theme(fig_pm)
        st.plotly_chart(fig_pm, use_container_width=True)

# 3. Category Comparison Table
st.subheader("📑 Category-Level Inflow vs Outflow Breakdown")
pivot_cat = df.pivot_table(
    index="category_name",
    columns="transaction_type",
    values="amount",
    aggfunc=["sum", "count"],
    fill_value=0.0
).reset_index()

# Flatten MultiIndex columns
pivot_cat.columns = ["Category", "Credit_Sum", "Debit_Sum", "Credit_Count", "Debit_Count"]
pivot_cat["Net_Balance"] = pivot_cat["Credit_Sum"] - pivot_cat["Debit_Sum"]
pivot_cat = pivot_cat.sort_values(by="Debit_Sum", ascending=False)

st.dataframe(
    pivot_cat.style.format({
        "Credit_Sum": "₹{:,.2f}",
        "Debit_Sum": "₹{:,.2f}",
        "Net_Balance": "₹{:,.2f}",
        "Credit_Count": "{:,}",
        "Debit_Count": "{:,}"
    }),
    use_container_width=True
)
