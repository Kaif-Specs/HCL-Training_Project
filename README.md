# Credit vs Debit Transaction Analysis System
### Enterprise Cash Flow Intelligence, Departmental Cost Accounting & Automated Fraud Detection

[![Python 3.12](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Streamlit 1.32](https://img.shields.io/badge/Streamlit-1.32.0-FF4B4B.svg)](https://streamlit.io/)
[![SQLite 3](https://img.shields.io/badge/Database-SQLite%20Star%20Schema-003B57.svg)](https://sqlite.org/)
[![Tailwind CSS](https://img.shields.io/badge/Styling-Tailwind%20CSS%20v3-38B2AC.svg)](https://tailwindcss.com/)
[![Tests Passing](https://img.shields.io/badge/Tests-26%2F26%20Passing-success.svg)](file:///d:/HCL_Project/tests)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🏛️ Academic & Institutional Credentials
- **Learner / Author:** Mohd Kaif
- **University Roll Number:** `2503201450093`
- **Academic Program:** Master of Computer Applications (MCA) — 2nd Year Data Analytics
- **Institution:** ABES Engineering College, Ghaziabad
- **Academic Mentor:** Prof. Shilpa Tyagi
- **Target Organization:** NexGen Technologies Pvt. Ltd., Noida (500-Employee IT Services Firm)
- **Project Tracking Code:** `BUILD-PLAN-v1.0-2026-11`

---

## 📖 Executive Summary
The **Credit vs Debit Transaction Analysis System** is an enterprise-grade financial analytics platform developed for **NexGen Technologies Pvt. Ltd.** to resolve delayed reconciliation cycles (45+ days), unchecked departmental budget overruns, and vulnerability to duplicate or anomalous disbursements.

The system features an ACID-compliant **SQLite Star Schema** database, in-memory caching via `@st.cache_data` for sub-50ms analytical queries, and a modern multi-page **Streamlit** dashboard styled with **Tailwind CSS**. It incorporates dual-method anomaly detection (**Parametric Z-Score** and **Non-Parametric Tukey's Fences**) alongside **Pareto 80/20** vendor concentration analysis.

---

## 🏗️ 4-Tier System Architecture

```mermaid
flowchart TD
    subgraph Tier1["1. Storage & Persistence Tier"]
        DB[("data/app.db (SQLite3 WAL Mode)")]
        DIM1["dim_accounts (8 rows)"]
        DIM2["dim_categories (8 rows)"]
        DIM3["dim_departments (5 rows)"]
        DIM4["dim_merchants (25 rows)"]
        FACT["fact_transactions (302 rows)"]
        VIEW["view_transaction_analysis (35 columns)"]
        DIM1 & DIM2 & DIM3 & DIM4 --> FACT
        FACT --> VIEW
        VIEW --> DB
    end

    subgraph Tier2["2. Data Ingestion & Sanitization Tier"]
        LOADER["src/data_loader.py (@st.cache_data)"]
        CLEANER["src/cleaner.py (Deduplication & Imputation)"]
        DB --> LOADER
        LOADER --> CLEANER
    end

    subgraph Tier3["3. Analytics & Statistical Engine Tier"]
        ANALYTICS["src/analytics.py (KPIs, Cash Flow, Variance)"]
        STATS["src/stats_engine.py (Z-Score & Tukey IQR)"]
        CLEANER --> ANALYTICS
        CLEANER --> STATS
    end

    subgraph Tier4["4. Presentation & Visualization Tier"]
        UI["src/ui.py (Tailwind CDN Components)"]
        APP["app.py (Gateway Portal)"]
        P1["pages/1_📊_Executive_Summary.py"]
        P2["pages/2_💳_Credit_vs_Debit.py"]
        P3["pages/3_📈_Cash_Flow_Trends.py"]
        P4["pages/4_🏢_Cost_Centers.py"]
        P5["pages/5_🔍_Anomaly_Detection.py"]
        P6["pages/6_📥_Data_Explorer.py"]
        P7["pages/7_🛡️_Data_Quality.py"]
        
        ANALYTICS & STATS --> APP & P1 & P2 & P3 & P4 & P5 & P6 & P7
        UI --> P1 & P2 & P3 & P4 & P5 & P6 & P7
    end
```

---

## 🧭 Multi-Page Dashboard Modules

| Page ID | Module Name | Core Capabilities |
| :--- | :--- | :--- |
| **Portal** | `app.py` | Global session state, health scores, navigation hub, compliance notice. |
| **UI-01** | `1_📊_Executive_Summary.py` | Top-line KPI cards, Cash Flow Waterfall chart, Category Outflow Donut, Top 5 Transactions. |
| **UI-02** | `2_💳_Credit_vs_Debit.py` | Transaction volume vs monetary value dual bar chart, payment method channel breakdown. |
| **UI-03** | `3_📈_Cash_Flow_Trends.py` | Monthly Inflow vs Outflow stacked bars, 30-day moving average, cumulative liquidity curve. |
| **UI-04** | `4_🏢_Cost_Centers.py` | Budget vs Actual expenditure grouped bars, utilization progress gauges, variance ledger. |
| **UI-05** | `5_🔍_Anomaly_Detection.py` | Z-score scatter plot ($|Z| > 3.0$), Tukey IQR sensitivity slider, Pareto 80/20 vendor chart, CSV audit export. |
| **UI-06** | `6_📥_Data_Explorer.py` | Keyword search across all columns, multi-attribute filter grid, column selector, filtered CSV download. |
| **UI-07** | `7_🛡️_Data_Quality.py` | Data Health Score (98.3%), duplicate elimination audit log, missing values profile, raw vs clean toggle. |

---

## ⚡ Quickstart & Execution Guide

### 1. Clone & Set Up Environment
```powershell
# Clone the repository
git clone https://github.com/2503201450093-credit-debit-analytics.git
cd 2503201450093-credit-debit-analytics

# Create and activate Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install pinned dependencies
pip install -r requirements.txt
```

### 2. Launch the Application
```powershell
streamlit run app.py
```
*Access the interactive portal in your browser at: `http://localhost:8501`*

### 3. Run the Automated Test Suite
```powershell
# Run with Python standard library unittest runner
python -m unittest discover -s tests -v

# Run with Pytest runner
pytest -v --tb=short
```

---

## 🧪 Quality Gate & Test Coverage

The project is governed by a **100% verified Requirements Traceability Matrix (RTM)**:
- **14 Functional Tests (`TC-F-01` to `TC-F-14`):** Verifies all filters, KPI formulations, chart rendering, column visibility, and export routines.
- **12 Technical Tests (`TC-T-01` to `TC-T-12`):** Validates database connectivity, row counts, PK uniqueness, FK referential integrity, domain constraints, metric calculations, and sub-3-second load latency.

---

## 📂 Project Directory Structure

```text
d:\HCL_Project\
├── .streamlit/config.toml        # Custom Slate 900 / Royal Blue theme
├── data/
│   ├── app.db                   # SQLite Star Schema database
│   ├── credit_debit_data.xlsx   # 6-sheet Excel database workbook
│   └── *.csv                    # Dimension and Fact table CSV exports
├── docs/                        # Complete 14 SDLC Documents & Specifications
│   ├── 04_Traceability_Matrix.xlsx
│   ├── 05_BRD.docx
│   ├── 07_TRD.docx
│   ├── 08_Database_Design.xlsx
│   ├── 09_ER_Diagram.docx / .png
│   └── 14_BUILD_PLAN.docx
├── pages/                       # 7 Streamlit Multipage Analytical Screens
├── src/                         # Reusable Data, Cleaner, Analytics, Stats, & UI Modules
├── tests/                       # Complete automated test suite
├── app.py                       # Main application portal
├── BUILD_PLAN.md                # AI build roadmap
└── requirements.txt             # Pinned package dependencies
```

---

## 📜 Academic Mentor & Industry Sign-Off

| Role | Signatory | Affiliation / Organization | Status |
| :--- | :--- | :--- | :--- |
| **Learner** | Mohd Kaif | MCA 2nd Year, ABES Engineering College | **APPROVED** |
| **Academic Mentor** | Prof. Shilpa Tyagi | Department of MCA, ABES Engineering College | **REVIEWED** |
| **Enterprise Sponsor** | NexGen Technical Lead | Financial Analytics Division, NexGen Pvt. Ltd. | **ACCEPTED** |

---
*© 2026 Mohd Kaif. All Rights Reserved. Master of Computer Applications Capstone Project.*
