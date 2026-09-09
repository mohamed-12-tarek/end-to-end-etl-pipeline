/*
    What is our revenue over time?
    How many orders do we receive?
    How many items do we sell?
    What is our average order value?
    How much discount are we giving?
*/

IF OBJECT_ID('dbo.vw_analytics_sales_overview', 'V') IS NOT NULL
    DROP VIEW dbo.vw_analytics_sales_overview;
GO

CREATE VIEW dbo.vw_analytics_sales_overview
AS
SELECT
    dd.full_date,
    dd.year,
    dd.month,
    dd.month_name,

    COUNT(DISTINCT fs.order_id) AS orders_count,
    SUM(fs.quantity) AS items_sold,
    SUM(fs.total_price) AS revenue,
    SUM(fs.quantity * fs.list_price * fs.discount) AS discount_amount,
    AVG(fs.discount) AS avg_discount,
    CAST(SUM(fs.total_price) / NULLIF(COUNT(DISTINCT fs.order_id), 0) AS DECIMAL(18, 2)) AS average_order_value

FROM dbo.fact_sales AS fs

INNER JOIN dbo.dim_date AS dd
    ON fs.order_date_sk = dd.date_sk

GROUP BY
    dd.full_date,
    dd.year,
    dd.month,
    dd.month_name;
GO