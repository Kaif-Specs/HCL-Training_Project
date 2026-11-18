"""
src/cleaner.py
Data sanitization, deduplication, and categorical imputation pipeline.
Produces a sanitized dataset and an audit trail for data quality governance.
"""

import pandas as pd
from typing import Tuple, Dict, Any

def clean_transaction_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Cleans raw transaction DataFrame:
    1. Detects and eliminates duplicate transaction rows based on key financial attributes.
    2. Imputes missing categorical values in payment_method.
    3. Normalizes text fields (strips whitespace, standardizes casing).
    4. Computes data health score and returns audit metrics.
    """
    raw_count = len(df)
    clean_df = df.copy()

    # 1. Detect duplicates based on compound business key
    dedup_subset = ["account_id", "transaction_date", "amount", "transaction_type", "merchant_id"]
    existing_subset = [c for c in dedup_subset if c in clean_df.columns]
    
    duplicate_mask = clean_df.duplicated(subset=existing_subset, keep="first")
    duplicate_rows = clean_df[duplicate_mask]
    dropped_duplicates_count = len(duplicate_rows)
    dropped_ids = duplicate_rows["transaction_id"].tolist() if "transaction_id" in duplicate_rows.columns else []

    clean_df = clean_df.drop_duplicates(subset=existing_subset, keep="first").reset_index(drop=True)

    # 2. Impute missing categorical values
    imputed_nulls_count = 0
    if "payment_method" in clean_df.columns:
        null_mask = clean_df["payment_method"].isna() | (clean_df["payment_method"].str.strip() == "")
        imputed_nulls_count = int(null_mask.sum())
        clean_df["payment_method"] = clean_df["payment_method"].fillna("Unknown/Pending")
        clean_df.loc[clean_df["payment_method"].str.strip() == "", "payment_method"] = "Unknown/Pending"

    # 3. String normalization
    text_cols = ["merchant_name", "category_name", "department_name", "account_name"]
    for col in text_cols:
        if col in clean_df.columns and clean_df[col].dtype == "object":
            clean_df[col] = clean_df[col].astype(str).str.strip()

    # 4. Compute Health Score
    total_issues = dropped_duplicates_count + imputed_nulls_count
    total_cells = raw_count * len(df.columns)
    health_score = round(max(0.0, 100.0 - ((total_issues / raw_count) * 100.0)), 2)

    audit_log = {
        "raw_records": raw_count,
        "clean_records": len(clean_df),
        "duplicates_removed": dropped_duplicates_count,
        "duplicate_ids": dropped_ids,
        "nulls_imputed": imputed_nulls_count,
        "health_score": health_score
    }

    return clean_df, audit_log
