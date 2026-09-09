QUESTIONS = {
    "Sales": {
        "Revenue Over Time": {"question": "What is our sales revenue over time?", "view": "dbo.vw_analytics_sales_overview", "chart": "revenue_over_time"},
        "Orders Over Time": {"question": "How many orders are placed over time?", "view": "dbo.vw_analytics_sales_overview", "chart": "orders_over_time"},
        "Average Order Value": {"question": "How does the average order value change over time?", "view": "dbo.vw_analytics_sales_overview", "chart": "aov_over_time"},
        "Monthly Sales Trend": {"question": "How is the business performing month over month?", "view": "dbo.vw_analytics_sales_monthly", "chart": "monthly_revenue"},
    },
    "Products": {
        "Top Products by Revenue": {"question": "Which products generate the highest revenue?", "view": "dbo.vw_analytics_sales_by_product", "chart": "top_products_revenue"},
        "Top Products by Quantity": {"question": "Which products sell the most units?", "view": "dbo.vw_analytics_sales_by_product", "chart": "top_products_quantity"},
        "Product Performance": {"question": "Which products generate high revenue with low sales volume?", "view": "dbo.vw_analytics_product_performance", "chart": "product_performance"},
    },
    "Stores": {
        "Revenue by Store": {"question": "Which stores generate the highest revenue?", "view": "dbo.vw_analytics_sales_by_store", "chart": "store_revenue"},
        "Orders by Store": {"question": "Which stores handle the most orders?", "view": "dbo.vw_analytics_sales_by_store", "chart": "store_orders"},
        "Average Order Value by Store": {"question": "Which stores have the highest average order value?", "view": "dbo.vw_analytics_sales_by_store", "chart": "store_aov"},
    },
    "Staff": {
        "Revenue by Staff": {"question": "Which staff members generate the highest revenue?", "view": "dbo.vw_analytics_sales_by_staff", "chart": "staff_revenue"},
        "Orders by Staff": {"question": "Which staff members handle the most orders?", "view": "dbo.vw_analytics_sales_by_staff", "chart": "staff_orders"},
        "Staff Performance": {"question": "Who are our top-performing staff members?", "view": "dbo.vw_analytics_sales_by_staff", "chart": "staff_performance"},
    },
}
