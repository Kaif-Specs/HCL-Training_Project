"""
src/ui.py
Reusable UI Component Library for Credit vs Debit Transaction Analysis System
Renders Tailwind CSS v3 via CDN inside Streamlit components.
Theme: Slate 900 Dark Foundation with Royal Blue (#2563EB) & Emerald (#10B981)
"""

import streamlit as st
import streamlit.components.v1 as components

def render_tailwind_header(title: str, subtitle: str, badge_text: str = "NexGen Analytics v1.0"):
    """
    Renders an executive corporate header with Tailwind CSS styling.
    """
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ margin: 0; padding: 0; background-color: transparent; font-family: ui-sans-serif, system-ui, sans-serif; }}
        </style>
    </head>
    <body>
        <div class="p-6 rounded-2xl bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 border border-slate-700/60 shadow-xl mb-4">
            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-3">
                <div>
                    <div class="flex items-center gap-2 mb-1">
                        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20">
                            {badge_text}
                        </span>
                        <span class="text-xs text-slate-400 font-medium tracking-wide uppercase">ABES MCA Capstone Project</span>
                    </div>
                    <h1 class="text-2xl md:text-3xl font-extrabold text-white tracking-tight">{title}</h1>
                    <p class="text-sm text-slate-300 mt-1">{subtitle}</p>
                </div>
                <div class="text-right hidden md:block">
                    <div class="text-xs text-slate-400">Target Enterprise</div>
                    <div class="text-sm font-semibold text-slate-200">NexGen Technologies Pvt. Ltd., Noida</div>
                    <div class="text-xs text-slate-400 mt-0.5">Author: Mohd Kaif (Roll: 2503201450093)</div>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=135)

def render_kpi_card(title: str, value: str, delta: str = None, status: str = "neutral", height: int = 120):
    """
    Renders a responsive Tailwind CSS KPI card.
    status: 'positive' (emerald), 'negative' (rose), 'warning' (amber), 'neutral' (blue)
    """
    color_map = {
        "positive": ("bg-emerald-500/10 text-emerald-400 border-emerald-500/20", "text-emerald-400"),
        "negative": ("bg-rose-500/10 text-rose-400 border-rose-500/20", "text-rose-400"),
        "warning":  ("bg-amber-500/10 text-amber-400 border-amber-500/20", "text-amber-400"),
        "neutral":  ("bg-blue-500/10 text-blue-400 border-blue-500/20", "text-blue-400")
    }
    badge_class, text_class = color_map.get(status, color_map["neutral"])
    delta_html = f'<div class="mt-2 inline-flex items-center px-2.5 py-0.5 rounded text-xs font-semibold border {badge_class}">{delta}</div>' if delta else ""

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ margin: 0; padding: 0; background-color: transparent; font-family: ui-sans-serif, system-ui, sans-serif; }}
        </style>
    </head>
    <body>
        <div class="p-4 rounded-xl bg-slate-800/90 border border-slate-700/80 shadow-lg hover:border-slate-600 transition-all">
            <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</div>
            <div class="text-2xl font-bold mt-1 text-slate-100 tracking-tight">{value}</div>
            {delta_html}
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=height)

def render_alert_box(title: str, message: str, alert_type: str = "warning", height: int = 100):
    """
    Renders an executive callout alert banner.
    alert_type: 'warning' (amber), 'critical' (red), 'success' (green), 'info' (blue)
    """
    styles = {
        "warning":  ("border-amber-500/40 bg-amber-950/20 text-amber-300", "⚠️"),
        "critical": ("border-rose-500/40 bg-rose-950/20 text-rose-300", "🚨"),
        "success":  ("border-emerald-500/40 bg-emerald-950/20 text-emerald-300", "✅"),
        "info":     ("border-blue-500/40 bg-blue-950/20 text-blue-300", "ℹ️")
    }
    style_classes, icon = styles.get(alert_type, styles["info"])

    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ margin: 0; padding: 0; background-color: transparent; font-family: ui-sans-serif, system-ui, sans-serif; }}
        </style>
    </head>
    <body>
        <div class="p-3.5 rounded-xl border {style_classes} flex items-start gap-3 shadow-md">
            <div class="text-lg">{icon}</div>
            <div>
                <div class="text-xs font-bold uppercase tracking-wider">{title}</div>
                <div class="text-xs text-slate-200 mt-0.5">{message}</div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=height)

def apply_chart_theme(fig):
    """
    Applies the enterprise Slate 900 / Royal Blue theme to Plotly figures.
    """
    fig.update_layout(
        paper_bgcolor="rgba(15, 23, 42, 0.0)",
        plot_bgcolor="rgba(30, 41, 59, 0.4)",
        font=dict(family="ui-sans-serif, system-ui, sans-serif", color="#CBD5E1", size=12),
        margin=dict(l=40, r=40, t=50, b=40),
        xaxis=dict(
            gridcolor="#334155",
            linecolor="#475569",
            zerolinecolor="#475569"
        ),
        yaxis=dict(
            gridcolor="#334155",
            linecolor="#475569",
            zerolinecolor="#475569"
        ),
        legend=dict(
            bgcolor="rgba(30, 41, 59, 0.7)",
            bordercolor="#475569",
            font=dict(color="#F1F5F9")
        )
    )
    return fig
