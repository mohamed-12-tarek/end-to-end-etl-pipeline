from prefect import get_run_logger, task
from sqlalchemy import text

from config import get_engine


@task
def reload_fact_table():
    logger = get_run_logger()
    logger.info("Reloading fact_sales...")

    sql = """
        INSERT INTO dbo.fact_sales
        (
            order_id, item_id, customer_sk, product_sk, staff_sk,
            store_sk, order_date_sk, quantity, list_price, discount,
            total_price
        )
        SELECT
            oi.order_id,
            oi.item_id,
            dc.customer_sk,
            dp.product_sk,
            dsf.staff_sk,
            dst.store_sk,
            dd.date_sk,
            oi.quantity,
            oi.list_price,
            oi.discount,
            CAST(oi.quantity * oi.list_price * (1 - oi.discount) AS DECIMAL(10,2))
        FROM dbo.vw_tr_order_items AS oi
        
        INNER JOIN dbo.vw_tr_orders AS o
            ON oi.order_id = o.order_id
            
        LEFT JOIN dbo.dim_customer AS dc
            ON o.customer_id = dc.customer_id
           AND o.order_date >= dc.start_date
           AND (dc.end_date IS NULL OR o.order_date <= dc.end_date)
           
        LEFT JOIN dbo.dim_product AS dp
            ON oi.product_id = dp.product_id
            
        LEFT JOIN dbo.dim_staff AS dsf
            ON o.staff_id = dsf.staff_id
           AND o.order_date >= dsf.start_date
           AND (dsf.end_date IS NULL OR o.order_date <= dsf.end_date)
           
        LEFT JOIN dbo.dim_store AS dst
            ON o.store_id = dst.store_id
            
        LEFT JOIN dbo.dim_date AS dd
            ON o.order_date = dd.full_date;
    """

    try:
        engine = get_engine()
        with engine.begin() as conn:
            logger.info("Truncating fact_sales...")
            conn.execute(text("TRUNCATE TABLE dbo.fact_sales"))
            logger.info("Inserting fact_sales...")
            result = conn.execute(text(sql))

        logger.info("fact_sales reloaded successfully: %s rows", result.rowcount)
    except Exception:
        logger.exception("Error reloading fact_sales")
        raise
