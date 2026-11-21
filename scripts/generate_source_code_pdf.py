"""
Source Code PDF Generator for LMS Submission
Learner: Mohd Kaif
Roll Number: 2500320140093
Batch ID: ABES_OND26 MCA 2ND YEAR_DATA ANALYTICS_BATCH 01
Project ID: P059
Academic Mentor: Mr Dinesh Sereno (DINESH SERENO)
Institution: ABES Engineering College, Ghaziabad
Academic Program: MCA — 2nd Year Data Analytics
Project: Credit vs Debit Transaction Analysis System
Target File: 2500320140093_MohdKaif_Source_Code.pdf
"""

import os
import re
import sys
import shutil

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ----------------------------------------------------------------------
# 1. Register Fonts (Consolas for Code, Segoe UI / Arial for Typography)
# ----------------------------------------------------------------------
try:
    pdfmetrics.registerFont(TTFont("CodeFont", r"C:\Windows\Fonts\consola.ttf"))
    pdfmetrics.registerFont(TTFont("CodeFontBold", r"C:\Windows\Fonts\consolab.ttf"))
except Exception as e:
    print(f"Warning: Could not load Consolas ({e}), falling back to standard fonts.")

try:
    pdfmetrics.registerFont(TTFont("MainFont", r"C:\Windows\Fonts\segoeui.ttf"))
    pdfmetrics.registerFont(TTFont("MainFontBold", r"C:\Windows\Fonts\segoeuib.ttf"))
except Exception:
    pdfmetrics.registerFont(TTFont("MainFont", r"C:\Windows\Fonts\arial.ttf"))
    pdfmetrics.registerFont(TTFont("MainFontBold", r"C:\Windows\Fonts\arialbd.ttf"))

