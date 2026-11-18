"""
pages/5_🔍_Anomaly_Detection.py
Screen UI-05: Statistical Anomaly Detection & Vendor Concentration Audit.
Features Parametric Z-Score, Non-Parametric Tukey's Fences, and Pareto 80/20 spend curves.
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
from src.stats_engine import detect_outliers_zscore, detect_outliers_tukey, compute_vendor_pareto
from src.ui import render_tailwind_header, render_kpi_card, render_alert_box, apply_chart_theme

st.set_page_config(page_title="Anomaly Detection | NexGen", page_icon="🔍", layout="wide")

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
    title="Statistical Anomaly Audit & Vendor Concentration Governance",
    subtitle="Parametric Z-Score (|Z| > 3.0), Tukey Interquartile Fences & Vendor Outflow Pareto Analysis",
    badge_text="Screen UI-05"
)

# 1. Parameter Sensitivity Controls in Sidebar
st.sidebar.header("⚙️ Statistical Sensitivity Controls")
z_thresh = st.sidebar.slider("Z-Score Sensitivity Threshold", min_value=2.0, max_value=4.0, value=3.0, step=0.1)
tukey_k = st.sidebar.slider("Tukey Fences Multiplier (k)", min_value=1.0, max_value=3.0, value=1.5, step=0.1)

# Apply statistical engines
z_df = detect_outliers_zscore(df, threshold=z_thresh)
full_anomaly_df = detect_outliers_tukey(z_df, k=tukey_k)

z_outliers = full_anomaly_df[full_anomaly_df["is_outlier_z"]]
tukey_outliers = full_anomaly_df[full_anomaly_df["is_outlier_tukey"]]

# KPI Summary
c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Z-Score Flagged Anomalies", f"{len(z_outliers)}", f"Threshold |Z| > {z_thresh}", status="negative" if len(z_outliers) > 0 else "positive", height=110)
with c2:
    render_kpi_card("Tukey IQR Outliers", f"{len(tukey_outliers)}", f"Multiplier k = {tukey_k}", status="warning" if len(tukey_outliers) > 0 else "positive", height=110)
with c3:
    tukey_ub = full_anomaly_df["tukey_upper_bound"].iloc[0] if "tukey_upper_bound" in full_anomaly_df.columns else 0.0
    render_kpi_card("Tukey Upper Bound Fence", f"₹{tukey_ub:,.2f}", "Upper Outlier Cutoff", status="neutral", height=110)
with c4:
    total_anom_val = z_outliers["amount"].sum()
    render_kpi_card("Flagged Outlier Value", f"₹{total_anom_val:,.2f}", "Suspect Capital Outflow", status="negative", height=110)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# 2. Scatter Plot: Anomaly Distribution Over Time
st.subheader("📈 Temporal Disbursement Scatter Plot with Z-Score Anomaly Highlights")
debits = full_anomaly_df[full_anomaly_df["transaction_type"] == "Debit"].copy()
debits["Classification"] = debits["is_outlier_z"].apply(lambda x: "High Outlier (|Z| > 3.0)" if x else "Standard Disbursement")

fig_scatter = px.scatter(
    debits,
    x="transaction_date",
    y="amount",
    color="Classification",
    size="amount",
    hover_data=["transaction_id", "merchant_name", "category_name", "z_score"],
    color_discrete_map={"Standard Disbursement": "#3B82F6", "High Outlier (|Z| > 3.0)": "#EF4444"},
    labels={"amount": "Disbursement Amount (₹)", "transaction_date": "Date"}
)
fig_scatter.update_layout(title="Transaction Amount vs Date (Outliers Highlighted in Red)", height=400)
apply_chart_theme(fig_scatter)
st.plotly_chart(fig_scatter, use_container_width=True)

# 3. Vendor Pareto Analysis
st.subheader("🎯 Vendor Outflow Concentration (Pareto 80/20 Distribution)")
pareto_df = compute_vendor_pareto(df)

if not pareto_df.empty:
    top10_vendors = pareto_df.head(10)
    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Bar(
        x=top10_vendors["merchant_name"],
        y=top10_vendors["Total_Spend"],
        name="Vendor Spend (₹)",
        marker_color="#2563EB",
        yaxis="y"
    ))
    fig_pareto.add_trace(go.Scatter(
        x=top10_vendors["merchant_name"],
        y=top10_vendors["Cumulative_Pct"],
        name="Cumulative Spend %",
        marker_color="#F59E0B",
        mode="lines+markers",
        yaxis="y2"
    ))
    fig_pareto.update_layout(
        title="Top 10 Vendors by Spend & Cumulative Absorption Curve",
        height=400,
        yaxis=dict(title="Spend Amount (₹)"),
        yaxis2=dict(title="Cumulative Spend %", overlaying="y", side="right", range=[0, 105]),
        legend=dict(x=0.7, y=1.1)
    )
    apply_chart_theme(fig_pareto)
    st.plotly_chart(fig_pareto, use_container_width=True)

# 4. Suspect Transactions Audit Table
st.subheader("🚨 Suspect Outlier Transactions Audit Table")
if not z_outliers.empty:
    cols_show = ["transaction_id", "transaction_date", "merchant_name", "category_name", "department_name", "amount", "z_score", "status"]
    st.dataframe(z_outliers[cols_show].sort_values(by="amount", ascending=False), use_container_width=True, hide_index=True)
    
    csv_bytes = z_outliers[cols_show].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Flagged Outliers as CSV",
        data=csv_bytes,
        file_name="flagged_anomalies_audit.csv",
        mime="text/csv"
    )
else:
    st.success("✅ Zero transactions exceed the active Z-score threshold.")
