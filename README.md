# Unified Data Pipeline & Reporting Automation System

## Overview
A Python-based ETL pipeline that ingests, cleans, and transforms multi-source datasets for structured KPI reporting. Cleaned data is loaded into MySQL for downstream SQL-based KPI standardization and automated recurring reporting.

## Tech Stack
- **Python 3.10+** — Pandas, SQLAlchemy, PyMySQL
- **MySQL** — structured storage and KPI transformation logic
- **SQL** — aggregation, standardization, and reporting queries

## Key Features
- Handles missing values, duplicate records, and schema inconsistencies across sources
- Automates recurring KPI reporting workflows end-to-end
- SQL-based KPI definitions ensure consistent metric standardization
- Validation layer flags data quality issues before loading

## Project Structure
```
data-pipeline-reporting-automation/
├── etl/
│   ├── extract.py          # Load raw data from CSV / DB sources
│   ├── transform.py        # Pandas cleaning & transformation logic
│   ├── load.py             # Load structured data into MySQL
│   └── validate.py         # Pre-load data quality checks
├── sql/
│   └── kpi_definitions.sql # KPI standardization & reporting queries
├── data/
│   └── sample_data.csv     # Sample multi-source dataset
├── config.py               # DB connection settings
├── main.py                 # Pipeline entry point
├── requirements.txt
└── README.md
```

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure your database
Edit `config.py` with your MySQL credentials:
```python
DB_HOST = "localhost"
DB_USER = "your_user"
DB_PASSWORD = "your_password"
DB_NAME = "kpi_reporting"
```

### 3. Run the pipeline
```bash
python main.py
```

### 4. Run SQL KPI reports
Open `sql/kpi_definitions.sql` in MySQL Workbench or run via CLI:
```bash
mysql -u your_user -p kpi_reporting < sql/kpi_definitions.sql
```

## Sample Output
After running the pipeline, the following tables are populated in MySQL:
- `cleaned_data` — transformed and validated records
- `kpi_summary` — aggregated KPI metrics by region/department/period
- `reporting_log` — pipeline run history and row counts

## Skills Demonstrated
- ETL pipeline design (Extract → Transform → Load)
- Data cleaning with Pandas (null handling, deduplication, type normalization)
- SQL-based KPI standardization and reporting automation
- Modular Python architecture for reusable pipeline components
