/*
    Who are our top-performing staff members?
    Who handles the most orders?
    Who generates the highest revenue?
*/
IF OBJECT_ID('dbo.vw_analytics_sales_by_staff', 'V') IS NOT NULL
    DROP VIEW dbo.vw_analytics_sales_by_staff;
GO

CREATE VIEW dbo.vw_analytics_sales_by_staff
AS
SELECT
    ds.staff_id,
    ds.full_name AS staff_name,

    COUNT(DISTINCT fs.order_id) AS orders_count,
    SUM(fs.quantity) AS items_sold,
    SUM(fs.total_price) AS revenue,
    CAST(SUM(fs.total_price) / NULLIF(COUNT(DISTINCT fs.order_id), 0) AS DECIMAL(18, 2)) AS average_order_value

FROM dbo.fact_sales AS fs

INNER JOIN dbo.dim_staff AS ds
    ON fs.staff_sk = ds.staff_sk

GROUP BY
    ds.staff_id,
    ds.full_name;
GO