# BUILD PLAN — Credit vs Debit Transaction Analysis System

**Project:** Credit vs Debit Transaction Analysis System  
**Organization:** NexGen Technologies Pvt. Ltd., Noida (500-Employee IT Services Firm)  
**Learner / Author:** Mohd Kaif (University Roll No: 2503201450093)  
**Program:** Master of Computer Applications (MCA) — 2nd Year Data Analytics  
**Institution:** ABES Engineering College, Ghaziabad  
**Academic Mentor:** Prof. Shilpa Tyagi  
**Target Environment:** Python 3.12 | Streamlit Multipage | Tailwind CSS CDN | SQLite 3 | Plotly  
**Document Version:** 1.0 (Baselined for Step 15 Implementation)  
**Tracking Code:** `BUILD-PLAN-v1.0-2026-11`

---

## 1. Project Summary (10 Lines) & Document Links

### 10-Line Executive Summary
1. **Domain & Organization:** A specialized enterprise financial analytics platform engineered for NexGen Technologies Pvt. Ltd., Noida, monitoring departmental operational expenditure and liquidity.
2. **Student & Academic Affiliation:** Authored by Mohd Kaif (Roll No: 2503201450093), MCA 2nd Year Data Analytics, ABES Engineering College, under the mentorship of Prof. Shilpa Tyagi.
3. **Core Problem:** Fragmented banking records, delayed reconciliation cycles (45+ days), unchecked departmental budget overruns, and vulnerability to duplicate or anomalous disbursements.
4. **Delivered Solution:** An interactive, multi-page financial intelligence web application powered by Streamlit and styled with Tailwind CSS, offering real-time visibility into cash flow dynamics.
5. **Architectural Foundation:** Decoupled 4-tier pipeline (Storage $\rightarrow$ Ingestion & Validation $\rightarrow$ Analytics & Statistical Engine $\rightarrow$ Presentation Layer) operating on an ACID-compliant SQLite star schema.
6. **Dataset Scale & Realism:** 302 transactions (Q1–Q3 2024) across 8 corporate accounts, 8 expense/revenue categories, 25 merchants, and 5 business departments with embedded business patterns and edge anomalies.
7. **Statistical Intelligence:** Dual-algorithm anomaly detection leveraging Parametric Z-Score ($|Z| > 3.0$) and Non-Parametric Tukey's Fences ($Q3 + 1.5 \times IQR$) for automated cash leak prevention.
8. **UI & Data Quality:** 7 responsive screens equipped with executive KPI metric cards, Plotly financial charts, dynamic multi-filter bindings, and automated data quality audits.
9. **Rigorous Quality Gate:** 100% verified Requirements Traceability Matrix (RTM) linking 10 OQs, 10 HMWs, 12 BRs, 13 Features, 15 User Stories, 8 UI screens, and 26 Test Cases (14 Functional, 12 Technical).
10. **Target SLA:** Sub-3-second page load latency, zero-configuration local execution, and seamless deployment on Streamlit Community Cloud.

