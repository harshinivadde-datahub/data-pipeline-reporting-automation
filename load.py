"""
extract.py
----------
Extracts raw data from CSV files or a MySQL source database.
Supports multi-source ingestion with basic schema logging.
"""

import pandas as pd
import sqlalchemy
import config


def extract_from_csv(filepath: str) -> pd.DataFrame:
    """Load raw data from a CSV file."""
    print(f"[EXTRACT] Reading CSV: {filepath}")
    df = pd.read_csv(filepath)
    print(f"[EXTRACT] Loaded {len(df)} rows, {len(df.columns)} columns.")
    return df


def extract_from_db(query: str) -> pd.DataFrame:
    """Load data from MySQL using a SQL query."""
    print("[EXTRACT] Connecting to source database...")
    engine = sqlalchemy.create_engine(
        f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}"
        f"@{config.DB_HOST}/{config.DB_NAME}"
    )
    df = pd.read_sql(query, con=engine)
    print(f"[EXTRACT] Loaded {len(df)} rows from DB.")
    return df


def extract_multiple_sources(sources: list) -> pd.DataFrame:
    """
    Ingest from multiple CSV sources and concatenate into one DataFrame.
    Adds a 'source_file' column to track origin.
    """
    frames = []
    for path in sources:
        df = extract_from_csv(path)
        df["source_file"] = path
        frames.append(df)
    combined = pd.concat(frames, ignore_index=True)
    print(f"[EXTRACT] Combined {len(frames)} sources → {len(combined)} total rows.")
    return combined
