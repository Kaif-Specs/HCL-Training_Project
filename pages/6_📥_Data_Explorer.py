"""
pages/6_📥_Data_Explorer.py
Screen UI-06: Interactive Data Explorer & Export Engine.
Provides comprehensive multi-attribute filtering, column selection, and CSV export.
"""

import streamlit as st
import pandas as pd
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.data_loader import load_analysis_view
from src.cleaner import clean_transaction_data
from src.ui import render_tailwind_header, render_kpi_card, format_inr, inject_fintech_theme

st.set_page_config(page_title="Data Explorer | NexGen", page_icon="📥", layout="wide")
inject_fintech_theme()

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
    title="Interactive Data Explorer & Analytical Ledger Export",
    subtitle="Full Multi-Column Attribute Filter, Keyword Search, and Structured CSV Download",
    badge_text="Screen UI-06"
)

# 1. Search and Filtering Controls
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    search_term = st.text_input("🔍 Global Keyword Search", placeholder="e.g. AWS, Salary, Mumbai, ICICI...")
with col_f2:
    txn_type_filter = st.multiselect("Transaction Type", options=["Credit", "Debit"], default=["Credit", "Debit"])
with col_f3:
    status_filter = st.multiselect("Transaction Status", options=sorted(df["status"].unique()), default=sorted(df["status"].unique()))

# Filter logic
filtered = df.copy()
if txn_type_filter:
    filtered = filtered[filtered["transaction_type"].isin(txn_type_filter)]
if status_filter:
    filtered = filtered[filtered["status"].isin(status_filter)]
if search_term:
    mask = filtered.astype(str).apply(lambda row: row.str.contains(search_term, case=False).any(), axis=1)
    filtered = filtered[mask]

# 2. Results Metrics
c1, c2, c3 = st.columns(3)
with c1:
    render_kpi_card("Matching Records", f"{len(filtered):,}", f"Out of {len(df):,} Cleaned", status="neutral")
with c2:
    render_kpi_card("Total Filtered Amount", format_inr(filtered['amount'].sum()), "Aggregated Sum", status="positive" if filtered['amount'].sum() > 0 else "neutral")
with c3:
    mean_val = filtered['amount'].mean() if not filtered.empty else 0.0
    render_kpi_card("Average Transaction Size", format_inr(mean_val), "Mean Ticket Value", status="neutral")

st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

# 3. Column Visibility Selector
default_cols = [
    "transaction_id", "transaction_date", "account_name", "merchant_name",
    "category_name", "department_name", "transaction_type", "payment_method",
    "amount", "status"
]
available_cols = list(df.columns)
selected_cols = st.multiselect("Select Columns to Display", options=available_cols, default=[c for c in default_cols if c in available_cols])

# 4. Display Table & Export Button
if not filtered.empty:
    display_df = filtered[selected_cols] if selected_cols else filtered
    
    # Apply clean formatting to monetary & statistical columns
    format_dict = {}
    for col in ["amount", "fee_amount", "budget_allocated", "Actual_Spend", "Variance"]:
        if col in display_df.columns:
            format_dict[col] = "₹{:,.2f}"
    if "z_score" in display_df.columns:
        format_dict["z_score"] = "{:.2f}"
    if "transaction_date" in display_df.columns:
        format_dict["transaction_date"] = lambda t: pd.to_datetime(t).strftime("%d-%b-%Y") if pd.notna(t) else ""

    if format_dict:
        st.dataframe(display_df.style.format(format_dict), use_container_width=True, hide_index=True)
    else:
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    csv_data = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Current Filtered View as CSV",
        data=csv_data,
        file_name="nexgen_filtered_transactions.csv",
        mime="text/csv"
    )
else:
    st.warning("No records match the current search or filter parameters.")
