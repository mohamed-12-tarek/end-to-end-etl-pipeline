import pandas as pd


def _name(row, preferred, fallback):
    return row.get(preferred, row.get(fallback, "Unknown"))


def generate_insight(category: str, question: str, df: pd.DataFrame) -> str:
    if df.empty:
        return ""

    if category == "Sales":
        if "Revenue Over Time" == question and "revenue" in df:
            row = df.loc[df["revenue"].idxmax()]
            return f"Peak daily revenue was {row['revenue']:,.2f} on {row['full_date']} ."
        if "Orders Over Time" == question and "orders_count" in df:
            row = df.loc[df["orders_count"].idxmax()]
            return f"The highest order volume was {int(row['orders_count']):,} orders on {row['full_date']}."
        if "Average Order Value" == question and "average_order_value" in df:
            row = df.loc[df["average_order_value"].idxmax()]
            return f"The highest daily average order value was {row['average_order_value']:,.2f} on {row['full_date']}."
        if "Monthly Sales Trend" == question and "revenue" in df:
            row = df.loc[df["revenue"].idxmax()]
            return f"The strongest month was {row['month_name']} {int(row['year'])}, with revenue of {row['revenue']:,.2f}."

    if category == "Products":
        if "revenue" in df and "product_name" in df:
            row = df.loc[df["revenue"].idxmax()]
            if "Revenue" in question:
                return f"{_name(row, 'product_name', 'product_id')} is the top product by revenue at {row['revenue']:,.2f}."
        if "items_sold" in df and "product_name" in df and "Quantity" in question:
            row = df.loc[df["items_sold"].idxmax()]
            return f"{_name(row, 'product_name', 'product_id')} sold the most units: {int(row['items_sold']):,}."
        if "Product Performance" == question and {"items_sold", "revenue"}.issubset(df.columns):
            median_units = df["items_sold"].median()
            candidates = df[df["items_sold"] <= median_units]
            if not candidates.empty:
                row = candidates.loc[candidates["revenue"].idxmax()]
                return f"{_name(row, 'product_name', 'product_id')} stands out with {int(row['items_sold']):,} units sold and {row['revenue']:,.2f} revenue."

    if category in {"Stores", "Staff"} and "revenue" in df:
        name_col = "store_name" if category == "Stores" else "staff_name"
        row = df.loc[df["revenue"].idxmax()]
        if name_col in df:
            return f"{row[name_col]} leads {category.lower()} by revenue with {row['revenue']:,.2f}."

    return ""