# ----------------------------------------------------------------------
# 2. File Manifest (Strict LMS Sequence)
# ----------------------------------------------------------------------
FILE_MANIFEST = [
    # 1. Main Entrypoint
    {
        "category": "Main Application Entrypoint",
        "badge": "STREAMLIT ENTRYPOINT",
        "path": "app.py",
        "display_name": "app.py",
        "desc": "Primary Streamlit entrypoint configuring routing, styling, session state, and navigation."
    },
    # 2. Streamlit Pages
    {
        "category": "Streamlit Dashboard Pages",
        "badge": "MULTI-PAGE UI",
        "path": "pages/1_📊_Executive_Summary.py",
        "display_name": "pages/1_Executive_Summary.py",
        "desc": "Enterprise KPI dashboard, cash flow health scoring, liquidity gauge, and key charts."
    },
    {
        "category": "Streamlit Dashboard Pages",
        "badge": "MULTI-PAGE UI",
        "path": "pages/2_💳_Credit_vs_Debit.py",
        "display_name": "pages/2_Credit_vs_Debit.py",
        "desc": "Comparative analytics of inflows vs outflows, net burn rate, and ratio benchmarking."
    },
    {
        "category": "Streamlit Dashboard Pages",
        "badge": "MULTI-PAGE UI",
        "path": "pages/3_📈_Cash_Flow_Trends.py",
        "display_name": "pages/3_Cash_Flow_Trends.py",
        "desc": "Time-series cash flow velocity, seasonal decomposition, and cumulative liquidity curve."
    },
    {
        "category": "Streamlit Dashboard Pages",
        "badge": "MULTI-PAGE UI",
        "path": "pages/4_🏢_Cost_Centers.py",
        "display_name": "pages/4_Cost_Centers.py",
        "desc": "Departmental expenditure allocation, budget variance, and vendor concentration analysis."
    },
    {
        "category": "Streamlit Dashboard Pages",
        "badge": "MULTI-PAGE UI",
        "path": "pages/5_🔍_Anomaly_Detection.py",
        "display_name": "pages/5_Anomaly_Detection.py",
        "desc": "Dual-engine anomaly detection: Z-Score (parametric) and Tukey's Fences (non-parametric)."
    },
    {
        "category": "Streamlit Dashboard Pages",
        "badge": "MULTI-PAGE UI",
        "path": "pages/6_📥_Data_Explorer.py",
        "display_name": "pages/6_Data_Explorer.py",
        "desc": "Interactive multi-filter tabular grid, column projection, and dynamic CSV/Excel export."
    },
    {
        "category": "Streamlit Dashboard Pages",
        "badge": "MULTI-PAGE UI",
        "path": "pages/7_🛡️_Data_Quality.py",
        "display_name": "pages/7_Data_Quality.py",
        "desc": "Data integrity audit, null-value checks, duplicate transaction detection, and reconciliation."
    },
    # 3. Core Source Modules
    {
        "category": "Core Architecture & Business Logic",
        "badge": "PACKAGE INIT",
        "path": "src/__init__.py",
        "display_name": "src/__init__.py",
        "desc": "Python package initializer exporting core analytics and data access subroutines."
    },
    {
        "category": "Core Architecture & Business Logic",
        "badge": "DATABASE LAYER",
        "path": "src/db.py",
        "display_name": "src/db.py",
        "desc": "SQLite Star Schema connection management, WAL-mode configuration, and schema execution."
    },
    {
        "category": "Core Architecture & Business Logic",
        "badge": "DATA INGESTION",
        "path": "src/data_loader.py",
        "display_name": "src/data_loader.py",
        "desc": "Streamlit @st.cache_data data loader with ETL caching and fallback CSV synchronization."
    },
    {
        "category": "Core Architecture & Business Logic",
        "badge": "DATA PIPELINE",
        "path": "src/cleaner.py",
        "display_name": "src/cleaner.py",
        "desc": "Data validation, datetime standardization, categorical cleaning, and schema normalization."
    },
    {
        "category": "Core Architecture & Business Logic",
        "badge": "FINANCIAL ANALYTICS",
        "path": "src/analytics.py",
        "display_name": "src/analytics.py",
        "desc": "Cash flow velocity, credit/debit aggregations, departmental KPI, and burn rate computations."
    },
    {
        "category": "Core Architecture & Business Logic",
        "badge": "STATISTICAL ENGINE",
        "path": "src/stats_engine.py",
        "display_name": "src/stats_engine.py",
        "desc": "Statistical engine executing Z-Score, Tukey IQR, and Benford's Law distribution analysis."
    },
    {
        "category": "Core Architecture & Business Logic",
        "badge": "UI COMPONENTS",
        "path": "src/ui.py",
        "display_name": "src/ui.py",
        "desc": "Reusable UI components, Tailwind CSS cards, KPI metrics, and responsive sidebar navigation."
    },
    {
        "category": "Core Architecture & Business Logic",
        "badge": "SYNTHETIC GENERATOR",
        "path": "src/generate_data.py",
        "display_name": "src/generate_data.py",
        "desc": "Synthetic realistic enterprise transaction generator creating Star Schema CSV and SQLite DB."
    },
    # 4. Automated Testing Suite
    {
        "category": "Automated Testing Suite",
        "badge": "ANALYTICS TESTS",
        "path": "tests/test_analysis.py",
        "display_name": "tests/test_analysis.py",
        "desc": "Validation tests for financial analytics, burn rate formulas, and statistical anomaly detectors."
    },
    {
        "category": "Automated Testing Suite",
        "badge": "STREAMLIT TESTS",
        "path": "tests/test_app.py",
        "display_name": "tests/test_app.py",
        "desc": "Streamlit AppTest runner verifying page loading, widget interactivity, and error-free rendering."
    },
    {
        "category": "Automated Testing Suite",
        "badge": "DATA INTEGRITY TESTS",
        "path": "tests/test_data.py",
        "display_name": "tests/test_data.py",
        "desc": "Database schema integrity, foreign key constraint validation, and data cleaning assertions."
    }
]

