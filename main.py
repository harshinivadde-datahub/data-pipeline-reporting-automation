"""
transform.py
------------
Cleans and transforms raw ingested data using Pandas.
Handles missing values, duplicates, schema inconsistencies,
and type normalization before loading into MySQL.
"""

import pandas as pd


REQUIRED_COLUMNS = ["transaction_id", "region", "department", "revenue",
                    "units_sold", "date", "category"]

COLUMN_RENAME_MAP = {
    "txn_id": "transaction_id",
    "dept": "department",
    "reg": "region",
    "rev": "revenue",
    "qty": "units_sold",
    "dt": "date",
    "cat": "category",
}


def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize column names across sources."""
    df = df.rename(columns=COLUMN_RENAME_MAP)
    print(f"[TRANSFORM] Columns after rename: {list(df.columns)}")
    return df


def drop_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Remove exact duplicate rows."""
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"[TRANSFORM] Dropped {before - after} duplicate rows.")
    return df


def handle_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Drop rows missing critical identifiers.
    - Fill numeric nulls with column median.
    - Fill categorical nulls with 'Unknown'.
    """
    df = df.dropna(subset=["transaction_id"])
    numeric_cols = df.select_dtypes(include="number").columns
    for col in numeric_cols:
        median_val = df[col].median()
        null_count = df[col].isna().sum()
        df[col] = df[col].fillna(median_val)
        if null_count > 0:
            print(f"[TRANSFORM] Filled {null_count} nulls in '{col}' with median {median_val:.2f}")

    categorical_cols = df.select_dtypes(include="object").columns
    for col in categorical_cols:
        null_count = df[col].isna().sum()
        df[col] = df[col].fillna("Unknown")
        if null_count > 0:
            print(f"[TRANSFORM] Filled {null_count} nulls in '{col}' with 'Unknown'")
    return df


def normalize_types(df: pd.DataFrame) -> pd.DataFrame:
    """Cast columns to correct data types."""
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["units_sold"] = pd.to_numeric(df["units_sold"], errors="coerce").astype("Int64")
    df["region"] = df["region"].str.strip().str.title()
    df["department"] = df["department"].str.strip().str.title()
    df["category"] = df["category"].str.strip().str.lower()
    print("[TRANSFORM] Data types normalized.")
    return df


def add_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add KPI-supporting calculated fields."""
    df["revenue_per_unit"] = (df["revenue"] / df["units_sold"]).round(2)
    df["year_month"] = df["date"].dt.to_period("M").astype(str)
    print("[TRANSFORM] Derived columns added: revenue_per_unit, year_month")
    return df


def validate_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Warn if any expected columns are missing."""
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        print(f"[TRANSFORM] WARNING: Missing expected columns: {missing}")
    else:
        print("[TRANSFORM] Schema validation passed.")
    return df


def run_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Run the full transformation pipeline."""
    print("\n--- Starting Transformation ---")
    df = rename_columns(df)
    df = drop_duplicates(df)
    df = handle_missing_values(df)
    df = normalize_types(df)
    df = add_derived_columns(df)
    df = validate_schema(df)
    print(f"--- Transformation Complete: {len(df)} clean rows ---\n")
    return df
