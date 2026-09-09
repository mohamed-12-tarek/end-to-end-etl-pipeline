from sqlalchemy import text
from config import get_engine
from prefect import task, get_run_logger


@task
def update_dim_product():
    logger = get_run_logger()
    logger.info("Updating dim_product using SCD Type 1...")

    merged_sql = '''
        MERGE dbo.dim_product AS trg
        USING dbo.vw_tr_products AS src
            ON trg.product_id = src.product_id

        WHEN MATCHED THEN
            UPDATE SET
                trg.product_name = src.product_name,
                trg.category_id = src.category_id,
                trg.category_name = src.category_name,
                trg.brand_id = src.brand_id,
                trg.brand_name = src.brand_name,
                trg.model_year = src.model_year,
                trg.list_price = src.list_price

        WHEN NOT MATCHED BY TARGET THEN
            INSERT (
                product_id,
                product_name,
                category_id,
                category_name,
                brand_id,
                brand_name,
                model_year,
                list_price
            )
            VALUES (
                src.product_id,
                src.product_name,
                src.category_id,
                src.category_name,
                src.brand_id,
                src.brand_name,
                src.model_year,
                src.list_price
            );
    '''

    try:
        engine = get_engine()

        with engine.begin() as conn:
            conn.execute(text(merged_sql))

        logger.info("dim_product updated successfully.")
        
    except Exception as e:
        logger.exception(f"Error updating dim_product: {e}")
        raise


@task
def update_dim_store():
    logger = get_run_logger()
    logger.info("Updating dim_store using SCD Type 1...")

    merged_sql = '''
        MERGE dbo.dim_store AS trg
        USING dbo.vw_tr_stores AS src
            ON trg.store_id = src.store_id

        WHEN MATCHED THEN
            UPDATE SET
                trg.store_name = src.store_name,
                trg.street = src.street,
                trg.city = src.city,
                trg.state = src.state,
                trg.zip_code = src.zip_code

        WHEN NOT MATCHED BY TARGET THEN
            INSERT (
                store_id,
                store_name,
                street,
                city,
                state,
                zip_code
            )
            VALUES (
                src.store_id,
                src.store_name,
                src.street,
                src.city,
                src.state,
                src.zip_code
            );
    '''

    try:
        engine = get_engine()

        with engine.begin() as conn:
            conn.execute(text(merged_sql))

        logger.info("dim_store updated successfully.")

    except Exception as e:
        logger.exception(f"Error updating dim_store: {e}")
        raise