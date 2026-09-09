# End-to-End ETL Pipeline

A batch ETL pipeline for the Bike Stores dataset using Python, Pandas, Prefect, SQLAlchemy, ODBC Driver 18, and SQL Server.

## Architecture

```text
CSV Sources -> Real Staging -> Transformation Views -> Core / OLAP -> fact_sales
```

Core dimensions:
- `dim_customer`: SCD Type 2
- `dim_staff`: SCD Type 2
- `dim_product`: SCD Type 1
- `dim_store`: SCD Type 1
- `dim_date`

`fact_sales` grain is one row per `(order_id, item_id)`.

## SCD Type 2

The source files do not contain a reliable change timestamp. The pipeline therefore uses the load date as the effective date. Initial dimension versions start at `1900-01-01`; changed versions start on the load date and previous versions end the day before.

## Setup

Install Python 3.14, Microsoft ODBC Driver 18 for SQL Server, then:

```bash
pip install -e .
```

Copy `.env.example` to `.env`, set the database variables, and make sure the target SQL Server database exists.

## Test

The database-independent test suite checks source schemas, business-key uniqueness, fact grain, NULL handling, measure ranges, date consistency, referential integrity, and critical SQL/SCD2 rules.

```bash
python -m unittest discover -s tests -v
python -m compileall -q .
```

GitHub Actions runs these checks on pushes and pull requests.

## Run

```bash
python flow.py
```

The flow creates the warehouse/staging objects, creates transformation views, loads all CSV files into real staging, populates the date dimension, applies SCD1/SCD2 dimensions, and rebuilds `fact_sales`.

## Current limitation

This is a batch full-reload design because the sources do not expose CDC or a watermark column. A production incremental version should introduce a source `updated_at`/CDC mechanism and process only changed records.
