from prefect import get_run_logger, task
from sqlalchemy import text

from config import get_engine


SCD2_START_DATE = "1900-01-01"


@task
def update_dim_customer():
    logger = get_run_logger()
    logger.info("Updating dim_customer (SCD Type 2)...")

    sql = f"""
        UPDATE d
        SET
            d.end_date = DATEADD(DAY, -1, CAST(GETDATE() AS DATE)),
            d.current_flag = 'N'
        FROM dbo.dim_customer AS d
        
        INNER JOIN dbo.vw_tr_customers AS s
            ON s.customer_id = d.customer_id
        WHERE d.current_flag = 'Y'
          AND (
                ISNULL(s.full_name, '') <> ISNULL(d.full_name, '')
                OR ISNULL(s.email, '') <> ISNULL(d.email, '')
                OR ISNULL(s.phone, '') <> ISNULL(d.phone, '')
                OR ISNULL(s.city, '') <> ISNULL(d.city, '')
                OR ISNULL(s.state, '') <> ISNULL(d.state, '')
                OR ISNULL(s.zip_code, '') <> ISNULL(d.zip_code, '')
          );

        INSERT INTO dbo.dim_customer (
            customer_id, full_name, email, phone, city, state, zip_code,
            start_date, end_date, current_flag
        )
        SELECT
            s.customer_id, s.full_name, s.email, s.phone, s.city, s.state,
            s.zip_code,
            CASE WHEN d.customer_id IS NULL
                 THEN CAST('{SCD2_START_DATE}' AS DATE)
                 ELSE CAST(GETDATE() AS DATE)
            END,
            NULL,
            'Y'
        FROM dbo.vw_tr_customers AS s
        
        LEFT JOIN dbo.dim_customer AS d
            ON s.customer_id = d.customer_id
           AND d.current_flag = 'Y'
           
        WHERE d.customer_id IS NULL
           OR (
                ISNULL(s.full_name, '') <> ISNULL(d.full_name, '')
                OR ISNULL(s.email, '') <> ISNULL(d.email, '')
                OR ISNULL(s.phone, '') <> ISNULL(d.phone, '')
                OR ISNULL(s.city, '') <> ISNULL(d.city, '')
                OR ISNULL(s.state, '') <> ISNULL(d.state, '')
                OR ISNULL(s.zip_code, '') <> ISNULL(d.zip_code, '')
           );
    """

    _execute_scd2("dim_customer", sql, logger)


@task
def update_dim_staff():
    logger = get_run_logger()
    logger.info("Updating dim_staff (SCD Type 2)...")

    sql = f"""
        UPDATE d
        SET
            d.end_date = DATEADD(DAY, -1, CAST(GETDATE() AS DATE)),
            d.current_flag = 'N'
        FROM dbo.dim_staff AS d
        
        INNER JOIN dbo.vw_tr_staffs AS s
            ON s.staff_id = d.staff_id
            
        WHERE d.current_flag = 'Y'
          AND (
                ISNULL(s.full_name, '') <> ISNULL(d.full_name, '')
                OR ISNULL(s.email, '') <> ISNULL(d.email, '')
                OR ISNULL(s.phone, '') <> ISNULL(d.phone, '')
                OR ISNULL(s.store_id, -1) <> ISNULL(d.store_id, -1)
                OR ISNULL(s.manager_id, -1) <> ISNULL(d.manager_id, -1)
          );

        INSERT INTO dbo.dim_staff (
            staff_id, full_name, email, phone, store_id, manager_id,
            start_date, end_date, current_flag
        )
        SELECT
            s.staff_id, s.full_name, s.email, s.phone, s.store_id, s.manager_id,
            CASE WHEN d.staff_id IS NULL
                 THEN CAST('{SCD2_START_DATE}' AS DATE)
                 ELSE CAST(GETDATE() AS DATE)
            END,
            NULL,
            'Y'
        FROM dbo.vw_tr_staffs AS s
        
        LEFT JOIN dbo.dim_staff AS d
            ON s.staff_id = d.staff_id
           AND d.current_flag = 'Y'
           
        WHERE d.staff_id IS NULL
           OR (
                ISNULL(s.full_name, '') <> ISNULL(d.full_name, '')
                OR ISNULL(s.email, '') <> ISNULL(d.email, '')
                OR ISNULL(s.phone, '') <> ISNULL(d.phone, '')
                OR ISNULL(s.store_id, -1) <> ISNULL(d.store_id, -1)
                OR ISNULL(s.manager_id, -1) <> ISNULL(d.manager_id, -1)
           );
    """

    _execute_scd2("dim_staff", sql, logger)


def _execute_scd2(table_name: str, sql: str, logger) -> None:
    try:
        engine = get_engine()
        with engine.begin() as conn:
            conn.execute(text(sql))
        logger.info("%s updated successfully.", table_name)
    except Exception:
        logger.exception("Error updating %s", table_name)
        raise