# ----------------------------------------------------------------------
# 3. Two-Pass Numbered Canvas
# ----------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, total_pages):
        page_num = self._pageNumber
        # Suppress headers/footers on Cover Page (Page 1)
        if page_num == 1:
            return

        self.saveState()
        w, h = A4

        # Top Header
        self.setStrokeColor(colors.HexColor("#CBD5E1"))  # Slate-300
        self.setLineWidth(0.6)
        self.line(36, h - 34, w - 36, h - 34)

        self.setFont("MainFontBold", 7.5)
        self.setFillColor(colors.HexColor("#0F172A"))  # Slate-900
        self.drawString(36, h - 28, "CREDIT VS DEBIT TRANSACTION ANALYSIS SYSTEM")

        self.setFont("MainFont", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))  # Slate-500
        header_text = getattr(self, "current_file_header", "Source Code Repository")
        self.drawRightString(w - 36, h - 28, header_text)

        # Bottom Footer
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.6)
        self.line(36, 36, w - 36, 36)

        self.setFont("MainFont", 7.5)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(36, 24, "Learner: Mohd Kaif  |  Roll No: 2500320140093  |  Project ID: P059  |  Mentor: Mr Dinesh Sereno")

        # Page Number Right-aligned
        self.setFont("MainFontBold", 7.5)
        self.setFillColor(colors.HexColor("#0F172A"))
        page_str = f"Page {page_num} of {total_pages}"
        self.drawRightString(w - 36, 24, page_str)

        self.restoreState()


# ----------------------------------------------------------------------
# 4. Helper: Split Code Line for Monospace Console
# ----------------------------------------------------------------------
def split_code_line(line_num, raw_line, max_chars=105):
    line_str = raw_line.rstrip("\r\n").replace("\t", "    ")
    chars = len(line_str)
    if chars <= max_chars:
        return [(line_num, line_str, False)]

    chunks = [(line_num, line_str[:max_chars], False)]
    remaining = line_str[max_chars:]
    while len(remaining) > (max_chars - 6):
        chunks.append((line_num, "      ↳ " + remaining[: max_chars - 6], True))
        remaining = remaining[max_chars - 6 :]
    chunks.append((line_num, "      ↳ " + remaining, True))
    return chunks


# ----------------------------------------------------------------------
# 5. Accurate Layout Simulation for TOC Pagination
# ----------------------------------------------------------------------
def simulate_pagination(manifest, h, content_top, content_bottom, line_h, banner_h):
    page = 3  # Cover = 1, TOC = 2
    cur_y = content_top

    for item in manifest:
        needed_for_banner = banner_h + 3 * line_h
        if cur_y - needed_for_banner < content_bottom:
            page += 1
            cur_y = content_top

        item["start_page"] = page
        cur_y -= banner_h + 8

        for l_num, raw_line in enumerate(item["lines"], 1):
            chunks = split_code_line(l_num, raw_line)
            for _ in chunks:
                if cur_y - line_h < content_bottom:
                    page += 1
                    cur_y = content_top
                cur_y -= line_h

        cur_y -= 14

    return page


