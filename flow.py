import re
from pathlib import Path
import pandas as pd
from prefect import flow, get_run_logger, task
from sqlalchemy import text
from config import get_engine
from tasks.fact_table import reload_fact_table
from tasks.scd_type1 import update_dim_product, update_dim_store
from tasks.scd_type2 import update_dim_customer, update_dim_staff


STAGING_TABLES = {
    "customers.csv": "stg_customers",
    "products.csv": "stg_products",
    "brands.csv": "stg_brands",
    "categories.csv": "stg_categories",
    "orders.csv": "stg_orders",
    "order_items.csv": "stg_order_items",
    "staffs.csv": "stg_staffs",
    "stores.csv": "stg_stores",
}


@task(retries=2, retry_delay_seconds=30)
def run_sql_script(file_path: str | Path):
    logger = get_run_logger()
    logger.info("Running SQL script: %s", file_path)
    engine = get_engine()

    try:
        sql = Path(file_path).read_text(encoding="utf-8")
        batches = re.split(r"(?im)^\s*GO\s*$", sql)

        with engine.begin() as conn:
            for batch in batches:
                if batch.strip():
                    conn.execute(text(batch))

        logger.info("SQL script executed successfully: %s", file_path)
    except Exception:
        logger.exception("Failed to execute SQL script: %s", file_path)
        raise


@task(retries=2, retry_delay_seconds=30)
def load_csv_to_staging(table_name: str, csv_path: str | Path):
    logger = get_run_logger()
    logger.info("Loading %s into %s", csv_path, table_name)

    csv_path = Path(csv_path)
    if not csv_path.is_file():
        raise FileNotFoundError(f"Source file not found: {csv_path}")

    engine = get_engine()

    try:
        df = pd.read_csv(csv_path, na_values=["NULL", "null", "Null"])
        if df.empty:
            raise ValueError(f"Source file is empty: {csv_path}")

        with engine.begin() as conn:
            logger.info("Truncating staging table: %s", table_name)
            conn.execute(text(f"TRUNCATE TABLE dbo.{table_name}"))
            df.to_sql(
                table_name,
                con=conn,
                schema="dbo",
                index=False,
                if_exists="append",
                chunksize=5000,
            )

        logger.info("%s rows loaded into %s", len(df), table_name)
    except Exception:
        logger.exception("Error loading %s into %s", csv_path, table_name)
        raise


@flow(name="End-to-End ETL Pipeline")
def etl_flow():
    base_dir = Path(__file__).resolve().parent
    data_dir = base_dir / "data"
    sql_dir = base_dir / "sql"

    run_sql_script(sql_dir / "create_olap_schema.sql")
    run_sql_script(sql_dir / "stage_tables.sql")
    run_sql_script(sql_dir / "transformation_views.sql")

    for filename, table_name in STAGING_TABLES.items():
        load_csv_to_staging(table_name, data_dir / filename)

    run_sql_script(sql_dir / "dim_date.sql")

    update_dim_customer()
    update_dim_staff()
    update_dim_product()
    update_dim_store()
    reload_fact_table()


if __name__ == "__main__":
    etl_flow()