### Project Document Artifact Links
Every phase of the project lifecycle has been documented and baselined:
- **Step 01:** [Project Understanding & Objectives](file:///d:/HCL_Project/Step_01_Project_Understanding.docx) | [Project Understanding Legacy Doc](file:///d:/HCL_Project/01_mohd_kaif_project_understanding.doc)
- **Step 02:** [How Might We (HMW) Statements](file:///d:/HCL_Project/docs/02_HMW_Statements.docx)
- **Step 03:** [Needs Analysis & Business Requirements](file:///d:/HCL_Project/docs/03_Needs_Analysis.docx)
- **Step 04:** [Requirements Traceability Matrix (RTM)](file:///d:/HCL_Project/docs/04_Traceability_Matrix.xlsx)
- **Step 05:** [Business Requirements Document (BRD)](file:///d:/HCL_Project/docs/05_BRD.docx)
- **Step 07:** [Technical Requirements Document (TRD)](file:///d:/HCL_Project/docs/07_TRD.docx)
- **Step 08:** [Database Design & Data Dictionary](file:///d:/HCL_Project/docs/08_Database_Design.xlsx)
- **Step 09:** [Entity-Relationship (ER) Diagram Document](file:///d:/HCL_Project/docs/09_ER_Diagram.docx) | [High-Res ER Diagram PNG](file:///d:/HCL_Project/docs/09_ER_Diagram.png)
- **Step 10:** [Synthetic Master Dataset Excel](file:///d:/HCL_Project/data/credit_debit_data.xlsx) | [SQLite Database (`app.db`)](file:///d:/HCL_Project/data/app.db) | [Data Generation Engine](file:///d:/HCL_Project/src/generate_data.py)
- **Step 11:** [User Stories & Sprint Backlog](file:///d:/HCL_Project/docs/11_User_Stories.docx)
- **Step 12:** [UI Framework & Wireframes](file:///d:/HCL_Project/docs/12_UI_Framework.docx) | [Theme Config](file:///d:/HCL_Project/.streamlit/config.toml) | [UI Components](file:///d:/HCL_Project/src/ui.py)
- **Step 13:** [Test Cases Specification](file:///d:/HCL_Project/docs/13_Test_Cases.docx) | [Automated Test Suite Directory](file:///d:/HCL_Project/tests)
- **Step 16:** [Streamlit Community Cloud Deployment Guide](file:///d:/HCL_Project/docs/16_DEPLOYMENT_GUIDE.docx) | [Live Application](https://2503201450093-credit-debit-analytics.streamlit.app) | [1-Click Deploy](https://share.streamlit.io/deploy?repository=Kaif-Specs/HCL-Training_Project&branch=main&mainModule=app.py)

---

## 2. Final Folder Structure

```text
d:\HCL_Project\
│
├── .streamlit/
│   └── config.toml                  # Streamlit custom theme (Slate 900 / Royal Blue palette)
│
├── data/
│   ├── app.db                       # Production SQLite DB (5 tables, indexes, 35-col analytical view)
│   ├── credit_debit_data.xlsx       # Comprehensive 6-sheet Excel workbook of database tables
│   ├── dim_accounts.csv             # 8 corporate bank/credit accounts
│   ├── dim_categories.csv           # 8 standard financial transaction categories
│   ├── dim_departments.csv          # 5 organizational cost centers with quarterly budgets
│   ├── dim_merchants.csv            # 25 corporate vendors, clients, and utility providers
│   └── fact_transactions.csv        # 302 granular credit/debit transaction records
│
├── docs/
│   ├── 02_HMW_Statements.docx       # Step 2: 10 HMW statements & prioritization
│   ├── 03_Needs_Analysis.docx       # Step 3: BR-01 to BR-12, MoSCoW breakdown
│   ├── 04_Traceability_Matrix.xlsx  # Step 4, 8, 11, 12, 13: 100% completed RTM workbook
│   ├── 05_BRD.docx                  # Step 5: Full Business Requirements Document
│   ├── 07_TRD.docx                  # Step 7: Full Technical Requirements Document
│   ├── 08_Database_Design.xlsx      # Step 8: Complete schema, data dictionary, DDL
│   ├── 09_ER_Diagram.docx           # Step 9: ER Diagram doc with cardinality analysis
│   ├── 09_ER_Diagram.png            # Step 9: High-resolution (300 DPI) ER diagram visual
│   ├── 11_User_Stories.docx         # Step 11: 15 User Stories with Gherkin acceptance criteria
│   ├── 12_UI_Framework.docx         # Step 12: Wireframes, Tailwind classes, design guidelines
│   ├── 13_Test_Cases.docx           # Step 13: 14 Functional & 12 Technical test cases
│   └── 14_BUILD_PLAN.docx           # Step 14: This Build Plan document in Word format
│
├── pages/                           # Streamlit Multipage Application Directory
│   ├── 1_📊_Executive_Summary.py    # Screen UI-01: Executive KPI cards, Cash flow waterfall, donut
│   ├── 2_💳_Credit_vs_Debit.py      # Screen UI-02: Volume vs value comparison, payment modes
│   ├── 3_📈_Cash_Flow_Trends.py     # Screen UI-03: Monthly temporal trend, 30-day moving avg
│   ├── 4_🏢_Cost_Centers.py         # Screen UI-04: Departmental budget utilization & variance
│   ├── 5_🔍_Anomaly_Detection.py    # Screen UI-05: Z-Score & Tukey IQR outliers, vendor Pareto
│   ├── 6_📥_Data_Explorer.py        # Screen UI-06: Interactive multi-filter grid & CSV export
│   └── 7_🛡️_Data_Quality.py         # Screen UI-07: Health score, duplicate & null audit log
│
├── src/                             # Core Python Application Modules
│   ├── __init__.py                  # Package marker
│   ├── analytics.py                 # Financial KPI formulations & aggregation logic
│   ├── cleaner.py                   # Data sanitization, deduplication, imputation engine
│   ├── data_loader.py               # st.cache_data database queries & view loading
│   ├── db.py                        # SQLite connection manager (WAL mode, foreign keys ON)
│   ├── generate_data.py             # Synthetic data generator script with business patterns
│   ├── stats_engine.py              # Z-Score & Tukey IQR statistical anomaly algorithms
│   └── ui.py                        # Reusable Tailwind CDN UI components & Plotly styler
│
├── tests/                           # Automated Verification Suite
│   ├── __init__.py                  # Package marker
│   ├── test_analysis.py             # Unit tests for KPI calculations & statistical routines
│   ├── test_app.py                  # Integration tests for Streamlit AppTest & page routing
│   └── test_data.py                 # Ingestion, schema integrity, and cleaning tests
│
├── app.py                           # Application Gateway, Session State, & Navigation
├── BUILD_PLAN.md                    # AI Build Roadmap & Execution Blueprint (This File)
├── README.md                        # Production Repository Documentation & Setup Guide
├── requirements.txt                 # Pinned Python package dependencies
└── Step_01_Project_Understanding.docx # Initial kickoff project understanding document
```

---

## 3. Sequential Build Tasks (BUILD-01 to BUILD-13)

### Task Overview Matrix

| Task ID | Task Goal | Primary Target Files | Linked Feature / US | Verification / Passing Tests |
| :--- | :--- | :--- | :--- | :--- |
| **BUILD-01** | Environment Setup & Pinned Dependencies | `requirements.txt`, `.streamlit/config.toml` | F-12 / US-01 | TC-T-09 |
| **BUILD-02** | Database Connectivity & Ingestion Connector | `src/db.py`, `src/data_loader.py` | F-01 / US-01 | TC-T-01, TC-T-02, TC-T-03, TC-T-04 |
| **BUILD-03** | Data Cleansing, Imputation & Deduplication | `src/cleaner.py` | F-10 / US-14 | TC-T-05, TC-F-12 |
| **BUILD-04** | Financial Analytics Engine & KPI Logic | `src/analytics.py` | F-02, F-03, F-04 / US-02, US-03 | TC-T-06, TC-F-02, TC-F-03 |
| **BUILD-05** | Statistical Engine (Z-Score & Tukey IQR) | `src/stats_engine.py` | F-06, F-07 / US-07, US-08 | TC-T-07, TC-F-06 |
| **BUILD-06** | Tailwind CSS UI Components & Chart Styler | `src/ui.py` | F-01..F-11 / US-01..US-15 | TC-F-01 |
| **BUILD-07** | Gateway Application & Executive Summary Screen | `app.py`, `pages/1_📊_Executive_Summary.py` | F-01, F-02 / US-01, US-02 | TC-F-01, TC-F-02, TC-T-08, TC-T-09 |
| **BUILD-08** | Credit vs Debit & Cash Flow Trend Screens | `pages/2_💳_Credit_vs_Debit.py`, `pages/3_📈_Cash_Flow_Trends.py` | F-03, F-04 / US-03, US-04, US-05 | TC-F-03, TC-F-04 |
| **BUILD-09** | Departmental Cost Centers & Budget Screen | `pages/4_🏢_Cost_Centers.py` | F-05 / US-06 | TC-F-05 |
| **BUILD-10** | Anomaly Detection & Vendor Concentration Screen| `pages/5_🔍_Anomaly_Detection.py` | F-06, F-07 / US-07, US-08, US-09 | TC-F-06, TC-F-07 |
| **BUILD-11** | Data Explorer & Data Quality Audit Screens | `pages/6_📥_Data_Explorer.py`, `pages/7_🛡️_Data_Quality.py` | F-08, F-09, F-10 / US-10..US-14 | TC-F-08..TC-F-12 |
| **BUILD-12** | Comprehensive Test Suite Execution | `tests/` | F-12 / All US | All 14 TC-F & 12 TC-T Passed |
| **BUILD-13** | Documentation, Packaging & Deployment Prep | `README.md`, `.gitignore`, `docs/14_BUILD_PLAN.docx` | F-13 / US-15 | TC-F-14 |

---

### Detailed Task Specifications

#### BUILD-01: Environment Setup & Pinned Dependencies
- **Goal:** Establish a reproducible Python 3.12 execution environment with strictly pinned dependencies and ensure the Streamlit visual theme matches corporate slate-900 / royal blue guidelines.
- **Files:** `requirements.txt`, `.streamlit/config.toml`
- **User Stories & Feature IDs:** Feature `F-12` (System Reliability), User Story `US-01`.
- **Exact Prompt for AI:**
  ```text
  Create requirements.txt with pinned production versions: pandas==2.2.1, numpy==1.26.4, scipy==1.12.0, statsmodels==0.14.1, plotly==5.19.0, streamlit==1.32.0, pytest==8.0.2. Ensure .streamlit/config.toml is configured with primaryColor="#2563EB", backgroundColor="#F8FAFC", secondaryBackgroundColor="#FFFFFF", textColor="#0F172A", and font="sans serif".
  ```
- **How to Check It:** Run `python -c "import streamlit, pandas, plotly, scipy; print('Packages imported successfully')"` and verify `.streamlit/config.toml` exists.
- **Tests That Must Pass:** `TC-T-09` (Theme and environment stability).

---

#### BUILD-02: Database Engine, Connection Pool & Data Ingestion
- **Goal:** Implement thread-safe SQLite connection management with Write-Ahead Logging (WAL) and foreign key enforcement, coupled with an in-memory caching data loader for `view_transaction_analysis`.
- **Files:** `src/db.py`, `src/data_loader.py`
- **User Stories & Feature IDs:** Feature `F-01` (Database Connectivity), User Story `US-01`.
- **Exact Prompt for AI:**
  ```text
  Implement src/db.py providing get_db_connection(db_path='data/app.db') that enforces 'PRAGMA foreign_keys = ON;' and 'PRAGMA journal_mode = WAL;'. Implement src/data_loader.py with load_raw_data() and load_analysis_view() decorated with @st.cache_data(ttl=3600, show_spinner=False), returning a pandas DataFrame from view_transaction_analysis with proper datetime conversions for transaction_date.
  ```
- **How to Check It:** Run a python one-liner loading the view: verify it returns exactly 302 rows and 35 columns in under 20 milliseconds.
- **Tests That Must Pass:** `TC-T-01` (DB File Presence), `TC-T-02` (Row Count), `TC-T-03` (PK Uniqueness), `TC-T-04` (FK Integrity).

---

#### BUILD-03: Data Cleansing, Imputation & Deduplication Pipeline
- **Goal:** Build an automated data sanitization pipeline that detects exact duplicate transaction entries, imputes missing categorical attributes (`payment_method`), flags string anomalies, and outputs an audit log.
- **Files:** `src/cleaner.py`
- **User Stories & Feature IDs:** Feature `F-10` (Data Cleansing Engine), User Story `US-14`.
- **Exact Prompt for AI:**
  ```text
  Implement src/cleaner.py containing clean_transaction_data(df) -> tuple[pd.DataFrame, dict]. The cleaner must: (1) Identify and drop exact duplicate records on ['account_id', 'transaction_date', 'amount', 'transaction_type', 'merchant_id'] while logging removed IDs, (2) Impute missing 'payment_method' values with 'Unknown/Pending', (3) Strip leading/trailing whitespaces from category and merchant names, and (4) Return the cleaned DataFrame alongside an audit dictionary containing dropped duplicate count, imputed null count, and data health score.
  ```
- **How to Check It:** Input the raw 302 records into `clean_transaction_data()`; verify cleaned dataset contains 300 records, 0 nulls in `payment_method`, and audit logs exactly 2 dropped duplicates.
- **Tests That Must Pass:** `TC-T-05` (Cleansing Logic Test), `TC-F-12` (Data Quality Screen Audit).

---

#### BUILD-04: Financial Analytics Engine & Metric Calculations
- **Goal:** Implement the mathematical and financial formulation engine for high-level KPIs, category rollups, account balance tracking, and monthly aggregation.
- **Files:** `src/analytics.py`
- **User Stories & Feature IDs:** Features `F-02`, `F-03`, `F-04`, User Stories `US-02`, `US-03`, `US-04`.
- **Exact Prompt for AI:**
  ```text
  Implement src/analytics.py containing:
  1. compute_executive_kpis(df) returning total_credit, total_debit, net_burn, and outflow_ratio (debit/credit * 100), with zero-division handling.
  2. compute_category_breakdown(df) returning aggregated sums and percentages grouped by category_name and transaction_type.
  3. compute_account_balances(df) tracking current liquidity balance per account.
  4. compute_monthly_trends(df) returning monthly aggregated credit, debit, net cash flow, and 30-day rolling averages.
  ```
- **How to Check It:** Validate mathematical calculations against synthetic test vectors (e.g., Credit ₹15,000, Debit ₹7,500 $\rightarrow$ Net ₹+7,500, Ratio 50.0%).
- **Tests That Must Pass:** `TC-T-06` (Metric Formulation Pytest), `TC-F-02` (KPI Card Accuracy), `TC-F-03` (Breakdown Accuracy).

---

#### BUILD-05: Statistical Engine (Z-Score & Tukey IQR Outlier Detection)
- **Goal:** Implement dual statistical anomaly detection routines to highlight suspect, fraudulent, or high-variance financial disbursements.
- **Files:** `src/stats_engine.py`
- **User Stories & Feature IDs:** Features `F-06`, `F-07`, User Stories `US-07`, `US-08`.
- **Exact Prompt for AI:**
  ```text
  Implement src/stats_engine.py providing:
  1. detect_outliers_zscore(df, threshold=3.0) using scipy.stats.zscore on debit amounts; returns df with 'z_score' and boolean 'is_outlier_z'.
  2. detect_outliers_tukey(df, k=1.5) calculating Q1, Q3, and IQR on debit amounts, defining upper bound = Q3 + (k * IQR); returns df with 'is_outlier_tukey' and 'outlier_severity'.
  3. compute_vendor_pareto(df) calculating cumulative outflow percentages to identify the 80/20 vendor concentration curve.
  ```
- **How to Check It:** Run against `app.db` fact records; verify exactly 4 known extreme outliers ($Z > 3.0$) are flagged (TXN-000042, TXN-000118, TXN-000205, TXN-000289).
- **Tests That Must Pass:** `TC-T-07` (Statistical Anomaly Detection Test), `TC-F-06` (Anomaly Screen Verification).

---

#### BUILD-06: Tailwind CSS Reusable UI Components & Plotly Themer
- **Goal:** Develop responsive Tailwind CSS component wrappers rendered via `st.components.v1.html` and a centralized Plotly figure styling utility.
- **Files:** `src/ui.py`
- **User Stories & Feature IDs:** Features `F-01` through `F-11`, User Stories `US-01` through `US-15`.
- **Exact Prompt for AI:**
  ```text
  Implement src/ui.py containing:
  1. render_header(title, subtitle, badge_text) rendering an enterprise header with live timestamp and status badge via Tailwind CDN iframe.
  2. render_kpi_card(title, value, subtitle, change_pct, is_positive, icon) rendering an elevated KPI metric card with gradient borders.
  3. render_insight_box(title, text, level='info'|'warning'|'success') rendering alert callout boxes.
  4. apply_chart_theme(fig) injecting corporate dark-slate typography, transparent backgrounds, custom tooltip templates, and accessible color scales.
  ```
- **How to Check It:** Render each component in a standalone Streamlit script; verify Tailwind styles load from CDN without layout shift or container clipping.
- **Tests That Must Pass:** `TC-F-01` (Global Theme & Header Rendering).

---

#### BUILD-07: Gateway Application & Screen UI-01 (Executive Summary)
- **Goal:** Build the main application gateway (`app.py`) managing global session state, sidebar filters, and the flagship `pages/1_📊_Executive_Summary.py`.
- **Files:** `app.py`, `pages/1_📊_Executive_Summary.py`
- **User Stories & Feature IDs:** Features `F-01`, `F-02`, User Stories `US-01`, `US-02`.
- **Exact Prompt for AI:**
  ```text
  1. Build app.py configuring st.set_page_config(page_title="NexGen Financial Analytics", layout="wide", initial_sidebar_state="expanded"), initializing st.session_state for raw/cleaned data, and rendering home portal with navigation guide.
  2. Build pages/1_📊_Executive_Summary.py featuring:
     - Shared sidebar filter bindings (Date range, Account multi-select, Department filter).
     - 4 Top-level KPI cards (Total Credit Inflow, Total Debit Outflow, Net Burn/Savings, Outflow Ratio).
     - Plotly Cash Flow Waterfall chart illustrating starting balance, credits, debits, and closing liquidity.
     - Plotly Category Outflow Donut chart with percent share annotations.
  ```
- **How to Check It:** Launch `streamlit run app.py`; verify initial page load < 2.5 seconds, KPI cards display correct formatted INR values (₹), and filters update charts synchronously.
- **Tests That Must Pass:** `TC-F-01` (Dashboard Render), `TC-F-02` (KPI Cards), `TC-T-08` (AppTest Route), `TC-T-09` (Theme Load).

---

#### BUILD-08: Screen UI-02 (Credit vs Debit) & Screen UI-03 (Cash Flow Trends)
- **Goal:** Implement deep-dive financial screens comparing transaction volume versus monetary value and longitudinal monthly cash flow dynamics.
- **Files:** `pages/2_💳_Credit_vs_Debit.py`, `pages/3_📈_Cash_Flow_Trends.py`
- **User Stories & Feature IDs:** Features `F-03`, `F-04`, User Stories `US-03`, `US-04`, `US-05`.
- **Exact Prompt for AI:**
  ```text
  1. Build pages/2_💳_Credit_vs_Debit.py displaying:
     - Side-by-side comparative bar chart: Transaction Count vs Total Value for Credit vs Debit.
     - Payment Mode breakdown (NEFT, RTGS, Corporate Card, UPI, NetBanking).
     - Category-level ratio analysis table with conditional bar indicators.
  2. Build pages/3_📈_Cash_Flow_Trends.py displaying:
     - Monthly Inflow vs Outflow stacked/grouped bar chart (Jan - Sep 2024).
     - 30-Day Moving Average trend line identifying seasonal spikes (March tax outlays, September renewals).
     - Cumulative Net Liquidity line curve with zero-line reference.
  ```
- **How to Check It:** Navigate between screens; filter by "Corporate Card"; confirm charts isolate card transactions and highlight recurring vendor subscriptions.
- **Tests That Must Pass:** `TC-F-03` (Credit vs Debit Breakdown), `TC-F-04` (Cash Flow Trends).

---

#### BUILD-09: Screen UI-04 (Departmental Cost Centers & Budget Tracking)
- **Goal:** Build the departmental cost accounting screen evaluating operational expenditures against quarterly allocated budgets.
- **Files:** `pages/4_🏢_Cost_Centers.py`
- **User Stories & Feature IDs:** Feature `F-05`, User Story `US-06`.
- **Exact Prompt for AI:**
  ```text
  Build pages/4_🏢_Cost_Centers.py featuring:
  1. Departmental summary cards for Engineering, Marketing, Operations, HR, and Sales.
  2. Horizontal grouped bar chart comparing Allocated Budget (₹) vs Actual Spend (₹) per department.
  3. Budget Utilization Progress Gauges with dynamic status badges:
     - Normal (< 80% utilization - Green)
     - Warning (80% - 100% utilization - Amber)
     - Over-Budget (> 100% utilization - Red)
  4. Granular table listing expense categories driving each department's budget variance.
  ```
- **How to Check It:** Verify Engineering and Marketing show highest departmental outflows, with budget variance matching database records.
- **Tests That Must Pass:** `TC-F-05` (Department Cost Center Audit).

---

#### BUILD-10: Screen UI-05 (Statistical Anomaly Detection & Vendor Pareto)
- **Goal:** Deliver an audit screen highlighting suspicious disbursements via Z-score scatter plots, Tukey box plots, and vendor outflow concentration analysis.
- **Files:** `pages/5_🔍_Anomaly_Detection.py`
- **User Stories & Feature IDs:** Features `F-06`, `F-07`, User Stories `US-07`, `US-08`, `US-09`.
- **Exact Prompt for AI:**
  ```text
  Build pages/5_🔍_Anomaly_Detection.py incorporating:
  1. Interactive Scatter Plot (Transaction Date vs Amount) with color coding for normal vs outlier transactions ($|Z| > 3.0$).
  2. Interactive Tukey IQR slider allowing auditors to adjust sensitivity k (1.5 standard, 3.0 extreme).
  3. Suspect Transaction Audit Table with one-click CSV export for external forensic review.
  4. Vendor Outflow Concentration Pareto Chart (Top 10 Vendors by spend + cumulative percentage curve).
  ```
- **How to Check It:** Verify that adjusting the IQR slider dynamically recalculates outlier classifications in the table and plot without page reload errors.
- **Tests That Must Pass:** `TC-F-06` (Anomaly Detection), `TC-F-07` (Vendor Concentration).

---

#### BUILD-11: Screen UI-06 (Data Explorer) & Screen UI-07 (Data Quality Audit)
- **Goal:** Provide end-users with full tabular search/export capabilities and complete transparency over dataset health, null imputation, and duplicate removal.
- **Files:** `pages/6_📥_Data_Explorer.py`, `pages/7_🛡️_Data_Quality.py`
- **User Stories & Feature IDs:** Features `F-08`, `F-09`, `F-10`, User Stories `US-10` through `US-14`.
- **Exact Prompt for AI:**
  ```text
  1. Build pages/6_📥_Data_Explorer.py providing an interactive st.dataframe with column visibility toggles, text search, date filtering, and a one-click 'Download Filtered Data as CSV' button.
  2. Build pages/7_🛡️_Data_Quality.py featuring:
     - Overall Data Health Score widget (98.3%).
     - Missing Values Breakdown chart before and after imputation.
     - Duplicate Transaction Audit Table displaying dropped records.
     - Interactive toggle allowing the user to view 'Raw Ingested Data' vs 'Sanitized Analytical View'.
  ```
- **How to Check It:** Download a filtered CSV and verify file row count matches active table filter; toggle raw view and verify 2 duplicates appear in raw view and disappear in clean view.
- **Tests That Must Pass:** `TC-F-08` through `TC-F-12`.

---

#### BUILD-12: Comprehensive Automated Test Suite Execution
- **Goal:** Execute the full test suite using Python's `unittest` / `pytest` runners to ensure all mathematical, structural, and interface assertions pass without regression.
- **Files:** `tests/test_data.py`, `tests/test_analysis.py`, `tests/test_app.py`
- **User Stories & Feature IDs:** Feature `F-12`, User Stories `US-01` through `US-15`.
- **Exact Prompt for AI:**
  ```text
  Execute python -m unittest discover -s tests -v. Verify that all 14 functional test cases (TC-F-01 to TC-F-14) and 12 technical test cases (TC-T-01 to TC-T-12) pass with 0 failures, 0 errors, and total runtime under 1.0 second.
  ```
- **How to Check It:** Check console exit code is `0` and summary output reports `OK`.
- **Tests That Must Pass:** All 26 test cases (`TC-F-01..14`, `TC-T-01..12`).

---

#### BUILD-13: Production Packaging, Documentation & Deployment
- **Goal:** Package the repository with an informative, professional `README.md`, configure `.gitignore`, verify git clean status, and document Streamlit Community Cloud launch steps.
- **Files:** `README.md`, `.gitignore`, `docs/14_BUILD_PLAN.docx`
- **User Stories & Feature IDs:** Feature `F-13` (Production Documentation & Deployment), User Story `US-15`.
- **Exact Prompt for AI:**
  ```text
  Create production-ready README.md containing: Project Title & Badges, Academic Affiliation, Executive Summary, System Architecture Diagram (Mermaid), Key Screens Walkthrough, Installation & Local Run Commands, Test Suite Execution Commands, and Deployment Guide for Streamlit Community Cloud. Generate docs/14_BUILD_PLAN.docx matching OpenXML formatting standards.
  ```
- **How to Check It:** Inspect `README.md` rendering; ensure `.gitignore` excludes `__pycache__`, `.venv`, and temporary artifacts; check Word document exists and opens cleanly.
- **Tests That Must Pass:** `TC-F-14` (Deployment Readiness Verification).

---

## 4. Definition of Done (DoD)

To consider the implementation phase (Step 15) complete, the system must satisfy 100% of the following criteria:

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│                            DEFINITION OF DONE (DoD)                          │
├──────────────────────────────────────────────────────────────────────────────┤
│ 1. Business Requirements:                                                    │
│    • 100% of 'Must-Have' Requirements (BR-01 through BR-08) implemented.     │
│    • 100% of 'Should-Have' Requirements (BR-09 through BR-11) implemented.   │
│                                                                              │
│ 2. Automated Test Coverage:                                                  │
│    • 14/14 Functional Tests (TC-F-01 to TC-F-14) PASSING with 0 errors.     │
│    • 12/12 Technical Tests (TC-T-01 to TC-T-12) PASSING with 0 errors.       │
│    • Zero regressions across database, analytics, and UI routing layers.     │
│                                                                              │
│ 3. Performance & Latency SLAs:                                               │
│    • Initial dashboard page load time < 2.5 seconds (SLA target: < 3.0s).    │
│    • SQLite analytical view query execution time < 50 milliseconds.          │
│    • In-memory caching active via @st.cache_data for instant filter switches.│
│                                                                              │
│ 4. Code Quality & Security:                                                  │
│    • Zero hardcoded credentials, secret keys, or absolute file path bugs.    │
│    • Proper exception handling for database connectivity and empty queries.  │
│    • Modular code structure across src/, pages/, tests/, and data/.          │
│                                                                              │
│ 5. Documentation & Packaging:                                                │
│    • Complete README.md with architecture diagram and setup instructions.    │
│    • Fully baselined docs/14_BUILD_PLAN.docx and BUILD_PLAN.md.              │
│    • Clean repository state ready for Streamlit Community Cloud deployment.  │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Environment & Execution Commands

### A. Environment Installation
```powershell
# Step 1: Create and activate isolated Python virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Step 2: Install pinned production dependencies
pip install -r requirements.txt
```

### B. Launching the Web Application
```powershell
# Run the Streamlit Multipage Application locally
streamlit run app.py
```
*The application will automatically launch in your browser at `http://localhost:8501`.*

### C. Executing the Automated Test Suite
```powershell
# Option 1: Standard Library Unittest (Offline, zero dependencies)
python -m unittest discover -s tests -v

# Option 2: Pytest Runner with detailed execution summary
pytest -v --tb=short
```

### D. Re-generating Synthetic Data (If Needed)
```powershell
# Rebuild data/app.db, CSV files, and Excel workbook with random seed 42
python src/generate_data.py
```

---

## 6. Viva Notes: 10 Likely Questions with Crisp Technical Answers

### Q1: Why did you choose a Star Schema over a 3NF normalized schema for this project?
**Answer:** A Star Schema (`dim_accounts`, `dim_categories`, `dim_merchants`, `dim_departments` $\rightarrow$ `fact_transactions`) denormalizes dimensions around a central numerical fact table. For an OLAP analytics dashboard, this dramatically reduces complex multi-table SQL joins, simplifies aggregation queries, and enables sub-5 millisecond query execution through the pre-joined `view_transaction_analysis`.

---

### Q2: How did you implement dual anomaly detection, and why are both Z-Score and Tukey's Fences necessary?
**Answer:** Z-Score is a parametric method that assumes a normal distribution, flagging records with $|Z| > 3.0$ standard deviations from the mean. However, financial disbursements are notoriously right-skewed with heavy tails. Tukey’s Fences is non-parametric—it uses quartiles ($Q1, Q3$) and the Interquartile Range ($IQR$), defining upper outliers as values $> Q3 + 1.5 \times IQR$. Using both allows us to capture extreme mathematical outliers (Z-score) as well as operational spending anomalies resistant to distributional skew (Tukey).

---

### Q3: How do you achieve sub-3-second load times in Streamlit?
**Answer:** We utilize three primary optimizations:
1. **SQLite WAL Mode:** `PRAGMA journal_mode = WAL` enables concurrent readers without locking the database.
2. **Pre-joined Database Views & Indexes:** Foreign key B-Tree indexes on `account_id`, `category_id`, and `merchant_id`.
3. **Streamlit In-Memory Caching:** `@st.cache_data(ttl=3600)` caches the cleaned pandas DataFrame in memory, ensuring that user filter adjustments execute instant vector slicing in RAM without hitting the disk.

---

### Q4: How is Tailwind CSS integrated into Streamlit without breaking the Python framework?
**Answer:** Streamlit does not natively compile Tailwind classes. We embed Tailwind CSS via the official Tailwind CDN inside `st.components.v1.html(..., height=...)` containers. This allows us to craft modern responsive cards, gradient badges, and flexbox containers with custom typography while retaining Streamlit’s native Python plotting and filter widgets.

---

### Q5: How does the system handle data quality issues, such as missing values or duplicate entries?
**Answer:** In `src/cleaner.py`, the pipeline detects exact duplicates based on the compound key `['account_id', 'transaction_date', 'amount', 'transaction_type', 'merchant_id']` and logs them before dropping. Missing `payment_method` values are imputed with `'Unknown/Pending'` rather than discarding the transaction, preserving the integrity of total financial amounts while maintaining a 98.3% data health score.

---

### Q6: What is the purpose of the Requirements Traceability Matrix (RTM), and how was it maintained?
**Answer:** The RTM (`docs/04_Traceability_Matrix.xlsx`) provides end-to-end forward and backward traceability across the entire SDLC. It maps each Operational Question (OQ) to its corresponding HMW statement, Business Requirement (BR), Database Column, User Story (US), UI Screen, and automated Test Cases (TC-F and TC-T). Every requirement has at least one functional and technical test, guaranteeing zero unverified features.

---

### Q7: Why did you choose SQLite over PostgreSQL or MySQL for this analytical application?
**Answer:** SQLite is serverless, zero-configuration, and fully self-contained inside the repository (`data/app.db`). For an enterprise analytical dashboard handling 300 to 100,000 corporate records, SQLite provides ACID compliance, lightning-fast in-process queries (under 5 ms), and seamless portability for academic evaluation and Streamlit Community Cloud deployment without requiring external database provisioning.

---

### Q8: What business patterns were embedded in the synthetic dataset, and why?
**Answer:** Rather than generating pure random noise, we embedded 5 realistic corporate financial patterns:
1. **Weekend Volume Drop:** ~80% lower transaction frequency on non-business days.
2. **Quarterly Tax Outlays:** Large debit spikes at the close of Q1 and Q2.
3. **Monthly Payroll Run:** Concentrated credit outflows on the 28th–30th of each month.
4. **Cloud Infrastructure Invoices:** Recurring mid-month debit disbursements to AWS and Microsoft.
5. **Departmental Budget Variance:** Marketing and Engineering demonstrating seasonal spikes during campaign launches and infrastructure upgrades.

---

### Q9: How does the Pareto Analysis work on the Anomaly & Vendor screen?
**Answer:** The Pareto Principle (80/20 rule) in corporate finance states that ~80% of corporate cash outflows are concentrated among ~20% of top vendors. `compute_vendor_pareto()` aggregates total debit spend by merchant, sorts in descending order, and calculates a running cumulative percentage curve. This immediately identifies vendor concentration risk for procurement leaders.

---

### Q10: How do you verify that the Streamlit application does not crash when filters return an empty dataset?
**Answer:** Test case `TC-F-13` specifically tests the empty filter state. In each screen, before rendering KPI cards or Plotly charts, the code evaluates `if filtered_df.empty: st.warning("No transactions match the selected filter criteria."); st.stop()`. This prevents zero-division errors in ratio formulas and unhandled index exceptions in chart renderers.

---

## 7. Sign-Off & Verification

| Role | Name | Designation / Organization | Date | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Learner / Author** | Mohd Kaif | MCA 2nd Year, ABES Engineering College | 18-Nov-2026 | **APPROVED** |
| **Academic Mentor** | Prof. Shilpa Tyagi | Department of MCA, ABES Engineering College | 18-Nov-2026 | **REVIEWED** |
| **Industry Reviewer** | NexGen Technical Lead | Financial Analytics Division, NexGen Pvt. Ltd. | 18-Nov-2026 | **BASELINE ACCEPTED** |

---
*Ready for STEP 15: AI Build & Implementation.*
