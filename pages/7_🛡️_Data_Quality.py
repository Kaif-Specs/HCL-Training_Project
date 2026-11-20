"""
pages/7_🛡️_Data_Quality.py
Screen UI-07: Data Quality Governance, Imputation & Deduplication Audit.
Displays health metrics, null value profiling, duplicate transaction log, and raw vs clean inspection.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.data_loader import load_analysis_view
from src.cleaner import clean_transaction_data
from src.ui import render_tailwind_header, render_kpi_card, render_alert_box, apply_chart_theme, inject_fintech_theme

st.set_page_config(page_title="Data Quality Audit | NexGen", page_icon="🛡️", layout="wide")
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
    else:
        raw_df = st.session_state["raw_df"]
        clean_df = st.session_state["clean_df"]
        audit_log = st.session_state["audit_log"]
except Exception:
    raw_df = load_analysis_view()
    clean_df, audit_log = clean_transaction_data(raw_df)

render_tailwind_header(
    title="Data Quality Governance & Pipeline Audit Dashboard",
    subtitle="Null Imputation Profiles, Duplicate Record Detection Log, and Dataset Integrity Assurance",
    badge_text="Screen UI-07"
)

# 1. Health Score Cards
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Overall Data Health Score", f"{audit_log['health_score']}%", "Comprehensive Reliability Index", status="positive")
with c2:
    render_kpi_card("Ingested Raw Records", f"{audit_log['raw_records']:,}", "Database Source Rows", status="neutral")
with c3:
    render_kpi_card("Duplicates Purged", f"{audit_log['duplicates_removed']}", "Eliminated Redundant Entries", status="warning" if audit_log['duplicates_removed'] > 0 else "positive")
with c4:
    render_kpi_card("Null Categoricals Imputed", f"{audit_log['nulls_imputed']}", "Imputed with 'Unknown/Pending'", status="positive")

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# 2. Duplicate Transaction Audit Log
st.subheader("📑 Duplicate Records Elimination Audit")
if audit_log["duplicate_ids"]:
    st.write(f"The following **{len(audit_log['duplicate_ids'])} duplicate transactions** were identified on compound key `['account_id', 'transaction_date', 'amount', 'transaction_type', 'merchant_id']` and safely purged:")
    dup_rows = raw_df[raw_df["transaction_id"].isin(audit_log["duplicate_ids"])][
        ["transaction_id", "transaction_date", "account_name", "merchant_name", "amount", "transaction_type"]
    ]
    st.dataframe(
        dup_rows.style.format({
            "amount": "₹{:,.2f}",
            "transaction_date": lambda t: pd.to_datetime(t).strftime("%d-%b-%Y") if pd.notna(t) else ""
        }),
        use_container_width=True,
        hide_index=True
    )
else:
    st.success("✅ No duplicate records detected in the active database.")

# 3. Missing Value Analysis
st.subheader("🔍 Missing Values Profile (Before vs After Cleansing)")
raw_nulls = raw_df.isnull().sum().reset_index()
raw_nulls.columns = ["Column", "Raw_Missing_Count"]
clean_nulls = clean_df.isnull().sum().reset_index()
clean_nulls.columns = ["Column", "Clean_Missing_Count"]

null_comp = pd.merge(raw_nulls, clean_nulls, on="Column")
null_comp = null_comp[null_comp["Raw_Missing_Count"] > 0]

if not null_comp.empty:
    fig_null = px.bar(
        null_comp,
        x="Column",
        y=["Raw_Missing_Count", "Clean_Missing_Count"],
        barmode="group",
        title="Missing Values Rectification Audit",
        labels={"value": "Null / Blank Count", "variable": "Dataset State"},
        color_discrete_map={"Raw_Missing_Count": "#EF4444", "Clean_Missing_Count": "#10B981"}
    )
    apply_chart_theme(fig_null)
    st.plotly_chart(fig_null, use_container_width=True)
else:
    st.info("No missing values found across primary columns.")

# 4. Interactive Dataset Inspection Toggle
st.subheader("🔬 Raw Ingestion vs Sanitized Analytical Dataset Inspector")
view_mode = st.radio("Select Dataset Perspective to Inspect:", ["Sanitized Clean Dataset (300 Rows)", "Raw Source View (302 Rows)"], horizontal=True)

if view_mode == "Sanitized Clean Dataset (300 Rows)":
    st.dataframe(clean_df.head(50), use_container_width=True)
else:
    st.dataframe(raw_df.head(50), use_container_width=True)
