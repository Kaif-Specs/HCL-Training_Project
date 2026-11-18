"""
app.py
Application Entrypoint & Session State Gateway.
Project: Credit vs Debit Transaction Analysis System
Enterprise: NexGen Technologies Pvt. Ltd., Noida
Author: Mohd Kaif (MCA 2nd Year Data Analytics, ABES EC)
"""

import streamlit as st
import os
import sys

# Ensure root workspace is in python path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from src.data_loader import load_analysis_view
from src.cleaner import clean_transaction_data
from src.ui import render_tailwind_header, render_alert_box, render_kpi_card

st.set_page_config(
    page_title="NexGen Financial Analytics",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Initialize Global Session State & Ingest Data
try:
    if "raw_df" not in st.session_state:
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

# Safe fallback
if "raw_df" not in locals() or raw_df is None:
    raw_df = load_analysis_view()
    clean_df, audit_log = clean_transaction_data(raw_df)

# 2. Main Portal Interface
render_tailwind_header(
    title="Corporate Credit vs Debit Analytics Portal",
    subtitle="Enterprise Cash Flow Intelligence, Departmental Cost Accounting & Automated Fraud Detection",
    badge_text="Live Production v1.0"
)

col1, col2, col3, col4 = st.columns(4)
with col1:
    render_kpi_card("Total Ingested Rows", f"{len(raw_df):,}", "Verified Star Schema", status="neutral", height=115)
with col2:
    render_kpi_card("Cleaned Analytical Rows", f"{len(clean_df):,}", f"{audit_log['duplicates_removed']} Duplicates Purged", status="positive", height=115)
with col3:
    render_kpi_card("Data Health Score", f"{audit_log['health_score']}%", f"{audit_log['nulls_imputed']} Nulls Imputed", status="positive", height=115)
with col4:
    render_kpi_card("Total Accounts Monitored", f"{clean_df['account_id'].nunique()}", "Active Banking Entities", status="neutral", height=115)

st.markdown("---")

st.markdown("""
### 🧭 Analytical Navigation Hub
Select an analytical dashboard module from the **sidebar navigation** to explore specific operational insights:

- **1. 📊 Executive Summary:** High-level executive KPIs, liquidity waterfalls, and category outflow donuts.
- **2. 💳 Credit vs Debit:** Volume vs monetary value side-by-side comparative matrices and payment mode distributions.
- **3. 📈 Cash Flow Trends:** Longitudinal monthly cash flow trends, 30-day moving averages, and seasonal spikes.
- **4. 🏢 Cost Centers:** Departmental cost allocation, actual spend vs quarterly budget variances, and utilization gauges.
- **5. 🔍 Anomaly Detection:** Parametric Z-Score ($|Z| > 3.0$) and Non-Parametric Tukey's Fences ($Q3 + 1.5 \times IQR$) with vendor Pareto.
- **6. 📥 Data Explorer:** Interactive multi-column filter table with instant CSV export engine.
- **7. 🛡️ Data Quality:** Ingestion audit logs, deduplication reports, and raw vs sanitized dataset inspection.
""")

st.markdown("---")
render_alert_box(
    title="ACADEMIC & ENTERPRISE COMPLIANCE NOTICE",
    message="This project is developed by Mohd Kaif (Roll No: 2503201450093), MCA 2nd Year, ABES Engineering College under academic mentorship of Prof. Shilpa Tyagi. Target organization: NexGen Technologies Pvt. Ltd., Noida.",
    alert_type="info",
    height=90
)
