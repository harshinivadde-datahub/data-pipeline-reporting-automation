"""
validate.py
-----------
Pre-load data quality checks.
Flags rows that fail validation rules and returns a clean subset.
"""

import pandas as pd


def check_nulls(df: pd.DataFrame) -> dict:
    """Return null count per column."""
    null_counts = df.isnull().sum()
    return null_counts[null_counts > 0].to_dict()


def check_negative_values(df: pd.DataFrame, numeric_cols: list) -> pd.DataFrame:
    """Flag rows with unexpected negative values."""
    mask = (df[numeric_cols] < 0).any(axis=1)
    flagged = df[mask]
    if not flagged.empty:
        print(f"[VALIDATE] {len(flagged)} rows with negative values in {numeric_cols}.")
    return flagged


def check_date_range(df: pd.DataFrame, date_col: str,
                     start: str = "2020-01-01", end: str = "2030-12-31") -> pd.DataFrame:
    """Flag rows with dates outside an acceptable range."""
    out_of_range = df[~df[date_col].between(start, end)]
    if not out_of_range.empty:
        print(f"[VALIDATE] {len(out_of_range)} rows with out-of-range dates.")
    return out_of_range


def run_validation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Run all validation checks.
    Returns the DataFrame with invalid rows removed.
    """
    print("\n--- Running Validation ---")
    nulls = check_nulls(df)
    if nulls:
        print(f"[VALIDATE] Remaining nulls detected: {nulls}")
    else:
        print("[VALIDATE] No nulls found.")

    negative_rows = check_negative_values(df, ["revenue", "units_sold"])
    df = df.drop(negative_rows.index)

    if "date" in df.columns:
        bad_dates = check_date_range(df, "date")
        df = df.drop(bad_dates.index)

    print(f"[VALIDATE] Validation complete. {len(df)} rows passed.\n")
    return df
