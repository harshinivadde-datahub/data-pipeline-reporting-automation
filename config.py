"""
load.py
-------
Loads the cleaned and transformed DataFrame into MySQL.
Supports append and replace modes with run logging.
"""

import pandas as pd
import sqlalchemy
from datetime import datetime
import config


def get_engine():
    return sqlalchemy.create_engine(
        f"mysql+pymysql://{config.DB_USER}:{config.DB_PASSWORD}"
        f"@{config.DB_HOST}/{config.DB_NAME}"
    )


def load_to_mysql(df: pd.DataFrame, table_name: str, mode: str = "append"):
    """
    Load DataFrame to a MySQL table.
    mode: 'append' to add rows, 'replace' to overwrite table.
    """
    engine = get_engine()
    print(f"[LOAD] Writing {len(df)} rows to table '{table_name}' (mode={mode})...")
    df.to_sql(table_name, con=engine, if_exists=mode, index=False)
    print(f"[LOAD] Successfully loaded '{table_name}'.")


def log_pipeline_run(source: str, rows_loaded: int, status: str = "SUCCESS"):
    """Write a pipeline run record to reporting_log table."""
    engine = get_engine()
    log_entry = pd.DataFrame([{
        "run_timestamp": datetime.now(),
        "source_file": source,
        "rows_loaded": rows_loaded,
        "status": status
    }])
    log_entry.to_sql("reporting_log", con=engine, if_exists="append", index=False)
    print(f"[LOAD] Pipeline run logged: {status}, {rows_loaded} rows from '{source}'.")
