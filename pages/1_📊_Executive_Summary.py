"""
pages/1_📊_Executive_Summary.py
Screen UI-01: Executive Financial Summary & Corporate Liquidity Cockpit.
Institutional-grade dark fintech design inspired by Linear, Stripe, and Bloomberg Terminal.
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
from src.ui import (
    inject_fintech_theme,
    render_fintech_header,
    render_kpi_card,
    apply_chart_theme,
    format_inr
)

st.set_page_config(
    page_title="Executive Summary | NexGen Cockpit",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 1. Inject Institutional Dark Fintech Global Theme
inject_fintech_theme()

# 2. Ensure Data Session State
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

# 3. Sidebar Global Dashboard Filters
st.sidebar.markdown("""
<div style="padding: 4px 0 16px 0;">
    <div style="font-size: 0.72rem; font-weight: 700; color: #64748B; letter-spacing: 0.08em; text-transform: uppercase;">Control Center</div>
    <div style="font-size: 1.15rem; font-weight: 700; color: #F8FAFC; letter-spacing: -0.01em;">Global Filters</div>
</div>
""", unsafe_allow_html=True)

min_date = df["transaction_date"].min().date()
max_date = df["transaction_date"].max().date()

selected_dates = st.sidebar.date_input(
    "Active Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

start_date = pd.to_datetime(selected_dates[0]) if isinstance(selected_dates, (tuple, list)) and len(selected_dates) > 0 else pd.to_datetime(min_date)
end_date = pd.to_datetime(selected_dates[1]) if isinstance(selected_dates, (tuple, list)) and len(selected_dates) > 1 else pd.to_datetime(max_date)

with st.sidebar.expander("Accounts & Departments", expanded=True):
    all_accounts = sorted(df["account_name"].unique())
    selected_accounts = st.multiselect("Corporate Accounts", options=all_accounts, default=all_accounts)

    all_depts = sorted(df["department_name"].unique())
    selected_depts = st.multiselect("Business Cost Centers", options=all_depts, default=all_depts)

# Apply Active Filtering
filtered_df = df[
    (df["transaction_date"] >= start_date) &
    (df["transaction_date"] <= end_date) &
    (df["account_name"].isin(selected_accounts)) &
    (df["department_name"].isin(selected_depts))
]

# 4. Header Banner with Dynamic Date Range Sync
formatted_date_range = f"{start_date.strftime('%b %d, %Y')} – {end_date.strftime('%b %d, %Y')}"
render_fintech_header(
    title="Executive Financial Summary & Liquidity KPI Cockpit",
    subtitle=f"Consolidated Cash Flow Health, Revenue Inflows vs Expenditure Outflows ({formatted_date_range})",
    badge_text="Screen UI-01"
)

if filtered_df.empty:
    st.warning("No transaction records match the active filter criteria. Please broaden your selection.")
    st.stop()

# 5. Executive KPIs (Institutional Fintech Cards without white iframe boxes)
kpis = compute_executive_kpis(filtered_df)

c1, c2, c3, c4 = st.columns(4)
with c1:
    render_kpi_card(
        title="GROSS INFLOWS",
        value=format_inr(kpis['total_credit']),
        badge_text=f"{kpis['credit_count']} Inflow Transactions",
        accent_color="#10B981"
    )
with c2:
    render_kpi_card(
        title="GROSS OUTFLOWS",
        value=format_inr(kpis['total_debit']),
        badge_text=f"{kpis['debit_count']} Outflow Transactions",
        accent_color="#F43F5E"
    )
with c3:
    net_accent = "#10B981" if kpis['net_cash_flow'] >= 0 else "#F43F5E"
    net_badge = "Surplus Cash Position" if kpis['net_cash_flow'] >= 0 else "Deficit Cash Burn"
    render_kpi_card(
        title="NET CASH FLOW",
        value=format_inr(kpis['net_cash_flow']),
        badge_text=net_badge,
        accent_color=net_accent
    )
with c4:
    ratio_accent = "#10B981" if kpis['outflow_ratio'] < 80 else ("#F59E0B" if kpis['outflow_ratio'] <= 100 else "#F43F5E")
    ratio_badge = "Healthy Operating Margin" if kpis['outflow_ratio'] < 80 else "Elevated Expenditure"
    render_kpi_card(
        title="OUTFLOW / INFLOW RATIO",
        value=f"{kpis['outflow_ratio']:.1f}%",
        badge_text=ratio_badge,
        accent_color=ratio_accent
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# 6. Visual Analytics Row: Waterfall & Category Donut
ch_col1, ch_col2 = st.columns([6, 4])

with ch_col1:
    st.markdown("""
    <div class="fintech-chart-container">
        <div class="fintech-chart-header">
            <span class="fintech-chart-title">Cash Flow Liquidity Waterfall</span>
            <span class="fintech-chart-badge">Movement Breakdown</span>
        </div>
    """, unsafe_allow_html=True)

    net_label = f"-₹{abs(kpis['net_cash_flow'])/1e5:.2f}L" if kpis['net_cash_flow'] < 0 else f"₹{kpis['net_cash_flow']/1e5:.2f}L"
    waterfall_fig = go.Figure(go.Waterfall(
        name="Cash Flow Movement",
        orientation="v",
        measure=["relative", "relative", "total"],
        x=["Gross Credit Inflows", "Gross Debit Outflows", "Net Liquidity Position"],
        textposition="outside",
        text=[
            f"₹{kpis['total_credit']/1e5:.2f}L",
            f"-₹{kpis['total_debit']/1e5:.2f}L",
            net_label
        ],
        y=[kpis['total_credit'], -kpis['total_debit'], kpis['net_cash_flow']],
        connector={"line": {"color": "#475569", "width": 1.5, "dash": "dot"}},
        decreasing={"marker": {"color": "#F43F5E"}},
        increasing={"marker": {"color": "#10B981"}},
        totals={"marker": {"color": "#3B82F6"}},
        cliponaxis=False
    ))
    waterfall_fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", color="#CBD5E1", size=11),
        margin=dict(t=40, b=20, l=20, r=20),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            showgrid=True,
            zerolinecolor="rgba(255, 255, 255, 0.12)",
            tickfont=dict(color="#94A3B8")
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(color="#E2E8F0")
        ),
        height=340
    )
    st.plotly_chart(waterfall_fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("</div>", unsafe_allow_html=True)

with ch_col2:
    st.markdown("""
    <div class="fintech-chart-container">
        <div class="fintech-chart-header">
            <span class="fintech-chart-title">Outflow by Category</span>
            <span class="fintech-chart-badge">Capital Allocation Share</span>
        </div>
    """, unsafe_allow_html=True)

    debit_df = filtered_df[filtered_df["transaction_type"] == "Debit"]
    if not debit_df.empty:
        cat_agg = debit_df.groupby("category_name")["amount"].sum().reset_index()
        fintech_palette = ["#3B82F6", "#10B981", "#8B5CF6", "#F59E0B", "#06B6D4", "#EC4899", "#F43F5E", "#64748B"]
        donut_fig = px.pie(
            cat_agg,
            values="amount",
            names="category_name",
            hole=0.6,
            color_discrete_sequence=fintech_palette
        )
        donut_fig.update_traces(
            textposition="inside",
            textinfo="percent+label",
            textfont=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", size=10, color="#FFFFFF")
        )
        donut_fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", color="#CBD5E1"),
            margin=dict(t=20, b=20, l=15, r=15),
            height=340,
            showlegend=False
        )
        st.plotly_chart(donut_fig, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("No debit expenditure records in the filtered window.")
    st.markdown("</div>", unsafe_allow_html=True)

# 7. Recent High-Value Transactions Ledger
st.markdown("""
<div class="fintech-chart-container" style="margin-top: 10px;">
    <div class="fintech-chart-header">
        <span class="fintech-chart-title">High-Value Transaction Ledger</span>
        <span class="fintech-chart-badge">Top 5 Disbursements by Monetary Volume</span>
    </div>
""", unsafe_allow_html=True)

top_txns = filtered_df.sort_values(by="amount", ascending=False).head(5)[
    ["transaction_id", "transaction_date", "account_name", "merchant_name", "category_name", "transaction_type", "amount", "status"]
].rename(columns={
    "transaction_id": "Transaction ID",
    "transaction_date": "Date",
    "account_name": "Account",
    "merchant_name": "Merchant / Entity",
    "category_name": "Category",
    "transaction_type": "Type",
    "amount": "Amount",
    "status": "Status"
})

st.dataframe(
    top_txns.style.format({
        "Amount": "₹{:,.2f}",
        "Date": lambda t: pd.to_datetime(t).strftime("%d-%b-%Y") if pd.notna(t) else ""
    }),
    use_container_width=True,
    hide_index=True
)
st.markdown("</div>", unsafe_allow_html=True)
