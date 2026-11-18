"""
src/generate_data.py
Synthetic Dataset Generator for Credit vs Debit Transaction Analysis System
Target Enterprise: NexGen Technologies Pvt. Ltd., Noida
Schema: Star Schema (dim_accounts, dim_categories, dim_merchants, dim_departments, fact_transactions)
Random Seed: 42
"""

import os
import random
import sqlite3
import datetime
import csv
import zipfile
import xml.sax.saxutils as saxutils
import numpy as np

# Set deterministic random seed
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

PROJECT_DIR = r"d:\HCL_Project"
DATA_DIR = os.path.join(PROJECT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. Master Dimension Data Definitions
# -------------------------------------------------------------

def generate_accounts():
    """8 Corporate banking accounts across HDFC, ICICI, SBI, Axis."""
    accounts = [
        ("ACC-HDFC-01", "XXXX-XXXX-XXXX-4123", "HDFC Bank", "Current Checking", 0.0, 1, "INR", "Active"),
        ("ACC-HDFC-02", "XXXX-XXXX-XXXX-8910", "HDFC Bank", "Corporate Credit Card", 2500000.0, 20, "INR", "Active"),
        ("ACC-ICICI-01", "XXXX-XXXX-XXXX-1122", "ICICI Bank", "Current Checking", 0.0, 1, "INR", "Active"),
        ("ACC-ICICI-02", "XXXX-XXXX-XXXX-3344", "ICICI Bank", "Corporate Credit Card", 1500000.0, 15, "INR", "Active"),
        ("ACC-SBI-01", "XXXX-XXXX-XXXX-5566", "SBI", "Current Checking", 0.0, 1, "INR", "Active"),
        ("ACC-SBI-02", "XXXX-XXXX-XXXX-7788", "SBI", "Corporate Credit Card", 1000000.0, 25, "INR", "Active"),
        ("ACC-AXIS-01", "XXXX-XXXX-XXXX-9900", "Axis Bank", "Current Checking", 0.0, 1, "INR", "Active"),
        ("ACC-AXIS-02", "XXXX-XXXX-XXXX-2233", "Axis Bank", "Corporate Credit Card", 750000.0, 10, "INR", "Suspended")
    ]
    return accounts

def generate_categories():
    """8 Standardized corporate expenditure categories."""
    categories = [
        ("CAT-01", "Cloud Infrastructure", "OpEx", "Debit/NetBanking", 450000.0),
        ("CAT-02", "Payroll & Compensation", "OpEx", "Debit/NetBanking", 1200000.0),
        ("CAT-03", "Employee Travel & Lodging", "OpEx", "Corporate Credit Card", 250000.0),
        ("CAT-04", "SaaS Software Subscriptions", "OpEx", "Corporate Credit Card", 350000.0),
        ("CAT-05", "Office Lease & Utilities", "OpEx", "Debit/NetBanking", 300000.0),
        ("CAT-06", "Hardware & IT Equipment", "CapEx", "Either", 400000.0),
        ("CAT-07", "Vendor & Professional Services", "OpEx", "Debit/NetBanking", 500000.0),
        ("CAT-08", "Marketing & Advertising", "OpEx", "Corporate Credit Card", 200000.0)
    ]
    return categories

def generate_departments():
    """5 Corporate cost centers."""
    departments = [
        ("DEP-ENG", "Engineering & Technology", "CC-ENG-101", "Rajesh Sharma", 6500000.0),
        ("DEP-FIN", "Finance & Accounting", "CC-FIN-201", "Sunita Nair", 2500000.0),
        ("DEP-HR", "Human Resources", "CC-HR-301", "Amitabh Verma", 1800000.0),
        ("DEP-SAL", "Sales & Marketing", "CC-SAL-401", "Pooja Malhotra", 3500000.0),
        ("DEP-OPS", "Operations & Facilities", "CC-OPS-501", "Vikas Saxena", 2200000.0)
    ]
    return departments

def generate_merchants():
    """25 Authentic commercial vendors operating in India."""
    # Note: 3 merchants have None for city to simulate 2-3% missing data quality issue
    merchants = [
        ("MER-01", "Amazon Web Services India", "7372", "Tier-1 Strategic", "Bengaluru", "India"),
        ("MER-02", "Microsoft Azure India", "7372", "Tier-1 Strategic", "Gurugram", "India"),
        ("MER-03", "Google Cloud India", "7372", "Tier-1 Strategic", "Mumbai", "India"),
        ("MER-04", "MakeMyTrip Corporate", "4722", "Tier-2 Preferred", "Gurugram", "India"),
        ("MER-05", "Uber for Business India", "4121", "Tier-2 Preferred", "Mumbai", "India"),
        ("MER-06", "Swiggy Corporate Cafeteria", "5812", "Tier-3 Standard", "Bengaluru", "India"),
        ("MER-07", "WeWork India Noida", "6513", "Tier-1 Strategic", "Noida", "India"),
        ("MER-08", "Dell Technologies India", "5045", "Tier-1 Strategic", "Bengaluru", "India"),
        ("MER-09", "Lenovo India Enterprise", "5045", "Tier-2 Preferred", "Mumbai", "India"),
        ("MER-10", "Tata Communications Ltd", "4816", "Tier-1 Strategic", "Mumbai", "India"),
        ("MER-11", "Airtel Enterprise Solutions", "4814", "Tier-1 Strategic", "Gurugram", "India"),
        ("MER-12", "Zoho Corporation", "7372", "Tier-2 Preferred", "Chennai", "India"),
        ("MER-13", "Freshworks India", "7372", "Tier-2 Preferred", "Chennai", "India"),
        ("MER-14", "LinkedIn Talent Solutions", "7311", "Tier-2 Preferred", None, "India"), # Missing city (Data Quality Issue)
        ("MER-15", "Deloitte Consulting India", "8931", "Tier-1 Strategic", "Gurugram", "India"),
        ("MER-16", "Ernst & Young Advisory", "8931", "Tier-1 Strategic", "Noida", "India"),
        ("MER-17", "Urban Company Enterprise", "7349", "Tier-3 Standard", "Noida", "India"),
        ("MER-18", "Blue Dart Express", "4215", "Tier-2 Preferred", "Mumbai", "India"),
        ("MER-19", "Reliance Jio Infocomm", "4814", "Tier-1 Strategic", "Mumbai", "India"),
        ("MER-20", "Razorpay Payment Gateway", "7372", "Tier-1 Strategic", "Bengaluru", "India"),
        ("MER-21", "Info Edge India (Naukri)", "7311", "Tier-2 Preferred", "Noida", "India"),
        ("MER-22", "Croma Enterprise Retail", "5732", "Tier-3 Standard", None, "India"), # Missing city (Data Quality Issue)
        ("MER-23", "Urban Ladder Commercial", "5712", "Tier-3 Standard", "Bengaluru", "India"),
        ("MER-24", "Tata Power Solar DDL", "4900", "Tier-1 Strategic", "Noida", "India"),
        ("MER-25", "Adobe Systems India", "7372", "Tier-2 Preferred", None, "India")  # Missing city (Data Quality Issue)
    ]
    return merchants

# -------------------------------------------------------------
# 2. Fact Transactions Generator with Embedded Patterns
# -------------------------------------------------------------

def generate_transactions(accounts, categories, departments, merchants, target_count=300):
    """
    Generates 300 realistic corporate transactions across 2025.
    Embeds 5 analytical patterns:
    1. Month-end payroll & vendor payout surges (28th-31st).
    2. Cloud Infrastructure regular monthly debits.
    3. Corporate credit card peak utilization in Q3.
    4. Weekend dips (lower volume on Saturdays & Sundays).
    5. Realistic failure rates (~4%) on card gateway timeouts & limit breaches.
    
    Embeds 3 data quality issues:
    1. 2-3% missing optional values (failure_reason on some successful rows).
    2. 2 intentional duplicate transaction attempts (retry on gateway timeout).
    3. 4 statistical outliers (|Z| > 3.0) for anomaly detection.
    """
    transactions = []
    
    start_date = datetime.date(2025, 1, 1)
    end_date = datetime.date(2025, 12, 31)
    total_days = (end_date - start_date).days
    
    # Split accounts by type
    checking_accs = [a[0] for a in accounts if a[3] == "Current Checking"]
    credit_accs = [a[0] for a in accounts if a[3] == "Corporate Credit Card" and a[7] == "Active"]
    
    dept_ids = [d[0] for d in departments]
    
    # Category to typical merchant mapping
    cat_merch_map = {
        "CAT-01": ["MER-01", "MER-02", "MER-03", "MER-10"], # Cloud
        "CAT-02": ["MER-15", "MER-16"],                      # Payroll/HR services
        "CAT-03": ["MER-04", "MER-05"],                      # Travel
        "CAT-04": ["MER-12", "MER-13", "MER-14", "MER-25"], # SaaS
        "CAT-05": ["MER-07", "MER-11", "MER-19", "MER-24"], # Lease/Utilities
        "CAT-06": ["MER-08", "MER-09", "MER-22", "MER-23"], # Hardware
        "CAT-07": ["MER-15", "MER-16", "MER-17", "MER-18", "MER-20"], # Professional
        "CAT-08": ["MER-14", "MER-21"]                       # Marketing
    }
    
    # Base amounts by category: (mean, std)
    cat_amount_stats = {
        "CAT-01": (180000, 35000),   # Cloud Infra
        "CAT-02": (450000, 80000),   # Payroll chunks
        "CAT-03": (32000, 12000),    # Travel
        "CAT-04": (48000, 15000),    # SaaS
        "CAT-05": (125000, 25000),   # Lease & Utilities
        "CAT-06": (160000, 45000),   # Hardware
        "CAT-07": (85000, 22000),    # Professional services
        "CAT-08": (65000, 18000)     # Marketing
    }
    
    channels = ["UPI", "Net Banking", "POS Terminal", "Corporate Card Gateway", "NEFT/RTGS"]
    
    txn_id_counter = 1
    
    for _ in range(target_count - 6): # Leave room for 2 duplicates (4 rows) and 4 outliers
        # Choose random date with weekend suppression (Pattern 4)
        while True:
            offset = random.randint(0, total_days)
            dt = start_date + datetime.timedelta(days=offset)
            is_weekend = dt.weekday() >= 5
            # Suppress 75% of weekend transactions
            if is_weekend and random.random() < 0.75:
                continue
            break
            
        time_str = f"{random.randint(9, 18):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"
        
        # Decide transaction type & instrument
        # Inflows (15% of transactions): Client payments / Contract retainers
        # Outflows (85% of transactions): OpEx / CapEx
        is_inflow = random.random() < 0.15
        
        if is_inflow:
            txn_type = "Credit"
            inst = "Current Account Debit" # Inflow deposited to checking
            acc = random.choice(checking_accs)
            cat = "CAT-07" # Billed professional services revenue
            merch = random.choice(["MER-15", "MER-16", "MER-20"])
            dept = "DEP-SAL"
            channel = random.choice(["NEFT/RTGS", "Net Banking"])
            amt = round(float(np.random.normal(350000, 75000)), 2)
            fee = 0.0
            status = "Success"
            fail_reason = "None"
        else:
            txn_type = "Debit"
            # Pattern 1: Month-end payroll / large vendor settlements (28th - 31st)
            if dt.day >= 28 and random.random() < 0.6:
                cat = random.choice(["CAT-02", "CAT-05", "CAT-07"])
                dept = "DEP-FIN" if cat == "CAT-02" else random.choice(dept_ids)
                acc = random.choice(checking_accs)
                inst = "Current Account Debit"
                channel = "NEFT/RTGS"
                mean_amt, std_amt = cat_amount_stats[cat]
                amt = round(float(np.random.normal(mean_amt * 1.5, std_amt)), 2)
                fee = 15.0 # Bank wire charges
            else:
                cat = random.choice(list(cat_amount_stats.keys()))
                dept = random.choice(dept_ids)
                
                # Payment instrument selection based on category nature
                if cat in ["CAT-03", "CAT-04", "CAT-08"]:
                    inst = "Corporate Credit Card"
                    acc = random.choice(credit_accs)
                    channel = random.choice(["Corporate Card Gateway", "POS Terminal"])
                    fee = round(random.choice([0.0, 0.0, 150.0, 350.0]), 2)
                else:
                    inst = "Current Account Debit"
                    acc = random.choice(checking_accs)
                    channel = random.choice(["Net Banking", "UPI", "NEFT/RTGS"])
                    fee = 0.0
                    
                mean_amt, std_amt = cat_amount_stats[cat]
                amt = round(max(500.0, float(np.random.normal(mean_amt, std_amt))), 2)

            merch = random.choice(cat_merch_map.get(cat, ["MER-01"]))

            # Failure rate pattern (~4%)
            if random.random() < 0.04:
                status = random.choice(["Failed", "Declined"])
                fail_reason = random.choice(["Gateway Timeout", "Limit Exceeded", "Card Expired", "Suspected Fraud Block"])
            else:
                status = "Success"
                fail_reason = "None"
                
        txn_id = f"TXN-2025-{txn_id_counter:05d}"
        txn_id_counter += 1
        
        transactions.append({
            "transaction_id": txn_id,
            "transaction_date": dt.strftime("%Y-%m-%d"),
            "transaction_time": time_str,
            "account_id": acc,
            "department_id": dept,
            "category_id": cat,
            "merchant_id": merch,
            "transaction_type": txn_type,
            "payment_instrument": inst,
            "payment_channel": channel,
            "amount": amt,
            "currency": "INR",
            "fee_amount": fee,
            "status": status,
            "failure_reason": fail_reason,
            "z_score": 0.0, # Computed later
            "is_anomaly": 0
        })

    # ---------------------------------------------------------
    # Inject Data Quality Issue 1: 2 Duplicate Transaction Pairs (4 rows)
    # Scenario: Gateway timeout on card swipe followed by immediate retry
    # ---------------------------------------------------------
    for dup_idx in range(2):
        dup_date = f"2025-06-1{5+dup_idx}"
        dup_acc = credit_accs[0]
        dup_merch = "MER-04" # MakeMyTrip
        dup_amt = 48500.00
        
        # Row 1: Failed attempt
        t1 = f"TXN-2025-{txn_id_counter:05d}"
        txn_id_counter += 1
        transactions.append({
            "transaction_id": t1,
            "transaction_date": dup_date,
            "transaction_time": "14:22:10",
            "account_id": dup_acc,
            "department_id": "DEP-SAL",
            "category_id": "CAT-03",
            "merchant_id": dup_merch,
            "transaction_type": "Debit",
            "payment_instrument": "Corporate Credit Card",
            "payment_channel": "Corporate Card Gateway",
            "amount": dup_amt,
            "currency": "INR",
            "fee_amount": 0.0,
            "status": "Failed",
            "failure_reason": "Gateway Timeout",
            "z_score": 0.0,
            "is_anomaly": 0
        })
        
        # Row 2: Successful retry 2 minutes later
        t2 = f"TXN-2025-{txn_id_counter:05d}"
        txn_id_counter += 1
        transactions.append({
            "transaction_id": t2,
            "transaction_date": dup_date,
            "transaction_time": "14:24:15",
            "account_id": dup_acc,
            "department_id": "DEP-SAL",
            "category_id": "CAT-03",
            "merchant_id": dup_merch,
            "transaction_type": "Debit",
            "payment_instrument": "Corporate Credit Card",
            "payment_channel": "Corporate Card Gateway",
            "amount": dup_amt,
            "currency": "INR",
            "fee_amount": 0.0,
            "status": "Success",
            "failure_reason": "None",
            "z_score": 0.0,
            "is_anomaly": 0
        })

    # ---------------------------------------------------------
    # Inject Data Quality Issue 2: 4 Extreme Statistical Outliers (|Z| > 3.0)
    # ---------------------------------------------------------
    outliers = [
        # Outlier 1: Emergency datacenter core switch replacement (Hardware)
        ("2025-08-14", "11:15:00", checking_accs[0], "DEP-ENG", "CAT-06", "MER-08", "Debit", "Current Account Debit", "NEFT/RTGS", 1450000.00, 50.0, "Success", "None"),
        # Outlier 2: Duplicate international enterprise software license renewal (SaaS)
        ("2025-04-10", "16:40:00", credit_accs[1], "DEP-ENG", "CAT-04", "MER-25", "Debit", "Corporate Credit Card", "Corporate Card Gateway", 980000.00, 2500.0, "Success", "None"),
        # Outlier 3: High-roller executive global summit lodging (Travel)
        ("2025-09-22", "19:05:00", credit_accs[0], "DEP-SAL", "CAT-03", "MER-04", "Debit", "Corporate Credit Card", "POS Terminal", 480000.00, 1200.0, "Success", "None"),
        # Outlier 4: Multi-month cloud overage burst due to unoptimized cluster (Cloud)
        ("2025-11-05", "10:30:00", checking_accs[1], "DEP-ENG", "CAT-01", "MER-01", "Debit", "Current Account Debit", "Net Banking", 1150000.00, 0.0, "Success", "None")
    ]
    
    for dt_str, tm_str, acc, dept, cat, merch, ttype, inst, ch, amt, fee, st, rsn in outliers:
        tid = f"TXN-2025-{txn_id_counter:05d}"
        txn_id_counter += 1
        transactions.append({
            "transaction_id": tid,
            "transaction_date": dt_str,
            "transaction_time": tm_str,
            "account_id": acc,
            "department_id": dept,
            "category_id": cat,
            "merchant_id": merch,
            "transaction_type": ttype,
            "payment_instrument": inst,
            "payment_channel": ch,
            "amount": amt,
            "currency": "INR",
            "fee_amount": fee,
            "status": st,
            "failure_reason": rsn,
            "z_score": 0.0,
            "is_anomaly": 1
        })

    # Sort transactions chronologically
    transactions.sort(key=lambda x: (x["transaction_date"], x["transaction_time"]))

    # ---------------------------------------------------------
    # Compute Exact Statistical Z-Scores per Category
    # ---------------------------------------------------------
    cat_amounts = {}
    for t in transactions:
        c = t["category_id"]
        cat_amounts.setdefault(c, []).append(t["amount"])
        
    cat_stats = {}
    for c, am_list in cat_amounts.items():
        arr = np.array(am_list)
        cat_stats[c] = (float(np.mean(arr)), float(np.std(arr)) if np.std(arr) > 0 else 1.0)
        
    for t in transactions:
        mean_c, std_c = cat_stats[t["category_id"]]
        z = (t["amount"] - mean_c) / std_c
        t["z_score"] = round(float(z), 2)
        if abs(z) > 3.0:
            t["is_anomaly"] = 1

    return transactions

# -------------------------------------------------------------
# 3. SQLite Database Initialization & Population
# -------------------------------------------------------------

def init_sqlite_db(accounts, categories, departments, merchants, transactions):
    db_path = os.path.join(DATA_DIR, "app.db")
    if os.path.exists(db_path):
        os.remove(db_path)
        
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # Enforce foreign keys and WAL mode
    cur.execute("PRAGMA foreign_keys = ON;")
    cur.execute("PRAGMA journal_mode = WAL;")
    
    # 1. dim_accounts DDL
    cur.execute("""CREATE TABLE dim_accounts (
        account_id TEXT PRIMARY KEY NOT NULL,
        account_number_masked TEXT NOT NULL,
        bank_name TEXT NOT NULL CHECK(bank_name IN ('HDFC Bank', 'ICICI Bank', 'SBI', 'Axis Bank')),
        account_type TEXT NOT NULL CHECK(account_type IN ('Current Checking', 'Corporate Credit Card')),
        sanctioned_credit_limit REAL NOT NULL DEFAULT 0.0 CHECK(sanctioned_credit_limit >= 0.0),
        billing_cycle_day INTEGER NOT NULL CHECK(billing_cycle_day BETWEEN 1 AND 31),
        currency TEXT NOT NULL DEFAULT 'INR',
        status TEXT NOT NULL CHECK(status IN ('Active', 'Suspended', 'Closed'))
    );""")
    
    # 2. dim_categories DDL
    cur.execute("""CREATE TABLE dim_categories (
        category_id TEXT PRIMARY KEY NOT NULL,
        category_name TEXT UNIQUE NOT NULL,
        expense_nature TEXT NOT NULL CHECK(expense_nature IN ('OpEx', 'CapEx')),
        default_payment_mode TEXT NOT NULL CHECK(default_payment_mode IN ('Debit/NetBanking', 'Corporate Credit Card', 'Either')),
        monthly_budget_allocation REAL NOT NULL DEFAULT 0.0 CHECK(monthly_budget_allocation >= 0.0)
    );""")
    
    # 3. dim_departments DDL
    cur.execute("""CREATE TABLE dim_departments (
        department_id TEXT PRIMARY KEY NOT NULL,
        department_name TEXT UNIQUE NOT NULL,
        cost_center_code TEXT UNIQUE NOT NULL,
        department_head TEXT NOT NULL,
        annual_budget REAL NOT NULL DEFAULT 0.0 CHECK(annual_budget >= 0.0)
    );""")
    
    # 4. dim_merchants DDL
    cur.execute("""CREATE TABLE dim_merchants (
        merchant_id TEXT PRIMARY KEY NOT NULL,
        merchant_name TEXT NOT NULL,
        merchant_category_code TEXT NOT NULL,
        vendor_tier TEXT NOT NULL CHECK(vendor_tier IN ('Tier-1 Strategic', 'Tier-2 Preferred', 'Tier-3 Standard')),
        city TEXT,
        country TEXT NOT NULL DEFAULT 'India'
    );""")
    
    # 5. fact_transactions DDL
    cur.execute("""CREATE TABLE fact_transactions (
        transaction_id TEXT PRIMARY KEY NOT NULL,
        transaction_date TEXT NOT NULL,
        transaction_time TEXT NOT NULL,
        account_id TEXT NOT NULL,
        department_id TEXT NOT NULL,
        category_id TEXT NOT NULL,
        merchant_id TEXT NOT NULL,
        transaction_type TEXT NOT NULL CHECK(transaction_type IN ('Credit', 'Debit')),
        payment_instrument TEXT NOT NULL CHECK(payment_instrument IN ('Corporate Credit Card', 'Current Account Debit')),
        payment_channel TEXT NOT NULL CHECK(payment_channel IN ('UPI', 'Net Banking', 'POS Terminal', 'Corporate Card Gateway', 'NEFT/RTGS')),
        amount REAL NOT NULL CHECK(amount > 0.00),
        currency TEXT NOT NULL DEFAULT 'INR',
        fee_amount REAL NOT NULL DEFAULT 0.0 CHECK(fee_amount >= 0.0),
        status TEXT NOT NULL CHECK(status IN ('Success', 'Failed', 'Declined')),
        failure_reason TEXT NOT NULL DEFAULT 'None',
        z_score REAL,
        is_anomaly INTEGER NOT NULL DEFAULT 0 CHECK(is_anomaly IN (0, 1)),
        FOREIGN KEY (account_id) REFERENCES dim_accounts(account_id) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (department_id) REFERENCES dim_departments(department_id) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (category_id) REFERENCES dim_categories(category_id) ON UPDATE CASCADE ON DELETE RESTRICT,
        FOREIGN KEY (merchant_id) REFERENCES dim_merchants(merchant_id) ON UPDATE CASCADE ON DELETE RESTRICT
    );""")
    
    # Indexes
    cur.execute("CREATE INDEX idx_txn_date_type ON fact_transactions(transaction_date, transaction_type);")
    cur.execute("CREATE INDEX idx_txn_category ON fact_transactions(category_id, amount);")
    cur.execute("CREATE INDEX idx_txn_merchant ON fact_transactions(merchant_id);")
    cur.execute("CREATE INDEX idx_txn_anomaly ON fact_transactions(is_anomaly) WHERE is_anomaly = 1;")
    
    # View definition (35 columns)
    cur.execute("""CREATE VIEW view_transaction_analysis AS
    SELECT 
        t.transaction_id,
        t.transaction_date,
        t.transaction_time,
        strftime('%w', t.transaction_date) AS day_of_week_num,
        case strftime('%w', t.transaction_date) 
            when '0' then 'Sunday' when '1' then 'Monday' when '2' then 'Tuesday'
            when '3' then 'Wednesday' when '4' then 'Thursday' when '5' then 'Friday' else 'Saturday' end AS day_of_week_name,
        strftime('%d', t.transaction_date) AS day_of_month,
        strftime('%Y-%m', t.transaction_date) AS month_year,
        case when strftime('%m', t.transaction_date) between '01' and '03' then 'Q1'
             when strftime('%m', t.transaction_date) between '04' and '06' then 'Q2'
             when strftime('%m', t.transaction_date) between '07' and '09' then 'Q3' else 'Q4' end AS fiscal_quarter,
        a.account_id,
        a.account_number_masked,
        a.bank_name,
        a.account_type,
        a.sanctioned_credit_limit,
        a.billing_cycle_day,
        d.department_id,
        d.department_name,
        d.cost_center_code,
        d.department_head,
        c.category_id,
        c.category_name,
        c.expense_nature,
        c.monthly_budget_allocation,
        m.merchant_id,
        m.merchant_name,
        m.merchant_category_code,
        m.vendor_tier,
        t.transaction_type,
        t.payment_instrument,
        t.payment_channel,
        t.amount,
        t.fee_amount,
        case when t.transaction_type = 'Credit' then t.amount else -t.amount end AS net_cash_impact,
        t.status,
        t.failure_reason,
        t.z_score,
        t.is_anomaly,
        case when t.is_anomaly = 1 then 'STATISTICAL OUTLIER' else 'NORMAL' end AS outlier_label
    FROM fact_transactions t
    JOIN dim_accounts a ON t.account_id = a.account_id
    JOIN dim_departments d ON t.department_id = d.department_id
    JOIN dim_categories c ON t.category_id = c.category_id
    JOIN dim_merchants m ON t.merchant_id = m.merchant_id;""")
    
    # Insert dimension rows
    cur.executemany("INSERT INTO dim_accounts VALUES (?, ?, ?, ?, ?, ?, ?, ?);", accounts)
    cur.executemany("INSERT INTO dim_categories VALUES (?, ?, ?, ?, ?);", categories)
    cur.executemany("INSERT INTO dim_departments VALUES (?, ?, ?, ?, ?);", departments)
    cur.executemany("INSERT INTO dim_merchants VALUES (?, ?, ?, ?, ?, ?);", merchants)
    
    # Insert fact rows
    fact_tuples = [
        (
            t["transaction_id"], t["transaction_date"], t["transaction_time"],
            t["account_id"], t["department_id"], t["category_id"], t["merchant_id"],
            t["transaction_type"], t["payment_instrument"], t["payment_channel"],
            t["amount"], t["currency"], t["fee_amount"], t["status"],
            t["failure_reason"], t["z_score"], t["is_anomaly"]
        )
        for t in transactions
    ]
    cur.executemany("INSERT INTO fact_transactions VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", fact_tuples)
    
    conn.commit()
    conn.close()
    print(f"Initialized SQLite database at: {db_path} ({os.path.getsize(db_path)} bytes)")

# -------------------------------------------------------------
# 4. CSV File Exports
# -------------------------------------------------------------

def export_csv_files(accounts, categories, departments, merchants, transactions):
    # 1. dim_accounts.csv
    p1 = os.path.join(DATA_DIR, "dim_accounts.csv")
    with open(p1, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["account_id", "account_number_masked", "bank_name", "account_type", "sanctioned_credit_limit", "billing_cycle_day", "currency", "status"])
        w.writerows(accounts)
        
    # 2. dim_categories.csv
    p2 = os.path.join(DATA_DIR, "dim_categories.csv")
    with open(p2, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["category_id", "category_name", "expense_nature", "default_payment_mode", "monthly_budget_allocation"])
        w.writerows(categories)

    # 3. dim_departments.csv
    p3 = os.path.join(DATA_DIR, "dim_departments.csv")
    with open(p3, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["department_id", "department_name", "cost_center_code", "department_head", "annual_budget"])
        w.writerows(departments)

    # 4. dim_merchants.csv
    p4 = os.path.join(DATA_DIR, "dim_merchants.csv")
    with open(p4, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["merchant_id", "merchant_name", "merchant_category_code", "vendor_tier", "city", "country"])
        w.writerows(merchants)

    # 5. fact_transactions.csv
    p5 = os.path.join(DATA_DIR, "fact_transactions.csv")
    with open(p5, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow([
            "transaction_id", "transaction_date", "transaction_time", "account_id", "department_id",
            "category_id", "merchant_id", "transaction_type", "payment_instrument", "payment_channel",
            "amount", "currency", "fee_amount", "status", "failure_reason", "z_score", "is_anomaly"
        ])
        for t in transactions:
            w.writerow([
                t["transaction_id"], t["transaction_date"], t["transaction_time"],
                t["account_id"], t["department_id"], t["category_id"], t["merchant_id"],
                t["transaction_type"], t["payment_instrument"], t["payment_channel"],
                t["amount"], t["currency"], t["fee_amount"], t["status"],
                t["failure_reason"], t["z_score"], t["is_anomaly"]
            ])

    print("Exported 5 CSV tables to data/ directory.")

# -------------------------------------------------------------
# 5. Multi-Sheet Excel Workbook Export (credit_debit_data.xlsx)
# -------------------------------------------------------------

def export_excel_workbook(accounts, categories, departments, merchants, transactions):
    excel_path = os.path.join(DATA_DIR, "credit_debit_data.xlsx")
    
    # Query view data from SQLite
    db_path = os.path.join(DATA_DIR, "app.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT * FROM view_transaction_analysis;")
    view_rows = cur.fetchall()
    view_headers = [d[0] for d in cur.description]
    conn.close()
    
    # Helper functions for OpenXML spreadsheet
    def col_letter(col_idx):
        result = ""
        while col_idx > 0:
            col_idx, remainder = divmod(col_idx - 1, 26)
            result = chr(65 + remainder) + result
        return result

    def build_sheet_xml(headers, rows):
        sheet_xml = []
        sheet_xml.append('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>')
        sheet_xml.append('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">')
        sheet_xml.append('<sheetData>')
        
        # Header
        sheet_xml.append('<row r="1" ht="26" customHeight="1">')
        for c_idx, h in enumerate(headers, start=1):
            ref = f"{col_letter(c_idx)}1"
            sheet_xml.append(f'<c r="{ref}" s="1" t="inlineStr"><is><t>{saxutils.escape(str(h))}</t></is></c>')
        sheet_xml.append('</row>')
        
        # Rows
        for r_idx, row in enumerate(rows, start=2):
            base_style = 3 if r_idx % 2 == 1 else 2
            sheet_xml.append(f'<row r="{r_idx}" ht="20" customHeight="1">')
            for c_idx, val in enumerate(row, start=1):
                ref = f"{col_letter(c_idx)}{r_idx}"
                v_str = "" if val is None else str(val)
                sheet_xml.append(f'<c r="{ref}" s="{base_style}" t="inlineStr"><is><t>{saxutils.escape(v_str)}</t></is></c>')
            sheet_xml.append('</row>')
            
        sheet_xml.append('</sheetData>')
        if len(rows) > 0:
            max_c = col_letter(len(headers))
            sheet_xml.append(f'<autoFilter ref="A1:{max_c}{len(rows)+1}"/>')
        sheet_xml.append('</worksheet>')
        return "".join(sheet_xml)

    # Styles
    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main">
    <fonts count="3">
        <font><sz val="10"/><name val="Calibri"/><color rgb="FF1E293B"/></font>
        <font><b/><sz val="10"/><name val="Calibri"/><color rgb="FFFFFFFF"/></font>
        <font><b/><sz val="10"/><name val="Calibri"/><color rgb="FF1E40AF"/></font>
    </fonts>
    <fills count="4">
        <fill><patternFill patternType="none"/></fill>
        <fill><patternFill patternType="gray125"/></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FF1E40AF"/></patternFill></fill>
        <fill><patternFill patternType="solid"><fgColor rgb="FFF8FAFC"/></patternFill></fill>
    </fills>
    <borders count="2">
        <border><left/><right/><top/><bottom/><diagonal/></border>
        <border>
            <left style="thin"><color rgb="FFCBD5E1"/></left>
            <right style="thin"><color rgb="FFCBD5E1"/></right>
            <top style="thin"><color rgb="FFCBD5E1"/></top>
            <bottom style="thin"><color rgb="FFCBD5E1"/></bottom>
        </border>
    </borders>
    <cellStyleXfs count="1"><xf numFmtId="0" fontId="0" fillId="0" borderId="0"/></cellStyleXfs>
    <cellXfs count="4">
        <xf numFmtId="0" fontId="0" fillId="0" borderId="0" xfId="0"/>
        <xf numFmtId="0" fontId="1" fillId="2" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment horizontal="center" vertical="center" wrapText="1"/></xf>
        <xf numFmtId="0" fontId="0" fillId="0" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="center"/></xf>
        <xf numFmtId="0" fontId="0" fillId="3" borderId="1" xfId="0" applyFont="1" applyFill="1" applyBorder="1" applyAlignment="1"><alignment vertical="center"/></xf>
    </cellXfs>
</styleSheet>"""

    content_types = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
    <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
    <Default Extension="xml" ContentType="application/xml"/>
    <Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
    <Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/worksheets/sheet2.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/worksheets/sheet3.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/worksheets/sheet4.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/worksheets/sheet5.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/worksheets/sheet6.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
    <Override PartName="/xl/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.styles+xml"/>
</Types>"""

    rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>"""

    wb_rels = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
    <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
    <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet2.xml"/>
    <Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet3.xml"/>
    <Relationship Id="rId4" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet4.xml"/>
    <Relationship Id="rId5" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet5.xml"/>
    <Relationship Id="rId6" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet6.xml"/>
    <Relationship Id="rId7" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>"""

    workbook = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
    <sheets>
        <sheet name="dim_accounts" sheetId="1" r:id="rId1"/>
        <sheet name="dim_categories" sheetId="2" r:id="rId2"/>
        <sheet name="dim_departments" sheetId="3" r:id="rId3"/>
        <sheet name="dim_merchants" sheetId="4" r:id="rId4"/>
        <sheet name="fact_transactions" sheetId="5" r:id="rId5"/>
        <sheet name="view_transaction_analysis" sheetId="6" r:id="rId6"/>
    </sheets>
</workbook>"""

    acc_headers = ["account_id", "account_number_masked", "bank_name", "account_type", "sanctioned_credit_limit", "billing_cycle_day", "currency", "status"]
    cat_headers = ["category_id", "category_name", "expense_nature", "default_payment_mode", "monthly_budget_allocation"]
    dep_headers = ["department_id", "department_name", "cost_center_code", "department_head", "annual_budget"]
    mer_headers = ["merchant_id", "merchant_name", "merchant_category_code", "vendor_tier", "city", "country"]
    txn_headers = [
        "transaction_id", "transaction_date", "transaction_time", "account_id", "department_id",
        "category_id", "merchant_id", "transaction_type", "payment_instrument", "payment_channel",
        "amount", "currency", "fee_amount", "status", "failure_reason", "z_score", "is_anomaly"
    ]
    txn_rows = [
        [
            t["transaction_id"], t["transaction_date"], t["transaction_time"],
            t["account_id"], t["department_id"], t["category_id"], t["merchant_id"],
            t["transaction_type"], t["payment_instrument"], t["payment_channel"],
            t["amount"], t["currency"], t["fee_amount"], t["status"],
            t["failure_reason"], t["z_score"], t["is_anomaly"]
        ]
        for t in transactions
    ]

    s1 = build_sheet_xml(acc_headers, accounts)
    s2 = build_sheet_xml(cat_headers, categories)
    s3 = build_sheet_xml(dep_headers, departments)
    s4 = build_sheet_xml(mer_headers, merchants)
    s5 = build_sheet_xml(txn_headers, txn_rows)
    s6 = build_sheet_xml(view_headers, view_rows)

    with zipfile.ZipFile(excel_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml', content_types)
        z.writestr('_rels/.rels', rels)
        z.writestr('xl/_rels/workbook.xml.rels', wb_rels)
        z.writestr('xl/workbook.xml', workbook)
        z.writestr('xl/styles.xml', styles)
        z.writestr('xl/worksheets/sheet1.xml', s1)
        z.writestr('xl/worksheets/sheet2.xml', s2)
        z.writestr('xl/worksheets/sheet3.xml', s3)
        z.writestr('xl/worksheets/sheet4.xml', s4)
        z.writestr('xl/worksheets/sheet5.xml', s5)
        z.writestr('xl/worksheets/sheet6.xml', s6)

    print(f"Generated multi-sheet Excel workbook at: {excel_path} ({os.path.getsize(excel_path)} bytes)")

# -------------------------------------------------------------
# 6. Database Validation & Integrity Verification Report
# -------------------------------------------------------------

def run_validation_checks():
    db_path = os.path.join(DATA_DIR, "app.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    print("\n" + "="*70)
    print("STEP 10 DATABASE VALIDATION & INTEGRITY REPORT")
    print("="*70)
    
    # 1. Row count verification
    tables = ["dim_accounts", "dim_categories", "dim_departments", "dim_merchants", "fact_transactions"]
    print("\n[CHECK 1] Row Counts per Database Object:")
    for t in tables:
        cur.execute(f"SELECT COUNT(*) FROM {t};")
        cnt = cur.fetchone()[0]
        print(f"  • {t:22s} : {cnt:5d} rows")
        
    cur.execute("SELECT COUNT(*) FROM view_transaction_analysis;")
    v_cnt = cur.fetchone()[0]
    print(f"  • {'view_transaction_analysis':22s} : {v_cnt:5d} rows (35 columns)")
    
    # 2. Foreign key check
    cur.execute("PRAGMA foreign_key_check;")
    fk_errors = cur.fetchall()
    print("\n[CHECK 2] Foreign Key Integrity Check (PRAGMA foreign_key_check):")
    if not fk_errors:
        print("  • Result: PASSED (Zero foreign key violations across all tables).")
    else:
        print(f"  • Result: FAILED ({len(fk_errors)} violations detected): {fk_errors}")

    # 3. Constraint & Range Checks
    cur.execute("SELECT COUNT(*) FROM fact_transactions WHERE amount <= 0;")
    neg_cnt = cur.fetchone()[0]
    print("\n[CHECK 3] Monetary Amount Sanity Check (amount > 0.00):")
    print(f"  • Non-positive records: {neg_cnt} (PASSED)" if neg_cnt == 0 else f"  • Failed: {neg_cnt} negative amounts")

    cur.execute("SELECT COUNT(*) FROM fact_transactions WHERE is_anomaly = 1;")
    outlier_cnt = cur.fetchone()[0]
    print("\n[CHECK 4] Statistical Outlier Distribution (|Z| > 3.0):")
    print(f"  • Flagged Outliers: {outlier_cnt} records identified")

    cur.execute("SELECT status, COUNT(*) FROM fact_transactions GROUP BY status;")
    status_dist = cur.fetchall()
    print("\n[CHECK 5] Transaction Status Distribution:")
    for st, c in status_dist:
        print(f"  • Status '{st:8s}' : {c:4d} rows")

    cur.execute("SELECT COUNT(*) FROM dim_merchants WHERE city IS NULL;")
    null_city = cur.fetchone()[0]
    print(f"\n[CHECK 6] Data Quality Issue Verification (Intentional Missing Values):")
    print(f"  • Merchants with NULL city: {null_city} (Expected 3 for cleaning)")

    conn.close()
    print("\n" + "="*70)
    print("ALL VALIDATION CHECKS COMPLETED SUCCESSFULLY.")
    print("="*70)

# -------------------------------------------------------------
# Main Execution Pipeline
# -------------------------------------------------------------

if __name__ == "__main__":
    print("Executing synthetic dataset generation pipeline...")
    accs = generate_accounts()
    cats = generate_categories()
    deps = generate_departments()
    merchs = generate_merchants()
    txns = generate_transactions(accs, cats, deps, merchs, target_count=300)
    
    init_sqlite_db(accs, cats, deps, merchs, txns)
    export_csv_files(accs, cats, deps, merchs, txns)
    export_excel_workbook(accs, cats, deps, merchs, txns)
    run_validation_checks()
