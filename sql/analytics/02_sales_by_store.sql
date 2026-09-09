/*
    Which store generates the highest revenue?
    Which store has the highest number of orders?
    Which store has the highest average order value?
*/

IF OBJECT_ID('dbo.vw_analytics_sales_by_store', 'V') IS NOT NULL
    DROP VIEW dbo.vw_analytics_sales_by_store;
GO

CREATE VIEW dbo.vw_analytics_sales_by_store
AS
SELECT
    ds.store_id,
    ds.store_name,
    ds.city,
    ds.state,

    COUNT(DISTINCT fs.order_id) AS orders_count,
    SUM(fs.quantity) AS items_sold,
    SUM(fs.total_price) AS revenue,
    CAST(SUM(fs.total_price) / NULLIF(COUNT(DISTINCT fs.order_id), 0) AS DECIMAL(18, 2)) AS average_order_value

FROM dbo.fact_sales AS fs

INNER JOIN dbo.dim_store AS ds
    ON fs.store_sk = ds.store_sk

GROUP BY
    ds.store_id,
    ds.store_name,
    ds.city,
    ds.state;
GO