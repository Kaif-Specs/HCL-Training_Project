import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

def generate_synthetic_data(num_rows=650, seed=42):
    np.random.seed(seed)
    random.seed(seed)

    departments = {
        'Engineering': {'head': 'Rajesh Sharma', 'budget': 3500000.0},
        'IT Infrastructure': {'head': 'Priya Nair', 'budget': 2800000.0},
        'Sales & Marketing': {'head': 'Amit Verma', 'budget': 2200000.0},
        'Finance & Accounting': {'head': 'Sunita Rao', 'budget': 1500000.0},
        'Human Resources': {'head': 'Vikram Malhotra', 'budget': 1200000.0}
    }

    dept_list = list(departments.keys())

    dept_categories = {
        'Engineering': ['Cloud Infrastructure', 'SaaS Subscriptions', 'Hardware Equipment'],
        'IT Infrastructure': ['Cloud Infrastructure', 'Office Equipment', 'SaaS Subscriptions'],
        'Sales & Marketing': ['Marketing & Ads', 'Travel & Entertainment', 'SaaS Subscriptions'],
        'Finance & Accounting': ['Professional Services', 'Office Equipment', 'Payroll & Benefits'],
        'Human Resources': ['Payroll & Benefits', 'Office Equipment', 'Travel & Entertainment']
    }

    vendors = {
        'Cloud Infrastructure': [('AWS Cloud', 'Tier-1 Strategic'), ('Google Cloud', 'Tier-1 Strategic'), ('Microsoft Azure', 'Tier-1 Strategic')],
        'Payroll & Benefits': [('ADP Payroll Systems', 'Tier-1 Strategic'), ('RazorpayX Payroll', 'Tier-1 Strategic')],
        'SaaS Subscriptions': [('Salesforce CRM', 'Tier-2 Preferred'), ('Slack Tech', 'Tier-2 Preferred'), ('Zoom Video', 'Tier-3 Standard'), ('Atlassian Jira', 'Tier-2 Preferred')],
        'Office Equipment': [('Dell Technologies', 'Tier-2 Preferred'), ('Staples Business', 'Tier-3 Standard'), ('Croma Enterprise', 'Tier-3 Standard')],
        'Travel & Entertainment': [('Uber for Business', 'Tier-3 Standard'), ('MakeMyTrip Corp', 'Tier-2 Preferred'), ('Taj Hotels', 'Tier-2 Preferred')],
        'Professional Services': [('Deloitte Consulting', 'Tier-1 Strategic'), ('Ernst & Young LLP', 'Tier-1 Strategic'), ('Khaitan Legal', 'Tier-2 Preferred')],
        'Marketing & Ads': [('Google Ads Engine', 'Tier-1 Strategic'), ('LinkedIn Ads Corp', 'Tier-2 Preferred'), ('Meta Business', 'Tier-2 Preferred')],
        'Hardware Equipment': [('Apple Business Direct', 'Tier-1 Strategic'), ('Lenovo Enterprise', 'Tier-2 Preferred'), ('HP Commercial', 'Tier-3 Standard')]
    }

    banks = ['HDFC Bank', 'ICICI Bank', 'Axis Bank', 'State Bank of India']
    accounts = [
        ('ACC-HDFC-01', 'Current Account', 'HDFC Bank', 0.0),
        ('ACC-ICICI-02', 'Corporate Credit Card', 'ICICI Bank', 1500000.0),
        ('ACC-AXIS-03', 'Current Account', 'Axis Bank', 0.0),
        ('ACC-SBI-04', 'Corporate Credit Card', 'State Bank of India', 1000000.0),
        ('ACC-HDFC-05', 'Corporate Credit Card', 'HDFC Bank', 2000000.0)
    ]

    channels = ['Online Portal', 'Automated Standing Instruction', 'NEFT/RTGS', 'Corporate Card POS', 'UPI']

    base_date = datetime(2025, 1, 1)
    rows = []

    for i in range(1, num_rows + 1):
        txn_id = f"TXN-2025-{i:05d}"
        days_offset = random.randint(0, 364)
        txn_date = base_date + timedelta(days=days_offset)
        
        # Mix date strings
        date_format_choice = random.random()
        if date_format_choice < 0.75:
            date_str = txn_date.strftime('%Y-%m-%d')
        elif date_format_choice < 0.90:
            date_str = txn_date.strftime('%d/%m/%Y')
        else:
            date_str = txn_date.strftime('%Y/%m/%d')
            
        time_str = f"{random.randint(8, 21):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}"

        dept = random.choice(dept_list)
        budget = departments[dept]['budget']
        
        category = random.choice(dept_categories[dept])
        vendor_choice, tier = random.choice(vendors[category])

        # Transaction type: 82% Debit, 18% Credit
        is_debit = random.random() < 0.82
        txn_type = 'Debit' if is_debit else 'Credit'

        if txn_type == 'Credit':
            acc = random.choice([a for a in accounts if a[1] == 'Current Account'])
            amount = round(np.random.gamma(shape=3.0, scale=35000.0), 2)
        else:
            acc = random.choice(accounts)
            if category == 'Payroll & Benefits':
                amount = round(np.random.normal(loc=280000.0, scale=35000.0), 2)
            elif category == 'Cloud Infrastructure':
                amount = round(np.random.gamma(shape=2.5, scale=25000.0), 2)
            elif category == 'Marketing & Ads':
                amount = round(np.random.gamma(shape=2.2, scale=30000.0), 2)
            elif category == 'Professional Services':
                amount = round(np.random.normal(loc=120000.0, scale=25000.0), 2)
            else:
                amount = round(np.random.exponential(scale=18000.0) + 1500.0, 2)

        acc_id, acc_type, bank, limit = acc

        # Channel
        if acc_type == 'Corporate Credit Card':
            channel = random.choice(['Online Portal', 'Corporate Card POS'])
        else:
            channel = random.choice(['NEFT/RTGS', 'Automated Standing Instruction', 'UPI', 'Online Portal'])

        # Fee
        if channel == 'NEFT/RTGS':
            fee = round(random.choice([0.0, 15.0, 25.0]), 2)
        elif acc_type == 'Corporate Credit Card':
            fee = round(amount * random.uniform(0.012, 0.018), 2)
        else:
            fee = 0.0

        # Status
        status_rand = random.random()
        if status_rand < 0.88:
            status = 'Completed'
            fail_reason = None
        elif status_rand < 0.94:
            status = 'Pending'
            fail_reason = None
        elif status_rand < 0.98:
            status = 'Failed'
            fail_reason = random.choice(['Insufficient Funds', 'Credit Limit Exceeded', 'Gateway Timeout', 'Card Verification Failed'])
        else:
            status = 'Reversed'
            fail_reason = 'Disputed by Merchant'

        rating = random.choices([1, 2, 3, 4, 5], weights=[0.05, 0.10, 0.25, 0.40, 0.20])[0]

        rows.append({
            'transaction_id': txn_id,
            'transaction_date': date_str,
            'transaction_time': time_str,
            'account_type': acc_type,
            'bank_name': bank,
            'department_name': dept,
            'category_name': category,
            'vendor_name': vendor_choice,
            'vendor_tier': tier,
            'transaction_type': txn_type,
            'payment_channel': channel,
            'amount': amount,
            'fee_amount': fee,
            'monthly_budget': budget,
            'credit_limit': limit,
            'status': status,
            'failure_reason': fail_reason,
            'approval_rating': rating,
            'is_anomaly_flag': 0
        })

    df = pd.DataFrame(rows)

    # 1. Inject Extreme IQR Outliers in amount
    outlier_indices = [15, 88, 142, 230, 310, 425, 512, 601]
    outlier_values = [985000.0, 1250000.0, 890000.0, 1450000.0, 920000.0, 1100000.0, 850000.0, 1380000.0]
    for idx, val in zip(outlier_indices, outlier_values):
        df.at[idx, 'amount'] = val
        df.at[idx, 'is_anomaly_flag'] = 1

    # 2. Inject Dirty string formatting in amount
    df.at[34, 'amount'] = "₹ 45,200.00"
    df.at[99, 'amount'] = "₹ 18,500.50"
    df.at[175, 'amount'] = "₹ 125,000.00"
    df.at[280, 'amount'] = "$ 12,000.00"
    df.at[350, 'amount'] = "₹ 82,400.00"

    # 3. Inject Miskeyed negative amounts
    df.at[62, 'amount'] = -8500.0
    df.at[215, 'amount'] = -14200.0
    df.at[440, 'amount'] = -3100.0

    # 4. Inject Inconsistent Categorical Labels (Bad Labels)
    df.at[22, 'department_name'] = 'engineering'
    df.at[85, 'department_name'] = 'ENGINEERING'
    df.at[150, 'department_name'] = 'it infrastructure'
    df.at[320, 'department_name'] = 'HR & Ops'
    df.at[410, 'department_name'] = 'Sales & Marketing '
    df.at[52, 'category_name'] = 'cloud infra'
    df.at[190, 'category_name'] = 'Cloud Infrastructure '
    df.at[360, 'category_name'] = 'saas subscriptions'

    # 5. Inject Missing Values (Nulls)
    null_fee_indices = np.random.choice(range(len(df)), size=28, replace=False)
    for idx in null_fee_indices:
        df.at[idx, 'fee_amount'] = np.nan

    null_rating_indices = np.random.choice(range(len(df)), size=36, replace=False)
    for idx in null_rating_indices:
        df.at[idx, 'approval_rating'] = np.nan

    # 6. Inject Exact Duplicate Rows (6 duplicate records appended)
    dup_rows = df.iloc[[10, 45, 120, 250, 380, 500]].copy()
    df = pd.concat([df, dup_rows], ignore_index=True)

    return df

if __name__ == '__main__':
    df = generate_synthetic_data(num_rows=650, seed=42)
    output_path = 'data/enterprise_transactions_eda.csv'
    df.to_csv(output_path, index=False)
    print(f"Generated synthetic dataset saved to {output_path}")
    print(f"Dataset Shape: {df.shape}")
    print(f"Duplicates: {df.duplicated().sum()}")
    print("Columns:", df.columns.tolist())
    print("Null counts:\n", df.isnull().sum()[df.isnull().sum() > 0])
