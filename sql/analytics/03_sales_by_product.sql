/*
    What are the top-selling products?
    What products generate the highest revenue?
    Which products have high revenue but low volume?
*/

IF OBJECT_ID('dbo.vw_analytics_sales_by_product', 'V') IS NOT NULL
    DROP VIEW dbo.vw_analytics_sales_by_product;
GO

CREATE VIEW dbo.vw_analytics_sales_by_product
AS
SELECT
    dp.product_id,
    dp.product_name,
    dp.category_id,
    dp.category_name,
    dp.brand_id,
    dp.brand_name,
    dp.model_year,
    dp.list_price,

    COUNT(DISTINCT fs.order_id) AS orders_count,
    SUM(fs.quantity) AS items_sold,
    SUM(fs.total_price) AS revenue,
    AVG(fs.discount) AS average_discount

FROM dbo.fact_sales AS fs

INNER JOIN dbo.dim_product AS dp
    ON fs.product_sk = dp.product_sk

GROUP BY
    dp.product_id,
    dp.product_name,
    dp.category_id,
    dp.category_name,
    dp.brand_id,
    dp.brand_name,
    dp.model_year,
    dp.list_price;
GO