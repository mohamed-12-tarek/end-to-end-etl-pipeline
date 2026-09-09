
-- How is our business performing month over month?

IF OBJECT_ID('dbo.vw_analytics_sales_monthly', 'V') IS NOT NULL
    DROP VIEW dbo.vw_analytics_sales_monthly;
GO

CREATE VIEW dbo.vw_analytics_sales_monthly
AS
SELECT
    dd.year,
    dd.month,
    dd.month_name,

    COUNT(DISTINCT fs.order_id) AS orders_count,
    SUM(fs.quantity) AS items_sold,
    SUM(fs.total_price) AS revenue

FROM dbo.fact_sales AS fs

INNER JOIN dbo.dim_date AS dd
    ON fs.order_date_sk = dd.date_sk

GROUP BY
    dd.year,
    dd.month,
    dd.month_name;
GO