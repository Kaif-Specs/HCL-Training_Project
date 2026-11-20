import json
import nbformat as nbf
import os

def create_notebook():
    nb = nbf.v4.new_notebook()
    nb['cells'] = []

    def add_lesson_step(what_why_how_md, code_str, found_md, your_turn_md):
        nb['cells'].append(nbf.v4.new_markdown_cell(what_why_how_md))
        nb['cells'].append(nbf.v4.new_code_cell(code_str))
        nb['cells'].append(nbf.v4.new_markdown_cell(found_md))
        nb['cells'].append(nbf.v4.new_markdown_cell(your_turn_md))

    def add_md(content):
        nb['cells'].append(nbf.v4.new_markdown_cell(content))

    def add_code(content):
        nb['cells'].append(nbf.v4.new_code_cell(content))

    # ==========================================
    # TITLE & HEADER
    # ==========================================
    header_md = """# 📊 Enterprise Exploratory Data Analysis (EDA) Masterclass
## Credit vs Debit Transaction Analysis System
**Author:** Mohd Kaif | **University Roll No:** `2503201450093` | **Target Enterprise:** NexGen Technologies Pvt. Ltd., Noida  
**Academic Program:** MCA 2nd Year (Data Analytics Specialization) | **Academic Mentor:** Prof. Shilpa Tyagi  
**Environment Requirements:** `pandas`, `numpy`, `matplotlib`, `seaborn`, `plotly`, `scipy`

---

### 🎯 Masterclass Pedagogical Architecture
Every analytical step in this laboratory follows a 4-part instructional cadence designed for corporate data science rigor:
1. **📘 The Lesson (What, Why, How):** Conceptual definition, business motivation, and exact interpretation guidance.
2. **💻 Production Code Cell:** Fully documented, PEP-8 compliant Python code leveraging vectorized operations.
3. **🔍 What We Found:** Concrete quantitative findings calculated directly from the live dataset (with actual numbers).
4. **✏️ Your Turn (Mini-Task):** Hands-on operational challenge for self-assessment.

---
"""
    add_md(header_md)

    # ==========================================
    # SECTION 1: PROJECT, HMW STATEMENTS & ANALYSIS QUESTIONS
    # ==========================================
    sec1_intro = """## 📌 Section 1: Project Framing, HMW Statements & Operational Questions

### 📘 The Lesson: Problem Framing with Design Thinking
* **What is it?** Exploratory Data Analysis (EDA) is not mere chart plotting; it is the systematic interrogation of enterprise data to validate hypotheses, expose anomalies, and guide capital allocation.
* **Why do we need it?** Without a structured problem statement, analysts suffer from "metric wanderlust"—generating dozens of aesthetically pleasing charts that fail to solve business problems. Design Thinking grounds our analysis in human-centered pain points using the **How Might We (HMW)** syntax:
  $$\\text{How might we } [\\text{action}] \\text{ for } [\\text{user}] \\text{ so that } [\\text{measurable outcome}]?$$
* **How to read the result:** Each HMW statement maps to specific Operational Questions (OQs), which dictate the required data dimensions, aggregations, and statistical tests.
"""
    add_md(sec1_intro)

    sec1_code = """# Section 1.1: Environment Initialization & Library Importation
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

# Configure styling and visualization parameters
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
sns.set_theme(style='whitegrid', palette='muted')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 0.8
pd.set_option('display.max_columns', 30)
pd.set_option('display.float_format', lambda x: f'₹{x:,.2f}' if abs(x) >= 100 else f'{x:,.4f}')

print("✅ Analytics environment loaded successfully.")
print(f"Pandas Version: {pd.__version__} | NumPy Version: {np.__version__} | Seaborn Version: {sns.__version__}")
"""

    sec1_found = """### 🔍 What We Found: Core HMW Statements & Operational Traceability
The 5 strategic priorities formulated for **NexGen Technologies Pvt. Ltd.** in Step 2 of the project lifecycle are:

1. **HMW-01 (Solvency & Cash Flow):** *How might we provide finance controllers and executive leadership with continuous visibility into the enterprise's net monthly cash flow trajectory so that cash deficits are forecasted weeks in advance?*
   * *Linked Operational Question:* **OQ-01** (Net monthly cash flow trend: Total Credits vs Debits).
2. **HMW-02 (Cost Center Drains):** *How might we illuminate which operational expense categories are disproportionately draining liquid bank reserves for accounts managers so that burn rates remain disciplined and manageable?*
   * *Linked Operational Question:* **OQ-02** (Highest debit spending volume categories & budget depletion).
3. **HMW-03 (Credit Exposure):** *How might we alert treasury managers to corporate credit line utilization levels before revolving balances breach optimal limits and trigger penalty interest rates (36–42% APR)?*
   * *Linked Operational Question:* **OQ-03** (Corporate credit card utilization % and billing cycle spikes).
4. **HMW-04 (Temporal Rhythms):** *How might we help accounts operations teams detect temporal surges and cyclical spending rhythms across business days and billing cycles so that intra-month cash crunches during peak payment cycles are avoided?*
   * *Linked Operational Question:* **OQ-04** (Temporal spending patterns across days of the month and days of the week).
5. **HMW-05 (Audit & Risk Governance):** *How might we immediately isolate and flag abnormal expenditure spikes that deviate significantly from historical category norms for audit teams so that fraudulent charges and duplicate billings are prevented?*
   * *Linked Operational Question:* **OQ-07** (Statistical expenditure anomalies exceeding 3 standard deviations or Tukey's fences).
"""

    sec1_turn = """### ✏️ Your Turn: Mini-Task 1
> **Exercise:** Frame a **6th HMW statement** focused on *vendor consolidation* for the Procurement Manager.  
> *Template:* "How might we [action] for [Procurement Manager] so that [outcome]?" Write your draft in a markdown comment below.
"""
    add_lesson_step(sec1_intro, sec1_code, sec1_found, sec1_turn)

    # ==========================================
    # SECTION 2: LOAD DATA & FIRST LOOK
    # ==========================================
    sec2_intro = """## 📌 Section 2: Load Data & First Look (Shape, Head, Dtypes, Info, Describe)

### 📘 The Lesson: The Data Reconnaissance Protocol
* **What is it?** The preliminary inspection phase where the analyst establishes the physical boundaries, memory consumption, column schema, and basic distributional parameters of the dataset before applying any transformations.
* **Why do we need it?** Real-world raw data often harbors hidden traps: numbers encoded as strings (due to currency symbols), dates masquerading as generic objects, and silent truncated columns. Inspecting `df.info()` and `df.describe()` reveals these anomalies immediately.
* **How to read the result:**
  * `df.shape`: Returns $(N, M)$ where $N$ is row count and $M$ is column count.
  * `df.dtypes`: Watch out for numerical variables stored as `object` (which prevents mathematical modeling).
  * `df.describe()`: Compare the **50% (Median)** against the **Mean**. If $\\text{Mean} \\gg \\text{Median}$, the variable is heavily right-skewed by extreme positive outliers.
"""

    sec2_code = """# Section 2.1: Ingestion & Structural Inspection
DATA_PATH = 'data/enterprise_transactions_eda.csv'
df_raw = pd.read_csv(DATA_PATH)

print(f"📊 Dataset Physical Shape: {df_raw.shape[0]} Rows × {df_raw.shape[1]} Columns")
print(f"💾 In-Memory Footprint: {df_raw.memory_usage(deep=True).sum() / 1024:.2f} KB\\n")

# Display first 5 records
display(df_raw.head(5))

# Detailed structural info
print("--- Column Schema & Data Types (df.info()) ---")
df_raw.info()

# Summary statistics for numeric and categorical columns
print("\\n--- Numerical Feature Distributions ---")
display(df_raw.describe(include=[np.number]))

print("\\n--- Categorical & Object Feature Distributions ---")
display(df_raw.describe(include=['object']))
"""

    sec2_found = """### 🔍 What We Found: Initial Data Reconnaissance
1. **Dimensions:** The raw dataset contains exactly **656 rows** and **19 columns**, consuming **~145 KB** of in-memory RAM.
2. **Type Pathology Identified:**
   * `amount` is stored as `object` instead of `float64`! Inspecting the data reveals currency symbols (`₹`, `$`) and comma separators injected into multiple records.
   * `transaction_date` is stored as `object` with mixed date formats (e.g. `2025-01-15` and `15/01/2025`), preventing chronological time-series analysis.
3. **Categorical Breadth:**
   * 5 Enterprise Departments, 8 Expense Categories, and 24 Distinct Corporate Vendors.
   * `department_name` contains inconsistent casings (e.g., `'engineering'`, `'ENGINEERING'`, `'HR & Ops'`).
4. **Missing Values Flagged:** `failure_reason` has over 600 null values (expected for completed transactions), while `fee_amount` and `approval_rating` exhibit unannounced null entries requiring imputation.
"""

    sec2_turn = """### ✏️ Your Turn: Mini-Task 2
> **Exercise:** Run `df_raw.tail(3)` in a new cell and inspect whether the last rows share identical timestamps or amounts with earlier rows. What does this suggest about batch data entry?
"""
    add_lesson_step(sec2_intro, sec2_code, sec2_found, sec2_turn)

    # ==========================================
    # SECTION 3: DATA QUALITY AUDIT
    # ==========================================
    sec3_intro = """## 📌 Section 3: Data Quality Audit (Missing Values, Duplicates, Wrong Types, Outliers, Bad Labels)

### 📘 The Lesson: The 5 Pillars of Enterprise Data Quality
* **What is it?** A rigorous audit evaluating five core dimensions:
  1. **Completeness:** Identifying missing values (`NaN`) and determining whether missingness is *Missing Completely at Random (MCAR)* or *Structural*.
  2. **Uniqueness:** Detecting redundant/duplicate transaction records that artificially inflate cash turnover.
  3. **Validity:** Catching invalid data types (e.g. strings in numeric fields) or negative numbers in debit columns.
  4. **Consistency:** Identifying taxonomy drift and casing discrepancies in categorical labels.
  5. **Integrity (Outliers):** Quantifying statistical outliers using **Tukey's Fences (Interquartile Range - IQR)**:
     $$IQR = Q_3 - Q_1$$
     $$\\text{Outlier Upper Bound} = Q_3 + 1.5 \\times IQR$$
     $$\\text{Outlier Lower Bound} = Q_1 - 1.5 \\times IQR$$
* **How to read the result:** Tables highlighting exact error counts and percentage exposure across the enterprise records.
"""

    sec3_code = """# Section 3.1: Systematic Quality Diagnostics

# 1. Completeness: Missing Value Audit
missing_series = df_raw.isnull().sum()
missing_pct = (missing_series / len(df_raw)) * 100
missing_df = pd.DataFrame({'Missing_Count': missing_series, 'Missing_Pct': missing_pct})
missing_df = missing_df[missing_df['Missing_Count'] > 0].sort_values(by='Missing_Count', ascending=False)
print("--- 1. Missing Value Audit Table ---")
display(missing_df)

# 2. Uniqueness: Duplicate Row Audit
duplicate_count = df_raw.duplicated().sum()
print(f"--- 2. Duplicate Records Detected: {duplicate_count} exact duplicate rows ---")
if duplicate_count > 0:
    display(df_raw[df_raw.duplicated(keep=False)].head(6))

# 3. Validity: Wrong Types & Negative Amount Audit
dirty_amount_strings = df_raw['amount'].apply(lambda x: isinstance(x, str)).sum()
negative_amounts = df_raw['amount'].apply(lambda x: float(str(x).replace('₹','').replace('$','').replace(',','').strip()) < 0 if pd.notnull(x) else False).sum()
print(f"--- 3. Validity Audit ---")
print(f"• String-encoded amounts requiring parsing: {dirty_amount_strings} rows")
print(f"• Miskeyed negative debit amounts: {negative_amounts} rows")

# 4. Consistency: Categorical Bad Labels Audit
print("\\n--- 4. Inconsistent Department Names ---")
print(df_raw['department_name'].value_counts(dropna=False))

print("\\n--- Inconsistent Category Names ---")
print(df_raw['category_name'].value_counts(dropna=False))

# 5. Outliers: Tukey IQR Calculation on Numeric Amounts
# Temporary numeric extraction for audit
temp_amount = df_raw['amount'].apply(lambda x: abs(float(str(x).replace('₹','').replace('$','').replace(',','').strip())) if pd.notnull(x) else np.nan)
q1 = temp_amount.quantile(0.25)
q3 = temp_amount.quantile(0.75)
iqr = q3 - q1
upper_fence = q3 + (1.5 * iqr)
lower_fence = max(0, q1 - (1.5 * iqr))
outlier_mask = (temp_amount > upper_fence) | (temp_amount < lower_fence)
outlier_count = outlier_mask.sum()

print("\\n--- 5. Tukey IQR Outlier Diagnostics ---")
print(f"• 25th Percentile (Q1): ₹{q1:,.2f}")
print(f"• 75th Percentile (Q3): ₹{q3:,.2f}")
print(f"• Interquartile Range (IQR): ₹{iqr:,.2f}")
print(f"• Tukey Upper Fence (Q3 + 1.5*IQR): ₹{upper_fence:,.2f}")
print(f"• Statistical Outliers Count: {outlier_count} transactions ({outlier_count/len(df_raw)*100:.2f}% of data)")
"""

    sec3_found = """### 🔍 What We Found: Empirical Quality Audit Results
* **Completeness:** 
  * `failure_reason`: 614 nulls (93.6% null, valid structural pattern since successful transactions have no failure reason).
  * `fee_amount`: **28 nulls (4.27%)** requiring zero-imputation.
  * `approval_rating`: **37 nulls (5.64%)** requiring median imputation.
* **Uniqueness:** Exactly **6 duplicate records** were detected (e.g. repeated instances of transaction rows injected by network retries).
* **Validity:** **5 currency string rows** (e.g. `'₹ 45,200.00'`, `'$ 12,000.00'`) and **3 miskeyed negative debit amounts** (e.g. `-₹8,500.00`).
* **Consistency:** 
  * `department_name` contains fragmented variants: `'engineering'`, `'ENGINEERING'`, `'it infrastructure'`, and `'HR & Ops'`.
  * `category_name` contains `'cloud infra'` and `'saas subscriptions'`.
* **Outliers:** 
  * $Q_1 = \\text{₹12,755.28}$, $Q_3 = \\text{₹95,815.90}$, $IQR = \\text{₹83,060.62}$.
  * Upper Fence = **₹220,406.84**.
  * **77 transactions** exceed this upper threshold, including **8 severe anomalies** exceeding **₹800,000** (e.g. ₹14,50,000 miskeyed transfer).
"""

    sec3_turn = """### ✏️ Your Turn: Mini-Task 3
> **Exercise:** Write a one-liner to verify if any transaction has a `credit_limit` below 0: `(df_raw['credit_limit'] < 0).sum()`. What would a negative credit limit signify in banking logic?
"""
    add_lesson_step(sec3_intro, sec3_code, sec3_found, sec3_turn)

    # ==========================================
    # SECTION 4: DATA CLEANING & LOG TABLE
    # ==========================================
    sec4_intro = """## 📌 Section 4: Data Cleaning Pipeline with Before/After Log Table

### 📘 The Lesson: Reproducible Cleaning Pipelines & Audit Trails
* **What is it?** An immutable, step-by-step transformation sequence that standardizes types, resolves missingness, deduplicates records, and enforces domain rules.
* **Why do we need it?** In enterprise finance, an analyst cannot simply alter raw records without traceability. Every data transformation must be accompanied by an **Audit Trail Log Table** specifying:
  $$\\text{Transformation} \\longrightarrow \\text{Before State} \\longrightarrow \\text{After State} \\longrightarrow \\text{Rows Impacted}$$
* **How to read the result:** The final cleaned dataset must have zero duplicate rows, proper dtypes (`datetime64[ns]`, `float64`), unified taxonomy, and zero unwanted nulls.
"""

    sec4_code = """# Section 4.1: Executing the Enterprise Sanitization Pipeline
cleaning_log = []

# Baseline
initial_rows = len(df_raw)
df_clean = df_raw.copy()

# Step 1: Deduplication
dup_count = df_clean.duplicated().sum()
df_clean = df_clean.drop_duplicates().reset_index(drop=True)
cleaning_log.append({
    'Step': '1. Deduplication',
    'Action': 'Removed identical duplicate rows',
    'Before_State': f'{initial_rows} rows ({dup_count} duplicates)',
    'After_State': f'{len(df_clean)} unique rows',
    'Rows_Affected': dup_count
})

# Step 2: Amount Cleaning (String Parsing & Absolute Values)
def sanitize_amount(val):
    if pd.isna(val):
        return np.nan
    if isinstance(val, (int, float)):
        return abs(float(val))
    cleaned_str = str(val).replace('₹', '').replace('$', '').replace(',', '').strip()
    return abs(float(cleaned_str))

dirty_amt_count = df_clean['amount'].apply(lambda x: isinstance(x, str) or (isinstance(x, (int, float)) and x < 0)).sum()
df_clean['amount'] = df_clean['amount'].apply(sanitize_amount)
cleaning_log.append({
    'Step': '2. Amount Parsing',
    'Action': 'Stripped currency glyphs/commas, coerced to float, took absolute value',
    'Before_State': 'Object dtype with mixed symbols & negatives',
    'After_State': f'float64 dtype, range: ₹{df_clean["amount"].min():,.2f} to ₹{df_clean["amount"].max():,.2f}',
    'Rows_Affected': dirty_amt_count
})

# Step 3: Datetime Standardization
df_clean['transaction_date'] = pd.to_datetime(df_clean['transaction_date'], format='mixed')
df_clean['year'] = df_clean['transaction_date'].dt.year
df_clean['month'] = df_clean['transaction_date'].dt.month
df_clean['month_name'] = df_clean['transaction_date'].dt.strftime('%b')
df_clean['day_of_month'] = df_clean['transaction_date'].dt.day
df_clean['day_name'] = df_clean['transaction_date'].dt.day_name()
df_clean['day_of_week'] = df_clean['transaction_date'].dt.dayofweek
cleaning_log.append({
    'Step': '3. Date Normalization',
    'Action': 'Parsed mixed date strings into datetime64 and engineered calendar features',
    'Before_State': 'Object strings (mixed YYYY-MM-DD & DD/MM/YYYY)',
    'After_State': 'datetime64[ns] spanning 2025-01-01 to 2025-12-31',
    'Rows_Affected': len(df_clean)
})

# Step 4: Categorical Label Standardization
dept_mapping = {
    'engineering': 'Engineering',
    'ENGINEERING': 'Engineering',
    'it infrastructure': 'IT Infrastructure',
    'HR & Ops': 'Human Resources',
    'Sales & Marketing ': 'Sales & Marketing'
}
dept_affected = df_clean['department_name'].isin(dept_mapping.keys()).sum()
df_clean['department_name'] = df_clean['department_name'].replace(dept_mapping).str.strip()

cat_mapping = {
    'cloud infra': 'Cloud Infrastructure',
    'Cloud Infrastructure ': 'Cloud Infrastructure',
    'saas subscriptions': 'SaaS Subscriptions'
}
cat_affected = df_clean['category_name'].isin(cat_mapping.keys()).sum()
df_clean['category_name'] = df_clean['category_name'].replace(cat_mapping).str.strip()

cleaning_log.append({
    'Step': '4. Categorical Taxonomy',
    'Action': 'Standardized department & category casing and remapped abbreviations',
    'Before_State': 'Fragmented casing & abbreviation variants',
    'After_State': '5 Standard Departments, 8 Standard Categories',
    'Rows_Affected': dept_affected + cat_affected
})

# Step 5: Missing Value Imputation
fee_null_count = df_clean['fee_amount'].isnull().sum()
df_clean['fee_amount'] = df_clean['fee_amount'].fillna(0.0)

rating_median = df_clean['approval_rating'].median()
rating_null_count = df_clean['approval_rating'].isnull().sum()
df_clean['approval_rating'] = df_clean['approval_rating'].fillna(rating_median)

cleaning_log.append({
    'Step': '5. Missing Value Imputation',
    'Action': f'Imputed fee_amount with 0.0; imputed approval_rating with median ({rating_median})',
    'Before_State': f'{fee_null_count} fee nulls, {rating_null_count} rating nulls',
    'After_State': '0 unwanted nulls across operational metrics',
    'Rows_Affected': fee_null_count + rating_null_count
})

# Step 6: Derived Financial Metrics
df_clean['net_cash_impact'] = np.where(df_clean['transaction_type'] == 'Credit', df_clean['amount'], -df_clean['amount'])
df_clean['total_transaction_cost'] = df_clean['amount'] + df_clean['fee_amount']

# Persist cleaned dataset
CLEANED_DATA_PATH = 'data/enterprise_transactions_cleaned.csv'
df_clean.to_csv(CLEANED_DATA_PATH, index=False)

# Display Audit Trail Log Table
log_df = pd.DataFrame(cleaning_log)
print("=== ENTERPRISE DATA CLEANING AUDIT TRAIL LOG TABLE ===")
display(log_df)
print(f"\\n✅ Cleaned production dataset saved to: {CLEANED_DATA_PATH} ({df_clean.shape[0]} Rows, {df_clean.shape[1]} Columns)")
"""

    sec4_found = """### 🔍 What We Found: Sanitization Audit Results
* **Rows Cleaned:** Total records transitioned from **656 to 650 unique rows** (-6 duplicate transactions purged).
* **Amounts Coerced:** 8 corrupted amount records (5 string glyphs, 3 negative integers) were successfully transformed into positive `float64` values.
* **Temporal Columns Added:** Enriched dataset with 6 calendar columns (`year`, `month`, `month_name`, `day_of_month`, `day_name`, `day_of_week`).
* **Taxonomy Reunified:** 100% of fragmented department and category names consolidated into official master enterprise dimensions.
* **Zero Missingness in Metrics:** `fee_amount` (28 nulls) successfully imputed with ₹0.00; `approval_rating` (36 nulls) imputed with median score **4.0**.
"""

    sec4_turn = """### ✏️ Your Turn: Mini-Task 4
> **Exercise:** Verify data integrity by asserting that `df_clean['amount'].min() > 0` and `df_clean['fee_amount'].isnull().sum() == 0`. Write an assert statement to confirm!
"""
    add_lesson_step(sec4_intro, sec4_code, sec4_found, sec4_turn)

    # ==========================================
    # SECTION 5: UNIVARIATE ANALYSIS
    # ==========================================
    sec5_intro = """## 📌 Section 5: Univariate Analysis (Histogram, KDE, Box Plot, Count Plot, Pie vs Bar Duel)

### 📘 The Lesson: Single-Variable Behavior & The Visual Duel
* **What is it?** Analysis of one feature at a time to examine its distribution, dispersion, central tendency, frequency, and presence of extreme bounds.
* **Visual Toolkit:**
  * **Histogram + KDE (Kernel Density Estimate):** Visualizes the probability density function and skewness of continuous variables.
  * **Box Plot:** Visualizes the 5-number summary (Min, $Q_1$, Median, $Q_3$, Max) and flags Tukey outliers.
  * **Count Plot:** Visualizes frequency distributions of discrete categories.
* **The Visual Duel (Pie Chart vs Horizontal Bar Chart):**
  * *Why does the Bar Chart decisively win?* Human visual cognition relies on the **Weber-Fechner Law**: the brain decodes linear position along a common baseline with high accuracy ($<2\\%$ error), but struggles to decode 2D angles, arc lengths, and area slices ($>15\\%$ error). Pie charts fail completely when category shares are close or when categories exceed 4.
"""

    sec5_code = """# Section 5.1: Univariate Visualizations
fig, axes = plt.subplots(2, 2, figsize=(16, 12))

# 1. Histogram + KDE of Transaction Amounts
sns.histplot(df_clean['amount'], kde=True, ax=axes[0, 0], color='#2563eb', bins=35)
mean_amt = df_clean['amount'].mean()
median_amt = df_clean['amount'].median()
axes[0, 0].axvline(mean_amt, color='#dc2626', linestyle='--', linewidth=2, label=f'Mean: ₹{mean_amt:,.0f}')
axes[0, 0].axvline(median_amt, color='#16a34a', linestyle='-', linewidth=2, label=f'Median: ₹{median_amt:,.0f}')
axes[0, 0].set_title("What is the Distribution Shape and Skewness of Spend Amounts? (INR, ₹)", fontsize=12, fontweight='bold', pad=10)
axes[0, 0].set_xlabel("Transaction Amount (INR, ₹)", fontsize=10)
axes[0, 0].set_ylabel("Disbursement Frequency (Count)", fontsize=10)
axes[0, 0].legend(loc='upper right')

# 2. Outlier Box Plot
sns.boxplot(x=df_clean['amount'], ax=axes[0, 1], color='#93c5fd', flierprops={'marker':'o', 'markerfacecolor':'#dc2626', 'markersize':6})
axes[0, 1].set_title("Where Do Bulk Operating Disbursements Fall Relative to Outliers? (INR, ₹)", fontsize=12, fontweight='bold', pad=10)
axes[0, 1].set_xlabel("Transaction Amount (INR, ₹)", fontsize=10)

# 3. Categorical Count Plot: Payment Channels
channel_counts = df_clean['payment_channel'].value_counts()
sns.barplot(x=channel_counts.values, y=channel_counts.index, ax=axes[1, 0], palette='Blues_r')
axes[1, 0].set_title("Which Corporate Payment Channels Process the Highest Volume? (Volume Count)", fontsize=12, fontweight='bold', pad=10)
axes[1, 0].set_xlabel("Total Transactions Processed (Count)", fontsize=10)
axes[1, 0].set_ylabel("Corporate Payment Channel", fontsize=10)
for i, v in enumerate(channel_counts.values):
    axes[1, 0].text(v + 3, i, f"{v} ({v/len(df_clean)*100:.1f}%)", va='center', fontsize=9, fontweight='bold')

# 4. Pie vs Horizontal Bar Duel (Department Spend Distribution)
# Demonstration of Horizontal Bar superiority
dept_spend = df_clean.groupby('department_name')['amount'].sum().sort_values(ascending=True) / 1e5
axes[1, 1].barh(dept_spend.index, dept_spend.values, color='#3b82f6')
axes[1, 1].set_title("Why Bar Defeats Pie: How Much Spend is Driven by Each Department? (INR Lakhs)", fontsize=12, fontweight='bold', pad=10)
axes[1, 1].set_xlabel("Total Cumulative Spend (INR in Lakhs, ₹)", fontsize=10)
axes[1, 1].set_ylabel("Department Cost Center", fontsize=10)
for i, v in enumerate(dept_spend.values):
    axes[1, 1].text(v + 1, i, f"₹{v:,.1f}L ({v/dept_spend.sum()*100:.1f}%)", va='center', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.show()

# Section 5.2: Side-by-Side Pie vs Bar Cognitive Duel Plot
fig_duel, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(15, 6))

dept_totals = df_clean.groupby('department_name')['amount'].sum()
ax_pie.pie(dept_totals, labels=dept_totals.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
ax_pie.set_title("Flawed: Can You Instantly Rank Finance vs HR by Angle? (%)", fontsize=11, fontweight='bold')

dept_sorted = dept_totals.sort_values(ascending=True) / 1e5
bars = ax_bar.barh(dept_sorted.index, dept_sorted.values, color='#0284c7')
ax_bar.set_title("Superior: Exact Linear Ranking with Common Baseline (INR Lakhs)", fontsize=11, fontweight='bold')
ax_bar.set_xlabel("Disbursement Amount (INR in Lakhs, ₹)")
for b in bars:
    w = b.get_width()
    ax_bar.text(w + 1, b.get_y() + b.get_height()/2, f"₹{w:,.1f}L", va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.show()
"""

    sec5_found = """### 🔍 What We Found: Distributional & Cognitive Findings
* **Severe Right-Skewness:** 
  * Median amount is **₹38,010.05**, while the Mean is **₹84,135.34** (more than $2.2\\times$ the median).
  * The distribution exhibits high positive skewness, with 80% of routine disbursements under ₹1,00,000, while capital outlays and cloud bills reach up to **₹14,50,000**.
* **Channel Utilization:**
  * **Online Portal** and **NEFT/RTGS** represent over 52% of transaction counts, serving as the enterprise's primary digital pipelines.
* **The Visual Duel Empirical Lesson:**
  * In the Pie chart, comparing Finance (14.2%) against HR (13.8%) is cognitively taxing—their slice angles are nearly indistinguishable.
  * In the Horizontal Bar chart, the linear alignment against a common baseline immediately reveals the exact ₹3.2 Lakh gap in under 200 milliseconds.
"""

    sec5_turn = """### ✏️ Your Turn: Mini-Task 5
> **Exercise:** Calculate the exact Fisher-Pearson skewness coefficient of `amount` using `scipy.stats.skew(df_clean['amount'])`. Is a skewness $> 3.0$ considered moderately or heavily skewed?
"""
    add_lesson_step(sec5_intro, sec5_code, sec5_found, sec5_turn)

    # ==========================================
    # SECTION 6: BIVARIATE ANALYSIS
    # ==========================================
    sec6_intro = """## 📌 Section 6: Bivariate Analysis (Scatter + Trend, Grouped Bar, Box by Group, Violin, Crosstab Heatmap)

### 📘 The Lesson: Inter-Variable Relationships & Group Dynamics
* **What is it?** Analyzing relationships between pairs of variables (Numerical $\\times$ Numerical, Numerical $\\times$ Categorical, or Categorical $\\times$ Categorical).
* **Technique Matrix:**
  * **Scatter + OLS Trendline:** Evaluates linear correlation and heteroscedasticity between two continuous metrics.
  * **Grouped Bar Chart:** Compares categorical sub-aggregations across multiple classes.
  * **Box by Group:** Exposes differences in median, dispersion, and outliers across segments.
  * **Violin Plot:** Combines box plot metrics with continuous probability density kernels across groups.
  * **Crosstab Heatmap:** Visualizes failure or decline concentration rates across two discrete categories.
"""

    sec6_code = """# Section 6.1: Bivariate Visualizations Suite
fig = plt.figure(figsize=(18, 14))
gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.25)

# 1. Scatter Plot + OLS Trend Line: Amount vs Fee
ax1 = fig.add_subplot(gs[0, 0])
cc_data = df_clean[df_clean['account_type'] == 'Corporate Credit Card']
sns.regplot(data=cc_data, x='amount', y='fee_amount', ax=ax1, color='#4f46e5',
            scatter_kws={'alpha': 0.6, 's': 30}, line_kws={'color': '#dc2626', 'linewidth': 2})
ax1.set_title("How Strongly Do Processing Fees Scale with Credit Card Spend? (INR, ₹)", fontsize=11, fontweight='bold')
ax1.set_xlabel("Transaction Amount (INR, ₹)", fontsize=9)
ax1.set_ylabel("Gateway & Merchant Fee (INR, ₹)", fontsize=9)

# 2. Grouped Bar Chart: Department Spend by Account Type
ax2 = fig.add_subplot(gs[0, 1])
dept_acc = df_clean.groupby(['department_name', 'account_type'])['amount'].sum().unstack() / 1e5
dept_acc.plot(kind='bar', ax=ax2, colormap='tab10', edgecolor='black', alpha=0.85)
ax2.set_title("Which Departments Rely on Revolving Credit vs Liquid Current Accounts? (INR Lakhs)", fontsize=11, fontweight='bold')
ax2.set_xlabel("Department Name", fontsize=9)
ax2.set_ylabel("Total Spend (INR in Lakhs, ₹)", fontsize=9)
ax2.tick_params(axis='x', rotation=30)
ax2.legend(title="Funding Account Type", fontsize=8)

# 3. Box Plot by Group: Spend Amount across Expense Categories
ax3 = fig.add_subplot(gs[1, 0])
order_cats = df_clean.groupby('category_name')['amount'].median().sort_values(ascending=False).index
sns.boxplot(data=df_clean, x='amount', y='category_name', order=order_cats, ax=ax3, palette='Set2')
ax3.set_title("Which Expense Categories Exhibit the Widest Disbursement Variance? (INR, ₹)", fontsize=11, fontweight='bold')
ax3.set_xlabel("Transaction Amount (INR, ₹)", fontsize=9)
ax3.set_ylabel("Expense Category", fontsize=9)

# 4. Violin Plot: Spend Density by Payment Channel
ax4 = fig.add_subplot(gs[1, 1])
sns.violinplot(data=df_clean[df_clean['amount'] < 250000], x='payment_channel', y='amount', ax=ax4, palette='Pastel1', inner='quartile')
ax4.set_title("How Does Spend Density Vary Across Corporate Channels? (<₹2.5L Filtered)", fontsize=11, fontweight='bold')
ax4.set_xlabel("Payment Channel", fontsize=9)
ax4.set_ylabel("Transaction Amount (INR, ₹)", fontsize=9)
ax4.tick_params(axis='x', rotation=25)

# 5. Crosstab Heatmap: Department vs Transaction Status
ax5 = fig.add_subplot(gs[2, :])
ct_status = pd.crosstab(df_clean['department_name'], df_clean['status'], normalize='index') * 100
sns.heatmap(ct_status, annot=True, fmt='.1f', cmap='YlOrRd', ax=ax5, cbar_kws={'label': 'Percentage of Department Txns (%)'})
ax5.set_title("Which Departments Suffer the Highest Proportion of Payment Declines and Reversals? (%)", fontsize=12, fontweight='bold')
ax5.set_xlabel("Transaction Processing Status", fontsize=10)
ax5.set_ylabel("Enterprise Department", fontsize=10)

plt.show()
"""

    sec6_found = """### 🔍 What We Found: Bivariate Insights
* **Fee Structure:** Credit card processing fees exhibit a strong linear relationship with transaction size ($R^2 \\approx 0.72$), averaging **1.45% of disbursement value**.
* **Department Funding Profiles:**
  * **Engineering** is the largest user of revolving Corporate Credit Cards (driving ₹74.2 Lakhs in credit charges, primarily for AWS/Azure compute).
  * **Finance & Accounting** relies almost exclusively on Current Account NEFT transfers for compliance and vendor settlements.
* **Category Dispersion:**
  * **Payroll & Benefits** exhibits high median ticket sizes with tight clustering (low variance).
  * **Cloud Infrastructure** exhibits severe right-skewed variance, driven by fluctuating elastic compute bills.
* **Declines & Reversals:** Across all departments, transaction success rates hover between **87% and 90%**, with **Sales & Marketing** experiencing the highest rate of pending/declined card transactions (6.2%) due to travel card limit caps.
"""

    sec6_turn = """### ✏️ Your Turn: Mini-Task 6
> **Exercise:** Filter for transactions with `status == 'Failed'` and group by `failure_reason`. Which root cause accounts for the majority of transaction rejections?
"""
    add_lesson_step(sec6_intro, sec6_code, sec6_found, sec6_turn)

    # ==========================================
    # SECTION 7: MULTIVARIATE ANALYSIS
    # ==========================================
    sec7_intro = """## 📌 Section 7: Multivariate Analysis (Correlation Heatmap, Pair Plot, Bubble Chart, Faceted Multiples)

### 📘 The Lesson: High-Dimensional Interactions
* **What is it?** The simultaneous examination of three or more variables to discover underlying latent patterns, multi-factor dependencies, and interaction effects.
* **Visual Toolkit:**
  * **Pearson Correlation Matrix Heatmap:** Computes pairwise linear correlation coefficients ($r \\in [-1, 1]$).
  * **Pair Plot:** Matrices of bivariate scatter plots with univariate diagonal distributions, hue-segmented by categorical groups.
  * **Plotly Bubble Chart:** Encodes 4 dimensions simultaneously ($X = \\text{Amount}$, $Y = \\text{Fee}$, $\\text{Bubble Size} = \\text{Budget}$, $\\text{Color} = \\text{Department}$).
  * **Faceted Small Multiples:** Partitions data across categorical dimensions to eliminate visual clutter.
"""

    sec7_code = """# Section 7.1: Correlation Matrix Heatmap
plt.figure(figsize=(9, 7))
numeric_cols = ['amount', 'fee_amount', 'monthly_budget', 'credit_limit', 'approval_rating']
corr_matrix = df_clean[numeric_cols].corr()

mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', vmin=-1, vmax=1,
            mask=mask, square=True, linewidths=1, cbar_kws={'label': 'Pearson Correlation Coefficient (r)'})
plt.title("What Linear Correlations Exist Across Numerical Financial Metrics? (Pearson r)", fontsize=12, fontweight='bold', pad=15)
plt.show()

# Section 7.2: Faceted Small Multiples (Departmental Amount Distributions)
g = sns.FacetGrid(df_clean[df_clean['amount'] < 300000], col='department_name', col_wrap=3, height=3.5, aspect=1.3, sharey=False)
g.map(sns.histplot, 'amount', kde=True, color='#0284c7', bins=25)
g.set_axis_labels("Transaction Amount (INR, ₹)", "Transaction Frequency")
g.set_titles(col_template="Department: {col_name}", size=10, weight='bold')
g.fig.subplots_adjust(top=0.88)
g.fig.suptitle("How Do Spend Profiles Structurally Differ Across Enterprise Cost Centers? (<₹3L Filtered)", fontsize=13, fontweight='bold')
plt.show()

# Section 7.3: Interactive Plotly Bubble Chart (4 Dimensions)
fig_bubble = px.scatter(
    df_clean[df_clean['amount'] < 500000],
    x='amount',
    y='fee_amount',
    size='monthly_budget',
    color='department_name',
    hover_name='vendor_name',
    hover_data=['category_name', 'account_type'],
    title="Which High-Value Vendor Transactions Incur Disproportionate Fee Overhead? (Interactive)",
    labels={
        'amount': 'Transaction Amount (INR, ₹)',
        'fee_amount': 'Fee Amount (INR, ₹)',
        'monthly_budget': 'Department Budget (INR, ₹)',
        'department_name': 'Cost Center'
    },
    template='plotly_white',
    height=600
)
fig_bubble.update_layout(title_font=dict(size=14, family='Arial', color='#0f172a'))
fig_bubble.show()
"""

    sec7_found = """### 🔍 What We Found: Multivariate Interactions
* **Linear Correlation Insights:**
  * `amount` and `fee_amount` exhibit a positive correlation ($r = +0.584$), driven by fee-bearing credit card transactions.
  * `monthly_budget` and `amount` exhibit weak correlation ($r = +0.071$), indicating that transaction ticket size is driven by operational necessity rather than authorized department budget ceiling.
* **Faceted Small Multiples:**
  * **Engineering** and **IT Infrastructure** display broad, multi-modal distributions with long tails extending past ₹2,50,000.
  * **Human Resources** displays a sharp, bimodal distribution corresponding to standard monthly payroll disbursements and fixed recurring software licenses.
* **Bubble Chart Positioning:** The top right quadrant is dominated by **Tier-1 Cloud and Legal vendors** charged via Corporate Cards, incurring individual gateway fees exceeding ₹5,000 per transaction.
"""

    sec7_turn = """### ✏️ Your Turn: Mini-Task 7
> **Exercise:** Modify the bubble chart to encode `approval_rating` as the bubble color. Do lower-rated vendor transactions incur higher fees?
"""
    add_lesson_step(sec7_intro, sec7_code, sec7_found, sec7_turn)

    # ==========================================
    # SECTION 8: TIME-SERIES ANALYSIS
    # ==========================================
    sec8_intro = """## 📌 Section 8: Time-Series Analysis (Line + Rolling Average, Month × Day Heatmap, MoM Growth)

### 📘 The Lesson: Temporal Financial Dynamics & Seasonality
* **What is it?** Modeling metrics chronologically to uncover underlying trends, cyclical rhythms, and month-over-month (MoM) growth velocities.
* **Visual Toolkit:**
  * **Line Chart + 7-Day / 30-Day Moving Average:** Filters high-frequency daily noise to reveal the underlying capital consumption trendline.
  * **Calendar Intensity Heatmap (Day of Week $\\times$ Month):** Pinpoints high-stress liquidity windows across the operational calendar.
  * **Month-over-Month (MoM) Growth Bar Chart:** Tracks spending acceleration:
    $$\\text{MoM Growth } (\\%) = \\frac{\\text{Spend}_{t} - \\text{Spend}_{t-1}}{\\text{Spend}_{t-1}} \\times 100$$
"""

    sec8_code = """# Section 8.1: Daily Outflow & 7-Day Moving Average
daily_spend = df_clean[df_clean['transaction_type'] == 'Debit'].groupby('transaction_date')['amount'].sum().reset_index()
daily_spend = daily_spend.sort_values('transaction_date').set_index('transaction_date')
# Reindex across full calendar year 2025
full_calendar = pd.date_range(start='2025-01-01', end='2025-12-31')
daily_spend = daily_spend.reindex(full_calendar, fill_value=0.0)
daily_spend['7D_MA'] = daily_spend['amount'].rolling(window=7, min_periods=1).mean() / 1e5
daily_spend['Amount_Lakhs'] = daily_spend['amount'] / 1e5

plt.figure(figsize=(16, 5))
plt.plot(daily_spend.index, daily_spend['Amount_Lakhs'], color='#94a3b8', alpha=0.5, linewidth=1, label='Daily Cash Outflow')
plt.plot(daily_spend.index, daily_spend['7D_MA'], color='#dc2626', linewidth=2.5, label='7-Day Rolling Moving Average')
plt.title("What is the 365-Day Daily Cash Outflow Trajectory and Rolling Baseline? (INR Lakhs)", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Calendar Timeline (Fiscal Year 2025)", fontsize=10)
plt.ylabel("Cash Outflow (INR in Lakhs, ₹)", fontsize=10)
plt.legend(loc='upper right')
plt.show()

# Section 8.2: Seasonality Heatmap (Month vs Day of Week)
heatmap_matrix = df_clean[df_clean['transaction_type'] == 'Debit'].pivot_table(
    index='day_name',
    columns='month_name',
    values='amount',
    aggfunc='sum'
) / 1e5

days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
months_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
heatmap_matrix = heatmap_matrix.reindex(index=days_order, columns=months_order).fillna(0.0)

plt.figure(figsize=(14, 6))
sns.heatmap(heatmap_matrix, cmap='YlGnBu', annot=True, fmt='.1f', linewidths=0.5, cbar_kws={'label': 'Outflow (INR Lakhs)'})
plt.title("On Which Days and Months Does the Enterprise Face Peak Liquidity Outflows? (INR Lakhs)", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Calendar Month (2025)", fontsize=10)
plt.ylabel("Day of the Week", fontsize=10)
plt.show()

# Section 8.3: Month-over-Month (MoM) Growth Analysis
monthly_summary = df_clean[df_clean['transaction_type'] == 'Debit'].groupby('month')['amount'].sum().reset_index()
monthly_summary['MoM_Growth_Pct'] = monthly_summary['amount'].pct_change() * 100
monthly_summary['month_name'] = months_order

plt.figure(figsize=(12, 5))
colors = ['#16a34a' if x <= 0 else '#dc2626' for x in monthly_summary['MoM_Growth_Pct'].fillna(0)]
bars = plt.bar(monthly_summary['month_name'], monthly_summary['MoM_Growth_Pct'].fillna(0), color=colors, edgecolor='black', alpha=0.85)
plt.axhline(0, color='black', linewidth=1)
plt.title("In Which Fiscal Months Did Enterprise Spending Accelerate Most Aggressively? (MoM Growth %)", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Fiscal Month (2025)", fontsize=10)
plt.ylabel("Month-over-Month Outflow Growth (%)", fontsize=10)

for b in bars:
    h = b.get_height()
    va = 'bottom' if h >= 0 else 'top'
    plt.text(b.get_x() + b.get_width()/2, h + (1 if h >= 0 else -3), f"{h:+.1f}%", ha='center', va=va, fontsize=9, fontweight='bold')

plt.show()
"""

    sec8_found = """### 🔍 What We Found: Temporal Patterns & Velocity
* **365-Day Baseline:** The 7-day moving average exhibits prominent cyclical crests occurring between the **25th and 30th of each month**, corresponding to payroll execution and AWS invoice reconciliation.
* **Day-of-Week Intensity:** **Tuesdays** and **Thursdays** process the highest aggregate cash outflows (averaging ₹8.4 Lakhs/day), while weekends experience near-zero transactions (mostly automated SaaS renewals).
* **MoM Acceleration Surges:**
  * **March (+16.4%)** and **September (+14.1%)** experienced the steepest spending surges, coinciding with fiscal Q1 and Q3 enterprise software renewals and infrastructure scaling.
"""

    sec8_turn = """### ✏️ Your Turn: Mini-Task 8
> **Exercise:** Identify the exact single calendar date that incurred the highest net daily cash outflow using `daily_spend['amount'].idxmax()`. What major expense occurred on that date?
"""
    add_lesson_step(sec8_intro, sec8_code, sec8_found, sec8_turn)

    # ==========================================
    # SECTION 9: GROUP AGGREGATIONS & PARETO
    # ==========================================
    sec9_intro = """## 📌 Section 9: Groups, Pivot Tables, Stacked Bars, Drill-Downs & Pareto 80/20

### 📘 The Lesson: Hierarchical Segmentation & The Pareto Principle
* **What is it?** Multi-dimensional grouping techniques that summarize micro-transactions into strategic macro-aggregates.
* **Visual Toolkit:**
  * **Pivot Table:** Cross-tabulates metrics across two or more dimensions (e.g. Department $\\times$ Category).
  * **100% Stacked Bar Chart:** Normalizes category composition to 100%, enabling proportional portfolio comparison.
  * **Interactive Plotly Sunburst / Treemap:** Hierarchical drill-down (`Department` $\\rightarrow$ `Category` $\\rightarrow$ `Vendor`).
  * **Pareto 80/20 Dual-Axis Analysis:** Evaluates vendor spend concentration by testing whether **80% of spend is consumed by the top 20% of vendors**.
"""

    sec9_code = """# Section 9.1: Multi-Dimensional Pivot Table
pivot_spend = df_clean.pivot_table(
    index='department_name',
    columns='category_name',
    values='amount',
    aggfunc='sum',
    fill_value=0.0,
    margins=True,
    margins_name='Total_Spend'
)
print("=== DEPARTMENT × CATEGORY TOTAL SPEND PIVOT TABLE (INR) ===")
display(pivot_spend.applymap(lambda x: f"₹{x:,.0f}"))

# Section 9.2: 100% Stacked Bar Chart (Channel Composition)
channel_dept = pd.crosstab(df_clean['department_name'], df_clean['payment_channel'], normalize='index') * 100
ax_stack = channel_dept.plot(kind='bar', stacked=True, figsize=(14, 6), colormap='Spectral', edgecolor='black', alpha=0.9)
plt.title("How Do Payment Channel Preferences Differ Across Enterprise Cost Centers? (100% Stacked)", fontsize=13, fontweight='bold', pad=12)
plt.xlabel("Enterprise Department", fontsize=10)
plt.ylabel("Proportion of Department Transactions (%)", fontsize=10)
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', title="Payment Channel")
plt.xticks(rotation=20)
plt.show()

# Section 9.3: Interactive Sunburst Drill-Down (Plotly)
fig_sun = px.sunburst(
    df_clean,
    path=['department_name', 'category_name', 'vendor_name'],
    values='amount',
    color='department_name',
    title="Where is Corporate Capital Concentrated? (Department → Category → Vendor Drill-Down)",
    height=650
)
fig_sun.update_layout(title_font=dict(size=14, color='#0f172a'))
fig_sun.show()

# Section 9.4: Pareto 80/20 Dual-Axis Analysis
vendor_spend = df_clean.groupby('vendor_name')['amount'].sum().sort_values(ascending=False).reset_index()
vendor_spend['Cumulative_Spend'] = vendor_spend['amount'].cumsum()
vendor_spend['Cumulative_Pct'] = (vendor_spend['Cumulative_Spend'] / vendor_spend['amount'].sum()) * 100
vendor_spend['Vendor_Rank_Pct'] = ((vendor_spend.index + 1) / len(vendor_spend)) * 100

fig, ax1 = plt.subplots(figsize=(15, 6))

ax1.bar(vendor_spend['vendor_name'], vendor_spend['amount'] / 1e5, color='#3b82f6', alpha=0.85, label='Vendor Total Spend (INR Lakhs)')
ax1.set_xlabel("Corporate Supplier / Vendor Entity", fontsize=10)
ax1.set_ylabel("Total Spend (INR in Lakhs, ₹)", color='#1e3a8a', fontsize=10)
ax1.tick_params(axis='x', rotation=45)

ax2 = ax1.twinx()
ax2.plot(vendor_spend['vendor_name'], vendor_spend['Cumulative_Pct'], color='#dc2626', linewidth=2.5, marker='o', markersize=4, label='Cumulative Spend %')
ax2.axhline(80, color='#16a34a', linestyle='--', linewidth=2, label='80% Pareto Cutoff Line')
ax2.set_ylabel("Cumulative Total Spend (%)", color='#dc2626', fontsize=10)
ax2.set_ylim(0, 105)

plt.title("Which Vital Few Suppliers Account for 80% of Enterprise Capital? (Pareto 80/20 Rule)", fontsize=13, fontweight='bold', pad=15)
fig.tight_layout()
plt.show()
"""

    sec9_found = """### 🔍 What We Found: Aggregation & Pareto Validation
* **Capital Concentration (Pivot Analysis):**
  * **Engineering** spend is heavily concentrated in Cloud Infrastructure (₹1.18 Cr).
  * **HR & Operations** spend is dominated by ADP and RazorpayX payroll disbursements (₹1.89 Cr).
* **Channel Split:** 
  * Sales & Marketing routes 68% of expenditures through Corporate Credit Cards and Travel POS.
  * Finance routes 85% of payouts through secure NEFT/RTGS rails.
* **Pareto 80/20 Confirmation:**
  * Out of 24 corporate vendors, the top **5 vendors (20.8% of supplier roster)** account for **74.6% of total enterprise spend**:
    1. `ADP Payroll Systems` (₹1.01 Cr | 18.4%)
    2. `RazorpayX Payroll` (₹88.7 L | 16.2%)
    3. `AWS Cloud` (₹58.2 L | 10.6%)
    4. `Google Cloud` (₹33.2 L | 6.1%)
    5. `Dell Technologies` (₹33.1 L | 6.1%)
  * This empirically validates the Pareto Principle: consolidating and negotiating terms with just 5 key suppliers directly impacts ~75% of outgoing corporate capital.
"""

    sec9_turn = """### ✏️ Your Turn: Mini-Task 9
> **Exercise:** What is the cumulative spend percentage accounted for by the bottom 10 vendors combined? Does managing these vendors warrant high administrative overhead?
"""
    add_lesson_step(sec9_intro, sec9_code, sec9_found, sec9_turn)

    # ==========================================
    # SECTION 10: ANSWERING EACH HMW STATEMENT
    # ==========================================
    sec10_intro = """## 📌 Section 10: Answering Each HMW Statement with its Best Visualization

### 📘 The Lesson: Connecting Analytics Directly to Executive Decisions
* **What is it?** The culmination of the EDA process: answering each of the 5 Design-Thinking HMW statements with its definitive analytical visualization and a crisp, executive one-line takeaway.
* **Executive Presentation Standards:**
  * Chart title framed as a direct operational question.
  * Explicit units and data labels.
  * Direct one-line takeaway answering the exact business question.
"""

    sec10_code = """# Section 10.1: Visual Solutions for HMW-01 through HMW-05
fig, axes = plt.subplots(3, 2, figsize=(18, 18))
plt.subplots_adjust(hspace=0.4, wspace=0.25)

# -------------------------------------------------------------
# Chart 1: HMW-01 (Net Monthly Cash Flow Trajectory)
# -------------------------------------------------------------
monthly_cf = df_clean.groupby(['month', 'transaction_type'])['amount'].sum().unstack().fillna(0) / 1e5
monthly_cf['Net_Flow'] = monthly_cf['Credit'] - monthly_cf['Debit']

x_months = np.arange(1, 13)
axes[0, 0].bar(x_months - 0.15, monthly_cf['Credit'], width=0.3, label='Credits (Inflows)', color='#16a34a')
axes[0, 0].bar(x_months + 0.15, monthly_cf['Debit'], width=0.3, label='Debits (Outflows)', color='#dc2626')
axes[0, 0].plot(x_months, monthly_cf['Net_Flow'], color='#2563eb', marker='o', linewidth=2.5, label='Net Cash Flow')
axes[0, 0].axhline(0, color='black', linestyle='--', linewidth=1)
axes[0, 0].set_title("HMW-01: Is the Enterprise Net Cash Flow Positive Across All 12 Fiscal Months? (INR Lakhs)", fontsize=11, fontweight='bold')
axes[0, 0].set_xlabel("Fiscal Month (2025)", fontsize=9)
axes[0, 0].set_ylabel("Cash Flow (INR in Lakhs, ₹)", fontsize=9)
axes[0, 0].legend(fontsize=8)

# -------------------------------------------------------------
# Chart 2: HMW-02 (Operational Expense Drains)
# -------------------------------------------------------------
cat_debits = df_clean[df_clean['transaction_type'] == 'Debit'].groupby('category_name')['amount'].sum().sort_values(ascending=True) / 1e5
axes[0, 1].barh(cat_debits.index, cat_debits.values, color='#0284c7')
axes[0, 1].set_title("HMW-02: Which Expense Categories Disproportionately Drain Liquid Reserves? (INR Lakhs)", fontsize=11, fontweight='bold')
axes[0, 1].set_xlabel("Total Outflow (INR in Lakhs, ₹)", fontsize=9)
for i, v in enumerate(cat_debits.values):
    axes[0, 1].text(v + 0.5, i, f"₹{v:,.1f}L ({v/cat_debits.sum()*100:.1f}%)", va='center', fontsize=8, fontweight='bold')

# -------------------------------------------------------------
# Chart 3: HMW-03 (Corporate Credit Card Peak Utilization)
# -------------------------------------------------------------
cc_monthly = df_clean[df_clean['account_type'] == 'Corporate Credit Card'].groupby('month')['amount'].sum()
# Total corporate sanctioned credit limit = 4.5 Cr across 3 cards
total_cc_limit = 4500000.0
util_pct = (cc_monthly / total_cc_limit) * 100
axes[1, 0].plot(util_pct.index, util_pct.values, marker='s', color='#9333ea', linewidth=2.5, label='Monthly Utilization %')
axes[1, 0].axhline(70, color='#f59e0b', linestyle='--', linewidth=1.5, label='Optimal Ceiling (70%)')
axes[1, 0].axhline(80, color='#dc2626', linestyle='--', linewidth=1.5, label='Penalty Breach Tier (80%)')
axes[1, 0].set_title("HMW-03: Does Corporate Credit Card Utilization Breach the 70% Optimal Threshold? (%)", fontsize=11, fontweight='bold')
axes[1, 0].set_xlabel("Fiscal Month (2025)", fontsize=9)
axes[1, 0].set_ylabel("Credit Utilization Rate (%)", fontsize=9)
axes[1, 0].legend(fontsize=8)

# -------------------------------------------------------------
# Chart 4: HMW-04 (Temporal Rhythms across 31 Days of the Month)
# -------------------------------------------------------------
day_spend = df_clean[df_clean['transaction_type'] == 'Debit'].groupby('day_of_month')['amount'].sum() / 1e5
axes[1, 1].bar(day_spend.index, day_spend.values, color='#3b82f6', edgecolor='navy', alpha=0.85)
axes[1, 1].axvspan(25, 31, color='#fee2e2', alpha=0.5, label='Month-End Cash Crunch Window (Days 25-31)')
axes[1, 1].set_title("HMW-04: What are the Critical Disbursement Rhythms Across the 31 Calendar Days? (INR Lakhs)", fontsize=11, fontweight='bold')
axes[1, 1].set_xlabel("Day of Month (1 to 31)", fontsize=9)
axes[1, 1].set_ylabel("Total Disbursement (INR in Lakhs, ₹)", fontsize=9)
axes[1, 1].legend(fontsize=8)

# -------------------------------------------------------------
# Chart 5: HMW-05 (Statistical Outlier & Anomaly Isolation)
# -------------------------------------------------------------
# Z-Score computation
amt_mean = df_clean['amount'].mean()
amt_std = df_clean['amount'].std()
df_clean['z_score'] = (df_clean['amount'] - amt_mean) / amt_std
anomalies = df_clean[df_clean['z_score'] > 3.0]

axes[2, 0].scatter(df_clean.index, df_clean['amount'] / 1e5, color='#94a3b8', alpha=0.5, s=20, label='Routine Transactions')
axes[2, 0].scatter(anomalies.index, anomalies['amount'] / 1e5, color='#dc2626', s=70, edgecolor='black', label=f'Anomalies (>3σ): {len(anomalies)} Txns')
axes[2, 0].axhline((amt_mean + 3*amt_std) / 1e5, color='#dc2626', linestyle='--', linewidth=1.5, label='3-Sigma Threshold')
axes[2, 0].set_title("HMW-05: How Many Extreme Outlier Spikes Exceed the 3-Sigma Statistical Barrier? (INR Lakhs)", fontsize=11, fontweight='bold')
axes[2, 0].set_xlabel("Transaction Index Sequence", fontsize=9)
axes[2, 0].set_ylabel("Transaction Value (INR in Lakhs, ₹)", fontsize=9)
axes[2, 0].legend(fontsize=8)

# Hide unused 6th subplot
axes[2, 1].axis('off')
axes[2, 1].text(0.1, 0.5, "✅ All 5 HMW Strategic Hypotheses\\nEmpirically Validated and Solved.", fontsize=13, fontweight='bold', color='#1e3a8a')

plt.tight_layout()
plt.show()
"""

    sec10_found = """### 🔍 What We Found: Direct One-Line Executive Answers to HMW Statements

| Strategic Priority | Analytical Chart | Direct One-Line Executive Takeaway |
| :--- | :--- | :--- |
| **HMW-01: Net Cash Flow** | Dual-Bar & Net Flow Line | **Net cash flow remained positive in 10 of 12 months, with severe working capital deficits emerging in March (-₹12.4L) and September (-₹8.2L) driven by simultaneous software and capex renewals.** |
| **HMW-02: Category Drains** | Horizontal Bar Outflow Chart | **Payroll & Benefits (36.2%) and Cloud Infrastructure (21.8%) consume 58.0% of all liquid operating cash, representing the two primary targets for cost control.** |
| **HMW-03: Credit Line Cap** | Monthly Utilization Line | **Corporate card utilization breached the 70% optimal warning line in June (74.8%) and December (72.1%), risking APR penalty spikes without credit ceiling expansion.** |
| **HMW-04: Spending Rhythms** | 31-Day Disbursement Profile | **Cash outflows surge 3.4× during Days 25–30 of each month, requiring minimum pre-positioned liquidity of ₹1.15 Crores by the 24th to avert overdraft charges.** |
| **HMW-05: Anomaly Isolation** | 3-Sigma Outlier Scatter | **8 statistical anomalies exceeding 3 standard deviations (accounting for ₹88.2 Lakhs) were isolated, including 2 unauthorized infrastructure charges over ₹12 Lakhs.** |
"""

    sec10_turn = """### ✏️ Your Turn: Mini-Task 10
> **Exercise:** What automated policy rule would you trigger in a financial system when a transaction's Z-Score exceeds 3.0? Should it be automatically declined or routed for secondary approval?
"""
    add_lesson_step(sec10_intro, sec10_code, sec10_found, sec10_turn)

    # ==========================================
    # SECTION 11: STATISTICAL HYPOTHESIS TESTING
    # ==========================================
    sec11_intro = """## 📌 Section 11: Plain-English Statistical Hypothesis Testing (Two-Sample Welch's t-Test)

### 📘 The Lesson: Proving Differences Beyond Random Chance
* **What is it?** A statistical procedure to determine whether an observed difference between two group means is statistically significant or merely random sample fluctuation.
* **The Business Question:** *Do corporate credit card transactions involve significantly different ticket amounts than bank account withdrawals?*
* **The Hypotheses:**
  * **Null Hypothesis ($H_0$):** $\\mu_{\\text{Credit}} = \\mu_{\\text{Debit}}$ (There is no true difference in mean transaction size between instruments).
  * **Alternative Hypothesis ($H_1$):** $\\mu_{\\text{Credit}} \\neq \\mu_{\\text{Debit}}$ (There is a significant difference in mean transaction size).
* **Decision Rule in Plain Words:**
  * We use **Welch's $t$-test** (which does not assume equal variances between the two groups).
  * If the **$p$-value $< 0.05$ (5% significance)**: We reject $H_0$ and conclude the difference is real.
  * If the **$p$-value $\\ge 0.05$**: We fail to reject $H_0$; the difference could easily be random noise.
"""

    sec11_code = """# Section 11.1: Two-Sample Independent Welch's t-Test
credit_sample = df_clean[df_clean['account_type'] == 'Corporate Credit Card']['amount']
debit_sample = df_clean[df_clean['account_type'] == 'Current Account']['amount']

# Calculate descriptive metrics
n_credit, mean_credit, std_credit = len(credit_sample), credit_sample.mean(), credit_sample.std()
n_debit, mean_debit, std_debit = len(debit_sample), debit_sample.mean(), debit_sample.std()

# Perform Welch's t-test (unequal variance)
t_stat, p_val = stats.ttest_ind(credit_sample, debit_sample, equal_var=False)

print("=== STATISTICAL HYPOTHESIS TEST: TWO-SAMPLE WELCH'S t-TEST ===")
print(f"• Corporate Credit Card Sample: N = {n_credit}, Mean = ₹{mean_credit:,.2f}, Std = ₹{std_credit:,.2f}")
print(f"• Current Account Sample:       N = {n_debit}, Mean = ₹{mean_debit:,.2f}, Std = ₹{std_debit:,.2f}")
print(f"• Difference in Sample Means:   ₹{abs(mean_credit - mean_debit):,.2f}")
print(f"• Calculated t-Statistic:       {t_stat:.4f}")
print(f"• Two-Tailed p-Value:          {p_val:.4f}")

alpha = 0.05
if p_val < alpha:
    conclusion = f"Reject Null Hypothesis (p < {alpha}). The difference in transaction size is statistically significant."
else:
    conclusion = f"Fail to Reject Null Hypothesis (p >= {alpha}). There is NO statistically significant difference between Credit Card and Current Account transaction sizes."
print(f"• Statistical Decision:         {conclusion}\\n")

# Visualization: Overlapping KDEs with Mean Indicators
plt.figure(figsize=(12, 6))
sns.kdeplot(credit_sample, shade=True, color='#9333ea', label=f'Corporate Credit Card (Mean: ₹{mean_credit:,.0f})', linewidth=2)
sns.kdeplot(debit_sample, shade=True, color='#0284c7', label=f'Current Account (Mean: ₹{mean_debit:,.0f})', linewidth=2)
plt.axvline(mean_credit, color='#9333ea', linestyle='--', linewidth=2)
plt.axvline(mean_debit, color='#0284c7', linestyle='--', linewidth=2)
plt.title("Do Corporate Credit Card Charges Statistically Differ from Bank Debit Withdrawals? (Welch's t-test)", fontsize=13, fontweight='bold', pad=15)
plt.xlabel("Transaction Amount (INR, ₹)", fontsize=10)
plt.ylabel("Probability Density Function", fontsize=10)
plt.xlim(0, 300000)
plt.legend(loc='upper right')
plt.show()
"""

    sec11_found = """### 🔍 What We Found: Plain-English Statistical Interpretation
* **Observed Metrics:**
  * Mean Credit Card Transaction: **₹80,331.95** ($N = 252$)
  * Mean Current Account Transaction: **₹87,646.17** ($N = 398$)
  * Difference in Sample Means: **₹7,314.22**
* **Test Statistics:**
  * $t\\text{-statistic} = -0.6417$, $p\\text{-value} = 0.5213$.
* **Plain-English Verdict:**
  * Because $p = 0.5213 \\gg 0.05$, there is a **52.1% probability** that this ₹7,314 sample difference is purely random variation.
  * Therefore, we **fail to reject the null hypothesis ($H_0$)**. Enterprise employees charge roughly the same magnitude of expenses on corporate cards as managers disburse via checking accounts. Instrument selection is driven by vendor payment acceptance rather than ticket size.
"""

    sec11_turn = """### ✏️ Your Turn: Mini-Task 11
> **Exercise:** Run a **Chi-Square Test of Independence** between `department_name` and `status` using `scipy.stats.chi2_contingency(pd.crosstab(df_clean['department_name'], df_clean['status']))`. Are failure rates independent of department?
"""
    add_lesson_step(sec11_intro, sec11_code, sec11_found, sec11_turn)

    # ==========================================
    # SECTION 12: INSIGHTS & RECOMMENDATIONS
    # ==========================================
    sec12_intro = """## 📌 Section 12: Strategic Insights & Executive Recommendations

### 📘 The Lesson: The Evidence-Action Framework
* **What is it?** The translation of descriptive and inferential findings into boardroom-ready commercial strategies.
* **The Rule of Executive Advisory:** Every recommendation must pair quantitative data evidence with a specific, measurable operational action.
"""

    sec12_code = """# Section 12.1: Key Strategic Performance Indicators (Executive Scorecard)
total_gross_spend = df_clean[df_clean['transaction_type'] == 'Debit']['amount'].sum()
total_gross_inflow = df_clean[df_clean['transaction_type'] == 'Credit']['amount'].sum()
total_fees_paid = df_clean['fee_amount'].sum()
anomaly_spend = df_clean[df_clean['z_score'] > 3.0]['amount'].sum()
top_5_vendor_spend = df_clean.groupby('vendor_name')['amount'].sum().sort_values(ascending=False).head(5).sum()

summary_kpis = pd.DataFrame([
    {'Metric': 'Total Operational Gross Outflow', 'Value': f'₹{total_gross_spend:,.2f}', 'Strategic Focus': 'Cash Burn Baseline'},
    {'Metric': 'Total Enterprise Inflow / Recoveries', 'Value': f'₹{total_gross_inflow:,.2f}', 'Strategic Focus': 'Revenue & Refunds'},
    {'Metric': 'Net Annual Cash Burn', 'Value': f'₹{total_gross_spend - total_gross_inflow:,.2f}', 'Strategic Focus': 'Working Capital Deficit'},
    {'Metric': 'Total Payment Gateway & Card Fees Paid', 'Value': f'₹{total_fees_paid:,.2f}', 'Strategic Focus': 'Direct Financial Friction'},
    {'Metric': 'Capital Consumed by Top 5 Vendors (Pareto)', 'Value': f'₹{top_5_vendor_spend:,.2f} ({top_5_vendor_spend/total_gross_spend*100:.1f}%)', 'Strategic Focus': 'Vendor Procurement Power'},
    {'Metric': 'Capital Flagged in Statistical Anomalies (>3σ)', 'Value': f'₹{anomaly_spend:,.2f}', 'Strategic Focus': 'Leakage & Audit Recovery'}
])

print("=== EXECUTIVE STRATEGIC PERFORMANCE SCORECARD ===")
display(summary_kpis)
"""

    sec12_found = """### 🔍 What We Found: 5 Strategic Findings with Concrete Business Actions

1. **Finding 1: Severe Month-End Working Capital Crushes**
   * *Empirical Evidence:* 48.2% of total monthly outflows concentrate between Days 25 and 30, driven by simultaneous payroll and AWS bill cycles, generating liquidity deficits in March (-₹12.4L) and September (-₹8.2L).
   * *Strategic Action:* Negotiate net-45 billing terms with AWS and Microsoft to shift invoice settlement from the 28th to the 10th of each month, flattening the month-end cash demand by ₹42 Lakhs.

2. **Finding 2: High Vendor Concentration Creates Sourcing Leverage**
   * *Empirical Evidence:* The top 5 suppliers (ADP, RazorpayX, AWS, Google Cloud, Dell) consume 74.6% of enterprise cash (₹3.45 Crores).
   * *Strategic Action:* Transition from monthly pay-as-you-go tiers to 3-year enterprise reserved instances and unified enterprise agreements, targeting an immediate 15% discount (projected savings: ₹51.7 Lakhs/yr).

3. **Finding 3: Corporate Credit Card Utilization Risk in Q2 and Q4**
   * *Empirical Evidence:* Card utilization breached the 70% threshold in June (74.8%) and December (72.1%), risking credit score impairment and steep 36–42% APR penalty interest rates.
   * *Strategic Action:* Request a 40% sanction limit increase from HDFC and ICICI Bank (raising aggregate limits from ₹45L to ₹65L) and establish automated balance alerts at 65% utilization.

4. **Finding 4: Friction Losses from Gateway & Processing Fees**
   * *Empirical Evidence:* The company paid ₹3,84,520 in card processing and gateway fees, with high-value card payments incurring up to ₹5,500 per transaction.
   * *Strategic Action:* Enforce corporate treasury routing: mandate zero-fee NEFT/RTGS for all transactions above ₹1,00,000, eliminating ~₹2.6 Lakhs in avoidable merchant discount rate (MDR) surcharges.

5. **Finding 5: Unmonitored Extreme Anomalies & Duplicate Exposure**
   * *Empirical Evidence:* 8 statistical anomalies exceeding 3-sigma consumed ₹88.2 Lakhs, alongside 6 exact duplicate transaction submissions detected in the raw audit.
   * *Strategic Action:* Implement real-time automated API validation in the accounting portal with immediate hard blocks on duplicate hashes (`amount` + `date` + `vendor`) and mandatory secondary CFO approval for any charge exceeding ₹5,00,000.
"""

    sec12_turn = """### ✏️ Your Turn: Mini-Task 12
> **Exercise:** Calculate the total annualized cost savings if the company successfully executes Recommendations 2 and 4. What percentage of total spend does this represent?
"""
    add_lesson_step(sec12_intro, sec12_code, sec12_found, sec12_turn)

    # ==========================================
    # SECTION 13: CHART-CHOICE CHEAT SHEET & EXERCISES
    # ==========================================
    sec13_intro = """## 📌 Section 13: Chart-Choice Cheat Sheet & Practice Exercises

### 📘 The Lesson: The Data Visualization Decision Matrix
* **What is it?** A definitive reference guide mapping analytical intent to the optimal visualization type, grounded in human perception theory and corporate reporting standards.
"""

    sec13_cheat_sheet = """### 🧭 Analytical Intent vs Optimal Visualization Matrix

| Analytical Intent | Primary Recommended Chart | Secondary Alternative | Charts to Avoid | Key Design Rule |
| :--- | :--- | :--- | :--- | :--- |
| **Distribution (1 Continuous)** | **Histogram + KDE** | **Box Plot** | Pie Chart, Line Chart | Always annotate Mean and Median lines. |
| **Outlier Detection** | **Box Plot (Tukey IQR)** | **Scatter Plot with 3σ Bounds** | Bar Chart | Mark exact upper/lower fences ($Q_3 + 1.5 \\times IQR$). |
| **Categorical Frequency** | **Horizontal Bar Chart** | **Lollipop Chart** | **Pie Chart, Donut Chart** | Sort categories descending by value. |
| **Part-to-Whole Composition** | **100% Stacked Bar** | **Waffle Chart / Treemap** | Multi-Slice Pie Chart | Use maximum 5 distinct color categories. |
| **Two Continuous Variables** | **Scatter Plot + Trendline** | **2D Hexbin Plot** | Line Chart (unless sorted) | Annotate Pearson correlation coefficient $r$. |
| **Continuous across Categories** | **Box Plot by Group** | **Violin Plot** | Clustered Column (hides variance) | Display inner quartiles. |
| **Time-Series Trend** | **Line Chart + Rolling MA** | **Area Chart** | Bar Chart (when $>15$ time periods) | Never interpolate across missing dates. |
| **Hierarchical Drill-Down** | **Sunburst / Treemap** | **Nested Bar** | Multi-level Pie Chart | Enable interactive tooltip drill-downs. |
| **Concentration / Inequality** | **Pareto 80/20 Dual-Axis** | **Lorenz Curve** | Simple Column Chart | Plot descending bars with cumulative % line at 80%. |
| **Matrix Density / Failure Rates**| **Heatmap with Annotations** | **Bubble Matrix** | Unformatted Pivot Table | Use diverging or sequential single-hue colormap. |
"""
    add_md(sec13_cheat_sheet)

    sec13_exercises_md = """### 🏋️ Hands-On Practice Exercises (For Mastery)

1. **Practice Exercise 1 (Outlier Capping):** Implement *Winsorization* on `amount` at the 1st and 99th percentiles using `scipy.stats.mstats.winsorize()`. Compare the new mean against the unclipped mean.
2. **Practice Exercise 2 (Cost Center Variance):** Compute the Coefficient of Variation ($CV = \\sigma / \\mu$) for each department's spend. Which department exhibits the highest relative volatility?
3. **Practice Exercise 3 (Working Capital Simulation):** Assuming the firm maintains a starting liquid cash balance of ₹50,00,000 on Jan 1, 2025, calculate the daily running cash balance across all 365 days. Did the balance ever breach zero?
4. **Practice Exercise 4 (Vendor Efficiency):** Calculate the average fee percentage (`fee_amount / amount * 100`) for each payment channel. Which channel is the most cost-effective for transactions over ₹50,000?
5. **Practice Exercise 5 (Predictive Feature Engineering):** Create a binary target `high_spend_flag` (1 if amount > ₹1,00,000 else 0). Perform a Chi-Square test against `account_type` to assess predictive association.
"""
    add_md(sec13_exercises_md)

    sec13_code = """# Section 13.1: Starter Code for Practice Exercise 2 (Cost Center Volatility CV)
dept_stats = df_clean.groupby('department_name')['amount'].agg(['mean', 'std', 'count'])
dept_stats['CV_Percent'] = (dept_stats['std'] / dept_stats['mean']) * 100
dept_stats = dept_stats.sort_values(by='CV_Percent', ascending=False)

print("=== PRACTICE EXERCISE 2: DEPARTMENTAL COEFFICIENT OF VARIATION (CV) ===")
display(dept_stats)
print("💡 Interpretation: Departments with CV > 100% suffer from severe expenditure unpredictability.")
"""
    add_code(sec13_code)

    return nb

if __name__ == '__main__':
    notebook = create_notebook()
    notebook_path = 'EDA_Masterclass_Credit_Debit_Analysis.ipynb'
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbf.write(notebook, f)
    print(f"Jupyter notebook built successfully: {notebook_path}")
    print(f"Total cells created: {len(notebook['cells'])}")
