"""
pages/4_🏢_Cost_Centers.py
Screen UI-04: Departmental Cost Center Accounting & Budget Variance.
Tracks actual departmental expenditures against allocated budgets with threshold utilization indicators.
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
from src.analytics import compute_department_spend
from src.ui import render_tailwind_header, render_kpi_card, render_alert_box, apply_chart_theme

st.set_page_config(page_title="Department Cost Centers | NexGen", page_icon="🏢", layout="wide")

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
    title="Departmental Cost Accounting & Budget Utilization Cockpit",
    subtitle="Operational Outflow Tracking vs Allocated Budgets across Corporate Cost Centers",
    badge_text="Screen UI-04"
)

dept_df = compute_department_spend(df)

if dept_df.empty:
    st.warning("No departmental data found.")
    st.stop()

# 1. High-level Summary Cards
total_allocated = dept_df["budget_allocated"].sum()
total_actual = dept_df["Actual_Spend"].sum()
net_variance = total_allocated - total_actual
overall_utilization = round((total_actual / total_allocated * 100.0), 2) if total_allocated > 0 else 0.0

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card("Total Budget Allocated", f"₹{total_allocated:,.2f}", "Approved Operating Budget", status="neutral", height=110)
with c2:
    render_kpi_card("Total Actual Outflows", f"₹{total_actual:,.2f}", "Year-to-Date Spend", status="negative", height=110)
with c3:
    v_status = "positive" if net_variance >= 0 else "negative"
    render_kpi_card("Net Budget Variance", f"₹{net_variance:,.2f}", "Under Budget Surplus" if net_variance >= 0 else "Budget Overrun", status=v_status, height=110)
with c4:
    u_status = "positive" if overall_utilization <= 80 else ("warning" if overall_utilization <= 100 else "negative")
    render_kpi_card("Overall Budget Utilization", f"{overall_utilization:.1f}%", "Corporate Absorption Rate", status=u_status, height=110)

st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)

# 2. Visual Budget vs Actual Bar Chart
col1, col2 = st.columns([6, 4])

with col1:
    st.subheader("📊 Allocated Budget vs Actual Expenditure")
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=dept_df["department_name"],
        y=dept_df["budget_allocated"],
        name="Allocated Budget (₹)",
        marker_color="#3B82F6"
    ))
    fig_bar.add_trace(go.Bar(
        x=dept_df["department_name"],
        y=dept_df["Actual_Spend"],
        name="Actual Spend (₹)",
        marker_color="#F43F5E"
    ))
    fig_bar.update_layout(
        barmode="group",
        title="Budget vs Spend per Department",
        height=380,
        xaxis_title="Department",
        yaxis_title="Amount (₹)"
    )
    apply_chart_theme(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("🎯 Department Utilization %")
    fig_util = px.bar(
        dept_df,
        x="Utilization_Pct",
        y="department_name",
        orientation="h",
        text="Utilization_Pct",
        color="Utilization_Pct",
        color_continuous_scale=["#10B981", "#FBBF24", "#EF4444"],
        range_color=[50, 110],
        labels={"Utilization_Pct": "Utilization %", "department_name": "Department"}
    )
    fig_util.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
    fig_util.update_layout(title="Budget Consumption Status", height=380, coloraxis_showscale=False)
    apply_chart_theme(fig_util)
    st.plotly_chart(fig_util, use_container_width=True)

# 3. Detailed Departmental Variance Table
st.subheader("📑 Departmental Budget Variance Ledger")
st.dataframe(
    dept_df.style.format({
        "budget_allocated": "₹{:,.2f}",
        "Actual_Spend": "₹{:,.2f}",
        "Variance": "₹{:,.2f}",
        "Utilization_Pct": "{:.2f}%"
    }),
    use_container_width=True
)
