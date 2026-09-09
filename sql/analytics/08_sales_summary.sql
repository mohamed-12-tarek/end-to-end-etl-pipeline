
-- Sales Overview

IF OBJECT_ID('dbo.vw_analytics_sales_summary', 'V') IS NOT NULL
    DROP VIEW dbo.vw_analytics_sales_summary;
GO

CREATE VIEW dbo.vw_analytics_sales_summary
AS
SELECT
    COUNT(DISTINCT fs.order_id) AS total_orders,
    SUM(fs.quantity) AS total_items_sold,
    CAST(SUM(fs.total_price) AS DECIMAL(18, 2)) AS total_revenue,
    CAST(SUM(fs.total_price) / NULLIF(COUNT(DISTINCT fs.order_id), 0) AS DECIMAL(18, 2)) AS average_order_value,
    CAST(AVG(fs.discount) AS DECIMAL(18, 4)) AS average_discount

FROM dbo.fact_sales AS fs;
GO