"""
src/ui.py
Institutional Dark-Mode Fintech UI Architecture for NexGen Financial Analytics.
Inspired by Linear, Stripe, and Bloomberg Terminal.
Palette: Foundation #0B0F19, Surface #131A26, Accent #3B82F6, Emerald #10B981, Rose #F43F5E, Amber #F59E0B.
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd

def format_inr(val: float, compact: bool = False) -> str:
    """
    Format monetary amounts in INR properly with negative sign before currency symbol.
    Example:
        1750000.00 -> '₹1,750,000.00'
        -39321947.54 -> '-₹39,321,947.54'
    """
    if val is None or pd.isna(val):
        return "₹0.00"
    sign = "-" if val < 0 else ""
    abs_val = abs(float(val))
    if compact:
        if abs_val >= 10_000_000:
            return f"{sign}₹{abs_val / 10_000_000:.2f} Cr"
        elif abs_val >= 100_000:
            return f"{sign}₹{abs_val / 100_000:.2f} L"
        elif abs_val >= 1_000:
            return f"{sign}₹{abs_val / 1_000:.1f} K"
    return f"{sign}₹{abs_val:,.2f}"

def inject_fintech_theme():
    """
    Injects global institutional-grade dark fintech styling via CSS:
    - Imports Inter from Google Fonts and applies it globally
    - Reduces excess top padding on .block-container (padding-top: 1.5rem)
    - Hides default Streamlit chrome (#MainMenu, footer, decoration) without breaking sidebar collapse
    - Restyles st.multiselect tags into compact, muted dark-slate pills (#1E293B)
    """
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"], .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        background-color: #0B0F19 !important;
        color: #F8FAFC !important;
    }

    /* Reduce excess top padding on .block-container */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2.5rem !important;
        max-width: 96% !important;
    }

    /* Hide default Streamlit chrome without breaking sidebar collapse toggle */
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    div[data-testid="stDecoration"] { display: none !important; }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }

    /* Streamlit multiselect tag styling - compact muted dark slate tags */
    span[data-baseweb="tag"], div[data-baseweb="tag"] {
        background-color: #1E293B !important;
        border: 1px solid #334155 !important;
        border-radius: 6px !important;
        padding: 2px 8px !important;
        margin: 2px !important;
    }
    span[data-baseweb="tag"] span, div[data-baseweb="tag"] span {
        color: #E2E8F0 !important;
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }
    span[data-baseweb="tag"] svg, div[data-baseweb="tag"] svg {
        fill: #94A3B8 !important;
    }

    /* Sidebar background and clean typography */
    section[data-testid="stSidebar"] {
        background-color: #111827 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    /* Tabular numeric values */
    .tabular-numbers {
        font-variant-numeric: tabular-nums;
        -moz-font-feature-settings: "tnum";
        -webkit-font-feature-settings: "tnum";
        font-feature-settings: "tnum";
    }

    /* Chart Containers */
    .fintech-chart-container {
        background: #131A26;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 20px 14px 20px;
        box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.35);
        margin-bottom: 1.25rem;
    }

    .fintech-chart-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        padding-bottom: 10px;
    }

    .fintech-chart-title {
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        color: #F1F5F9;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .fintech-chart-badge {
        font-size: 0.7rem;
        font-weight: 500;
        color: #64748B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

def render_fintech_header(title: str, subtitle: str, badge_text: str = "SCREEN UI-01", enterprise: str = "NexGen Technologies Pvt. Ltd., Noida", author: str = "Mohd Kaif (Roll: 2500320140093)"):
    """
    Renders an institutional-grade dark gradient header banner natively in the DOM.
    Container: linear-gradient(#131A26, #0F172A) with 1px rgba(255,255,255,0.08) border and 12px radius.
    Left: Badge pill, Title, and dynamic Subtitle.
    Right: Enterprise metadata and author info in muted slate (#94A3B8).
    """
    header_html = f"""
    <div style="
        background: linear-gradient(135deg, #131A26 0%, #0F172A 100%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 20px 24px;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.45);
        margin-bottom: 22px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 16px;
    ">
        <div style="flex: 1 1 500px; min-width: 0;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 6px; flex-wrap: wrap;">
                <span style="
                    display: inline-flex;
                    align-items: center;
                    background: rgba(59, 130, 246, 0.12);
                    color: #60A5FA;
                    border: 1px solid rgba(59, 130, 246, 0.25);
                    font-size: 0.72rem;
                    font-weight: 600;
                    padding: 2px 8px;
                    border-radius: 6px;
                    letter-spacing: 0.04em;
                    text-transform: uppercase;
                ">{badge_text}</span>
                <span style="
                    color: #64748B;
                    font-size: 0.72rem;
                    font-weight: 600;
                    letter-spacing: 0.05em;
                    text-transform: uppercase;
                ">ABES MCA Capstone Project</span>
            </div>
            <h1 style="
                margin: 0;
                color: #FFFFFF;
                font-size: 1.55rem;
                font-weight: 800;
                letter-spacing: -0.025em;
                line-height: 1.25;
            ">{title}</h1>
            <p style="
                margin: 6px 0 0 0;
                color: #94A3B8;
                font-size: 0.85rem;
                line-height: 1.4;
                font-weight: 400;
            ">{subtitle}</p>
        </div>
        <div style="
            text-align: right;
            flex-shrink: 0;
            padding-left: 20px;
            border-left: 1px solid rgba(255, 255, 255, 0.06);
        ">
            <div style="color: #64748B; font-size: 0.7rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Target Enterprise</div>
            <div style="color: #E2E8F0; font-size: 0.85rem; font-weight: 600; margin-top: 2px;">{enterprise}</div>
            <div style="color: #94A3B8; font-size: 0.75rem; margin-top: 3px;">Author: {author}</div>
            <div style="color: #64748B; font-size: 0.7rem; margin-top: 2px;">Project ID: P059 &bull; Batch: ABES_OND26 MCA 2ND YEAR_DATA ANALYTICS_BATCH 01 &bull; Mentor: Mr Dinesh Sereno</div>
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

def render_tailwind_header(title: str, subtitle: str, badge_text: str = "NexGen Analytics v1.0", height: int = 150):
    """
    Corporate header renderer compatible with unit tests and native DOM injection.
    """
    render_fintech_header(title=title, subtitle=subtitle, badge_text=badge_text)

def render_kpi_card(title: str, value: str, badge_text: str = None, accent_color: str = "#3B82F6", delta: str = None, status: str = None, height: int = None):
    """
    Renders an institutional-grade dark KPI card using native HTML/CSS (no white iframe boxes).
    Surface: #131A26 with 1px rgba(255,255,255,0.08) border, 12px radius, and 3px subtle top accent bar.
    Labels: Uppercase, letter-spacing 0.06em, font-size 0.75rem.
    Amounts: font-variant-numeric: tabular-nums for aligned digits.
    Badges: Subtle tinted pills matching semantic accent color (Emerald, Rose, Amber, Blue).
    """
    # Normalize badge input
    badge = badge_text if badge_text is not None else delta

    # Map semantic keywords to institutional hex codes
    semantic_map = {
        "positive": "#10B981",  # Emerald
        "negative": "#F43F5E",  # Rose
        "warning":  "#F59E0B",  # Amber
        "neutral":  "#3B82F6"   # Royal Blue
    }

    if accent_color in semantic_map:
        accent_hex = semantic_map[accent_color]
    elif status in semantic_map:
        accent_hex = semantic_map[status]
    elif accent_color and accent_color.startswith("#"):
        accent_hex = accent_color
    else:
        accent_hex = "#3B82F6"

    # Semantic pill tinting
    if accent_hex in ("#10B981", "#10b981", "#34D399", "#059669"):
        badge_bg = "rgba(16, 185, 129, 0.12)"
        badge_text_color = "#34D399"
        badge_border = "rgba(16, 185, 129, 0.25)"
    elif accent_hex in ("#F43F5E", "#f43f5e", "#FB7185", "#E11D48", "#EF4444"):
        badge_bg = "rgba(244, 63, 94, 0.12)"
        badge_text_color = "#FB7185"
        badge_border = "rgba(244, 63, 94, 0.25)"
    elif accent_hex in ("#F59E0B", "#f59e0b", "#FBBF24", "#D97706"):
        badge_bg = "rgba(245, 158, 11, 0.12)"
        badge_text_color = "#FBBF24"
        badge_border = "rgba(245, 158, 11, 0.25)"
    else:
        badge_bg = "rgba(59, 130, 246, 0.12)"
        badge_text_color = "#60A5FA"
        badge_border = "rgba(59, 130, 246, 0.25)"

    badge_html = f"""
    <div style="margin-top: 10px;">
        <span style="
            display: inline-flex;
            align-items: center;
            background: {badge_bg};
            color: {badge_text_color};
            border: 1px solid {badge_border};
            font-size: 0.72rem;
            font-weight: 500;
            padding: 3px 8px;
            border-radius: 6px;
            letter-spacing: 0.02em;
        ">{badge}</span>
    </div>
    """ if badge else ""

    val_str = str(value)
    # Adaptive sizing for long monetary values
    font_size = "1.5rem" if len(val_str) <= 13 else "1.32rem"

    card_html = f"""
    <div style="
        background: #131A26;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-top: 3px solid {accent_hex};
        border-radius: 12px;
        padding: 16px 18px 14px 18px;
        box-shadow: 0 4px 16px -2px rgba(0, 0, 0, 0.35);
        min-height: 118px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        margin-bottom: 12px;
        transition: transform 0.2s ease, border-color 0.2s ease;
    ">
        <div>
            <div style="
                color: #94A3B8;
                font-size: 0.75rem;
                font-weight: 600;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                margin-bottom: 6px;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            ">{title}</div>
            <div style="
                color: #F8FAFC;
                font-size: {font_size};
                font-weight: 700;
                letter-spacing: -0.02em;
                font-variant-numeric: tabular-nums;
                white-space: nowrap;
                overflow: hidden;
                text-overflow: ellipsis;
            " title="{val_str}">{val_str}</div>
        </div>
        {badge_html}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def render_alert_box(title: str, message: str, alert_type: str = "warning", height: int = 115):
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
        <meta charset="utf-8">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            * {{ box-sizing: border-box; }}
            body {{
                margin: 0;
                padding: 2px 4px;
                background-color: transparent;
                font-family: 'Inter', ui-sans-serif, system-ui, sans-serif;
                overflow: hidden;
            }}
            .alert-card {{
                padding: 12px 14px;
                border-radius: 0.75rem;
            }}
        </style>
    </head>
    <body>
        <div class="alert-card border {style_classes} flex items-start gap-3 shadow-md">
            <div class="text-lg leading-tight shrink-0">{icon}</div>
            <div class="min-w-0">
                <div class="text-xs font-bold uppercase tracking-wider">{title}</div>
                <div class="text-xs text-slate-200 mt-0.5 leading-relaxed">{message}</div>
            </div>
        </div>
    </body>
    </html>
    """
    components.html(html_code, height=max(height, 115))

def apply_chart_theme(fig):
    """
    Applies the institutional dark fintech theme to Plotly figures.
    Linear / Stripe / Bloomberg Terminal inspired:
    - Zero background (transparent)
    - Inter font
    - Subtle horizontal gridlines (rgba(255,255,255,0.06))
    - Zero vertical gridlines
    """
    fig.update_layout(
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(family="Inter, -apple-system, BlinkMacSystemFont, sans-serif", color="#94A3B8", size=11),
        margin=dict(l=20, r=20, t=35, b=25),
        xaxis=dict(
            showgrid=False,
            linecolor="rgba(255, 255, 255, 0.1)",
            zerolinecolor="rgba(255, 255, 255, 0.1)",
            tickfont=dict(color="#94A3B8")
        ),
        yaxis=dict(
            gridcolor="rgba(255, 255, 255, 0.06)",
            linecolor="rgba(255, 255, 255, 0.1)",
            zerolinecolor="rgba(255, 255, 255, 0.12)",
            tickfont=dict(color="#94A3B8")
        ),
        legend=dict(
            bgcolor="rgba(19, 26, 38, 0.8)",
            bordercolor="rgba(255, 255, 255, 0.08)",
            font=dict(color="#E2E8F0")
        )
    )
    return fig