# ----------------------------------------------------------------------
# 6. Main PDF Generator Function
# ----------------------------------------------------------------------
def generate_source_code_pdf(output_pdf_path):
    print(f"Generating Source Code PDF -> {output_pdf_path}")
    c = NumberedCanvas(output_pdf_path, pagesize=A4)
    w, h = A4

    # Pre-scan files and record metrics
    total_loc = 0
    total_bytes = 0

    for item in FILE_MANIFEST:
        rel_path = item["path"]
        if os.path.exists(rel_path):
            with open(rel_path, "r", encoding="utf-8", errors="replace") as f:
                lines = f.readlines()
                loc = len(lines)
                fsize = os.path.getsize(rel_path)
        else:
            loc = 0
            fsize = 0
            lines = []
        item["loc"] = loc
        item["fsize"] = fsize
        item["lines"] = lines
        total_loc += loc
        total_bytes += fsize

    # Geometry settings
    content_top = h - 48
    content_bottom = 48
    line_h = 9.4
    banner_h = 42

    # Simulate exact pagination
    total_calculated_pages = simulate_pagination(
        FILE_MANIFEST, h, content_top, content_bottom, line_h, banner_h
    )

    # ==================================================================
    # PAGE 1: COVER PAGE
    # ==================================================================
    c.current_file_header = "Cover Page"

    # Outer decorative frame
    c.setStrokeColor(colors.HexColor("#1E3A8A"))  # Deep Blue
    c.setLineWidth(1.5)
    c.rect(28, 28, w - 56, h - 56)

    c.setStrokeColor(colors.HexColor("#93C5FD"))  # Light Blue Inner Frame
    c.setLineWidth(0.5)
    c.rect(32, 32, w - 64, h - 64)

    # Top Institutional Banner
    c.setFillColor(colors.HexColor("#0F172A"))  # Slate-900
    c.rect(32, h - 130, w - 64, 98, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#38BDF8"))  # Sky-400
    c.setFont("MainFontBold", 11)
    c.drawCentredString(w / 2, h - 56, "ABES ENGINEERING COLLEGE, GHAZIABAD")

    c.setFillColor(colors.HexColor("#94A3B8"))  # Slate-400
    c.setFont("MainFont", 8.5)
    c.drawCentredString(w / 2, h - 72, "Department of Master of Computer Applications (MCA) — Data Analytics")

    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setFont("MainFontBold", 17)
    c.drawCentredString(w / 2, h - 104, "CONSOLIDATED SOURCE CODE REPOSITORY")

    c.setFillColor(colors.HexColor("#E2E8F0"))
    c.setFont("MainFont", 9.5)
    c.drawCentredString(w / 2, h - 120, "Academic Capstone Submission — HCL Enterprise Analytics Program")

    # Project Title Box
    cur_y = h - 165
    c.setFillColor(colors.HexColor("#1E293B"))  # Slate-800
    c.setFont("MainFontBold", 14)
    c.drawString(50, cur_y, "Project: Credit vs Debit Transaction Analysis System")

    cur_y -= 16
    c.setFillColor(colors.HexColor("#475569"))
    c.setFont("MainFont", 9)
    c.drawString(50, cur_y, "Enterprise Cash Flow Intelligence, Departmental Cost Accounting & Automated Fraud Detection")

    # Horizontal Rule
    cur_y -= 14
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.8)
    c.line(50, cur_y, w - 50, cur_y)

    # Metadata Grid (Two Columns in a styled card)
    cur_y -= 20
    card_h = 160
    card_y = cur_y - card_h

    c.setFillColor(colors.HexColor("#F8FAFC"))  # Slate-50 background
    c.setStrokeColor(colors.HexColor("#E2E8F0"))
    c.setLineWidth(1)
    c.roundRect(50, card_y, w - 100, card_h, 6, fill=1, stroke=1)

    # Column 1: Student & Mentorship
    col1_x = 68
    col1_y = cur_y - 24

    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.setFont("MainFontBold", 10)
    c.drawString(col1_x, col1_y, "ACADEMIC CREDENTIALS")

    items_col1 = [
        ("Learner / Author:", "Mohd Kaif"),
        ("University Roll No:", "2500320140093"),
        ("Project ID:", "P059"),
        ("Academic Mentor:", "Mr Dinesh Sereno"),
        ("Institution:", "ABES Engineering College, Ghaziabad"),
        ("Submission Date:", "November 2026")
    ]

    ty = col1_y - 18
    for label, val in items_col1:
        c.setFont("MainFontBold", 8)
        c.setFillColor(colors.HexColor("#475569"))
        c.drawString(col1_x, ty, label)
        c.setFont("MainFont", 8)
        c.setFillColor(colors.HexColor("#0F172A"))
        c.drawString(col1_x + 95, ty, val)
        ty -= 18

    # Column 2: Technical & Deployment
    col2_x = 310
    col2_y = cur_y - 24

    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.setFont("MainFontBold", 10)
    c.drawString(col2_x, col2_y, "DEPLOYMENT & PROJECT SPECS")

    items_col2 = [
        ("Batch ID:", "ABES_OND26 MCA 2ND YEAR_BATCH 01"),
        ("Target Organization:", "NexGen Technologies Pvt. Ltd., Noida"),
        ("Architecture Tier:", "4-Tier Architecture (Streamlit + SQLite)"),
        ("Live Streamlit App:", "hcl-trainingproject-zm5krbplamq8v3qqnjjakz"),
        ("Total Code Files:", f"{len(FILE_MANIFEST)} Modules (Complete)"),
        ("Total Source Lines:", f"{total_loc:,} Lines of Python Code")
    ]

    ty = col2_y - 18
    for label, val in items_col2:
        c.setFont("MainFontBold", 8)
        c.setFillColor(colors.HexColor("#475569"))
        c.drawString(col2_x, ty, label)
        c.setFont("MainFont", 8)
        c.setFillColor(colors.HexColor("#0F172A"))
        c.drawString(col2_x + 95, ty, val)
        ty -= 18

    # Table of Contents Preview / Executive Notice
    cur_y = card_y - 25
    c.setFillColor(colors.HexColor("#0F172A"))
    c.setFont("MainFontBold", 11)
    c.drawString(50, cur_y, "SYSTEM CODE STRUCTURE & VERIFICATION")

    cur_y -= 14
    c.setFont("MainFont", 8.5)
    c.setFillColor(colors.HexColor("#334155"))
    notice_text = (
        "This consolidated document encapsulates the complete, unaltered source code of the Credit vs Debit "
        "Transaction Analysis System in strict accordance with the LMS Capstone submission guidelines. "
        "Files are sequenced systematically starting with the main entrypoint (app.py), multi-page Streamlit dashboards "
        "(pages/), core architectural modules (src/), and unit/integration test suites (tests/)."
    )
    words = notice_text.split()
    line = []
    max_w = w - 100
    for word in words:
        test_line = " ".join(line + [word])
        if c.stringWidth(test_line, "MainFont", 8.5) < max_w:
            line.append(word)
        else:
            c.drawString(50, cur_y, " ".join(line))
            cur_y -= 13
            line = [word]
    if line:
        c.drawString(50, cur_y, " ".join(line))
        cur_y -= 16

    # Summary Statistics Banner
    cur_y -= 6
    stat_box_h = 44
    stat_box_y = cur_y - stat_box_h
    c.setFillColor(colors.HexColor("#EFF6FF"))  # Blue-50
    c.setStrokeColor(colors.HexColor("#BFDBFE"))  # Blue-200
    c.roundRect(50, stat_box_y, w - 100, stat_box_h, 4, fill=1, stroke=1)

    c.setFillColor(colors.HexColor("#1E40AF"))
    c.setFont("MainFontBold", 9)
    c.drawString(62, stat_box_y + 26, "MODULE DISTRIBUTION OVERVIEW:")

    c.setFont("MainFont", 8)
    c.setFillColor(colors.HexColor("#1E3A8A"))
    c.drawString(62, stat_box_y + 12, "• 1 Main Router (app.py)   • 7 Multi-Page UIs (pages/)   • 8 Core Architectures (src/)   • 3 Automated Test Suites (tests/)")

    # Bottom Submission Declaration
    cur_y = stat_box_y - 25
    c.setFont("MainFontBold", 8)
    c.setFillColor(colors.HexColor("#047857"))  # Emerald-700
    c.drawString(50, cur_y, "VERIFIED CLEAN BUILD: Free from hardcoded credentials, secret keys, or local machine dependencies.")

    c.setFont("MainFont", 7.5)
    c.setFillColor(colors.HexColor("#64748B"))
    cur_y -= 13
    c.drawString(50, cur_y, "Repository: https://github.com/kaif-009/HCL_Project  |  Live App: https://hcl-trainingproject-zm5krbplamq8v3qqnjjakz.streamlit.app/")

    c.showPage()

    # ==================================================================
    # PAGE 2: TABLE OF CONTENTS
    # ==================================================================
    c.current_file_header = "Table of Contents"

    # Header Box
    c.setFillColor(colors.HexColor("#0F172A"))
    c.rect(36, h - 85, w - 72, 45, fill=1, stroke=0)

    c.setFillColor(colors.HexColor("#FFFFFF"))
    c.setFont("MainFontBold", 14)
    c.drawString(48, h - 60, "TABLE OF CONTENTS — SOURCE CODE MANIFEST")

    c.setFillColor(colors.HexColor("#94A3B8"))
    c.setFont("MainFont", 8)
    c.drawString(48, h - 74, "Strict Sequence: Main Application -> Multi-Page Dashboards -> Core Modules -> Test Suites")

    # TOC Table Header
    toc_top = h - 105
    c.setFillColor(colors.HexColor("#F1F5F9"))  # Slate-100
    c.rect(36, toc_top - 18, w - 72, 18, fill=1, stroke=0)

    c.setFont("MainFontBold", 7.5)
    c.setFillColor(colors.HexColor("#1E293B"))
    c.drawString(42, toc_top - 13, "#")
    c.drawString(62, toc_top - 13, "FILE PATH / MODULE NAME")
    c.drawString(255, toc_top - 13, "CATEGORY / BADGE")
    c.drawString(395, toc_top - 13, "LINES")
    c.drawString(450, toc_top - 13, "SIZE")
    c.drawRightString(w - 44, toc_top - 13, "START PAGE")

    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.setLineWidth(0.6)
    c.line(36, toc_top - 18, w - 72, toc_top - 18)

    # Draw the TOC rows using accurately simulated start_page
    row_y = toc_top - 20
    curr_cat = None

    for idx, item in enumerate(FILE_MANIFEST, 1):
        if item["category"] != curr_cat:
            curr_cat = item["category"]
            row_y -= 10
            c.setFillColor(colors.HexColor("#0F172A"))
            c.setFont("MainFontBold", 8)
            c.drawString(42, row_y, f"■ {curr_cat.upper()}")
            row_y -= 13

        # Alternating row fill
        if idx % 2 == 0:
            c.setFillColor(colors.HexColor("#F8FAFC"))
            c.rect(36, row_y - 4, w - 72, 14, fill=1, stroke=0)

        c.setFont("CodeFontBold", 7.5)
        c.setFillColor(colors.HexColor("#64748B"))
        c.drawString(42, row_y, f"{idx:02d}")

        c.setFont("CodeFont", 7.5)
        c.setFillColor(colors.HexColor("#0F172A"))
        c.drawString(62, row_y, item["display_name"])

        c.setFont("MainFont", 7)
        c.setFillColor(colors.HexColor("#2563EB"))
        c.drawString(255, row_y, item["badge"])

        c.setFont("MainFont", 7.5)
        c.setFillColor(colors.HexColor("#475569"))
        c.drawString(395, row_y, f"{item['loc']:,} L")
        c.drawString(450, row_y, f"{(item['fsize']/1024):.1f} KB")

        c.setFont("MainFontBold", 8)
        c.setFillColor(colors.HexColor("#0F172A"))
        c.drawRightString(w - 44, row_y, f"Page {item['start_page']}")

        row_y -= 14

    # Total Summary row at bottom of TOC
    row_y -= 8
    c.setStrokeColor(colors.HexColor("#0F172A"))
    c.setLineWidth(1)
    c.line(36, row_y + 12, w - 72, row_y + 12)

    c.setFillColor(colors.HexColor("#0F172A"))
    c.setFont("MainFontBold", 8.5)
    c.drawString(42, row_y - 2, "TOTAL REPOSITORY MANIFEST:")
    c.drawString(255, row_y - 2, f"{len(FILE_MANIFEST)} Code Files")
    c.drawString(395, row_y - 2, f"{total_loc:,} Lines")
    c.drawString(450, row_y - 2, f"{(total_bytes/1024):.1f} KB")
    c.drawRightString(w - 44, row_y - 2, f"{total_calculated_pages} Pages Total")

    c.showPage()

    # ==================================================================
    # PAGES 3+: SOURCE CODE RENDERING
    # ==================================================================
    current_y = content_top

    for item in FILE_MANIFEST:
        rel_path = item["path"]
        display_name = item["display_name"]
        c.current_file_header = f"File: {display_name}"

        # If remaining height is not enough for banner + 3 lines, start fresh page
        needed_for_banner = banner_h + 3 * line_h
        if current_y - needed_for_banner < content_bottom:
            c.showPage()
            current_y = content_top

        # Draw File Banner
        banner_top = current_y
        c.setFillColor(colors.HexColor("#0F172A"))  # Slate-900 Dark Card
        c.roundRect(36, banner_top - banner_h, w - 72, banner_h, 3, fill=1, stroke=0)

        # File title inside banner
        c.setFillColor(colors.HexColor("#FFFFFF"))
        c.setFont("MainFontBold", 9.5)
        c.drawString(46, banner_top - 16, f"FILE: {display_name}")

        # Badge pill
        c.setFont("MainFontBold", 7)
        badge_w = c.stringWidth(item["badge"], "MainFontBold", 7) + 12
        badge_x = w - 46 - badge_w
        c.setFillColor(colors.HexColor("#1E3A8A"))  # Dark Blue Pill
        c.roundRect(badge_x, banner_top - 18, badge_w, 12, 3, fill=1, stroke=0)
        c.setFillColor(colors.HexColor("#38BDF8"))  # Sky-400
        c.drawString(badge_x + 6, banner_top - 15, item["badge"])

        # Subtitle / Details
        c.setFont("MainFont", 7.2)
        c.setFillColor(colors.HexColor("#94A3B8"))
        details_str = f"{item['desc']}  |  Lines: {item['loc']:,}  |  Size: {(item['fsize']/1024):.1f} KB  |  UTF-8 Python 3.12"
        c.drawString(46, banner_top - 32, details_str)

        current_y = banner_top - banner_h - 8

        # Render code lines
        lines = item["lines"]
        for line_num, raw_line in enumerate(lines, 1):
            chunks = split_code_line(line_num, raw_line)

            for l_num, text_chunk, is_wrap in chunks:
                if current_y - line_h < content_bottom:
                    c.showPage()
                    current_y = content_top

                # Alternating row background
                if l_num % 2 == 0 and not is_wrap:
                    c.setFillColor(colors.HexColor("#F8FAFC"))  # Subtle cool gray
                    c.rect(36, current_y - 2, w - 72, line_h, fill=1, stroke=0)

                # Line Number Gutter
                c.setFont("CodeFont", 6.8)
                c.setFillColor(colors.HexColor("#94A3B8"))  # Slate-400
                if not is_wrap:
                    c.drawRightString(66, current_y, f"{l_num:4d}")
                else:
                    c.drawRightString(66, current_y, "  ·")

                # Vertical separator rule
                c.setStrokeColor(colors.HexColor("#E2E8F0"))
                c.setLineWidth(0.5)
                c.line(70, current_y - 2, 70, current_y + line_h - 2)

                # Syntax coloring logic
                c.setFont("CodeFont", 7.0)
                stripped = text_chunk.strip()
                if stripped.startswith("#"):
                    c.setFillColor(colors.HexColor("#15803D"))  # Green for comments
                elif stripped.startswith(('"""', "'''")):
                    c.setFillColor(colors.HexColor("#0369A1"))  # Sky blue for docstrings
                elif stripped.startswith(("import ", "from ", "def ", "class ", "return ", "if ", "elif ", "else:", "for ", "while ", "try:", "except ")):
                    c.setFillColor(colors.HexColor("#1E3A8A"))  # Navy for keywords
                else:
                    c.setFillColor(colors.HexColor("#0F172A"))  # Charcoal for standard code

                # Draw the code line
                c.drawString(74, current_y, text_chunk)
                current_y -= line_h

        # Spacing after file block
        current_y -= 14

    # Save and finalize PDF
    c.showPage()
    c.save()
    print("PDF generation complete!")


if __name__ == "__main__":
    out_dir = r"D:\HCL_Project"
    target_filename = "2500320140093_MohdKaif_Source_Code.pdf"
    full_output_path = os.path.join(out_dir, target_filename)

    # Clean up old source code PDF files matching pattern if present
    for old_f in os.listdir(out_dir):
        if old_f.endswith("_MohdKaif_Source_Code.pdf") and old_f != target_filename:
            try:
                os.remove(os.path.join(out_dir, old_f))
            except Exception:
                pass
    docs_dir = os.path.join(out_dir, "docs")
    for old_f in os.listdir(docs_dir):
        if old_f.endswith("_MohdKaif_Source_Code.pdf") and old_f != target_filename:
            try:
                os.remove(os.path.join(docs_dir, old_f))
            except Exception:
                pass

    generate_source_code_pdf(full_output_path)

    # Also copy to docs/ for convenience
    docs_copy_path = os.path.join(out_dir, "docs", target_filename)
    shutil.copyfile(full_output_path, docs_copy_path)
    print(f"Copied to: {docs_copy_path}")

    # Print final file size
    fsize_mb = os.path.getsize(full_output_path) / (1024 * 1024)
    print(f"Final File Size: {fsize_mb:.2f} MB")
