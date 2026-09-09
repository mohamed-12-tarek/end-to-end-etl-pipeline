
-- Which products generate high revenue with relatively low sales volume?

IF OBJECT_ID('dbo.vw_analytics_product_performance', 'V') IS NOT NULL
    DROP VIEW dbo.vw_analytics_product_performance;
GO

CREATE VIEW dbo.vw_analytics_product_performance
AS
SELECT
    dp.product_id,
    dp.product_name,
    dp.category_name,
    dp.brand_name,

    SUM(fs.quantity) AS items_sold,
    SUM(fs.total_price) AS revenue,
    AVG(fs.list_price) AS average_list_price,
    AVG(fs.discount) AS average_discount,
    COUNT(DISTINCT fs.order_id) AS orders_count

FROM dbo.fact_sales AS fs

INNER JOIN dbo.dim_product AS dp
    ON fs.product_sk = dp.product_sk

GROUP BY
    dp.product_id,
    dp.product_name,
    dp.category_name,
    dp.brand_name;
GO