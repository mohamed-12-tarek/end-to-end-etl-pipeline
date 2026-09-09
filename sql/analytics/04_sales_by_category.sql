/*
    Which product category generates the most revenue?
    Which category sells the most items?
    How important is each category to total revenue?
*/

IF OBJECT_ID('dbo.vw_analytics_sales_by_category', 'V') IS NOT NULL
    DROP VIEW dbo.vw_analytics_sales_by_category;
GO

CREATE VIEW dbo.vw_analytics_sales_by_category
AS
SELECT
    dp.category_id,
    dp.category_name,

    COUNT(DISTINCT fs.order_id) AS orders_count,
    SUM(fs.quantity) AS items_sold,
    SUM(fs.total_price) AS revenue,
    AVG(fs.discount) AS average_discount

FROM dbo.fact_sales AS fs

INNER JOIN dbo.dim_product AS dp
    ON fs.product_sk = dp.product_sk

GROUP BY
    dp.category_id,
    dp.category_name;
GO