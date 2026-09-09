import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", context="notebook")


def _bar(df, x, y, title, xlabel, ylabel, top_n=None):
    data = df.sort_values(x, ascending=False)
    if top_n:
        data = data.head(top_n)
    data = data.sort_values(x)
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(data=data, x=x, y=y, ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    fig.tight_layout()
    return fig


def revenue_over_time(df):
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=df, x="full_date", y="revenue", marker="o", ax=ax)
    ax.set_title("Sales Revenue Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")
    fig.tight_layout()
    return fig


def orders_over_time(df):
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=df, x="full_date", y="orders_count", marker="o", ax=ax)
    ax.set_title("Orders Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Orders")
    fig.tight_layout()
    return fig


def aov_over_time(df):
    fig, ax = plt.subplots(figsize=(12, 5))
    sns.lineplot(data=df, x="full_date", y="average_order_value", marker="o", ax=ax)
    ax.set_title("Average Order Value Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Average Order Value")
    fig.tight_layout()
    return fig


def monthly_revenue(df):
    fig, ax = plt.subplots(figsize=(12, 5))
    data = df.sort_values(["year", "month"])
    data = data.assign(period=data["year"].astype(str) + "-" + data["month"].astype(str).str.zfill(2))
    sns.lineplot(data=data, x="period", y="revenue", marker="o", ax=ax)
    ax.set_title("Monthly Sales Trend")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()
    return fig


def top_products_revenue(df):
    return _bar(df, "revenue", "product_name", "Top 10 Products by Revenue", "Revenue", "Product", 10)


def top_products_quantity(df):
    return _bar(df, "items_sold", "product_name", "Top 10 Products by Quantity", "Items Sold", "Product", 10)


def product_performance(df):
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.scatterplot(data=df, x="items_sold", y="revenue", size="orders_count", hue="category_name", alpha=0.75, ax=ax)
    ax.set_title("Product Performance")
    ax.set_xlabel("Items Sold")
    ax.set_ylabel("Revenue")
    fig.tight_layout()
    return fig


def store_revenue(df):
    return _bar(df, "revenue", "store_name", "Revenue by Store", "Revenue", "Store")


def store_orders(df):
    return _bar(df, "orders_count", "store_name", "Orders by Store", "Orders", "Store")


def store_aov(df):
    return _bar(df, "average_order_value", "store_name", "Average Order Value by Store", "Average Order Value", "Store")


def staff_revenue(df):
    return _bar(df, "revenue", "staff_name", "Revenue by Staff", "Revenue", "Staff")


def staff_orders(df):
    return _bar(df, "orders_count", "staff_name", "Orders by Staff", "Orders", "Staff")


def staff_performance(df):
    return _bar(df, "revenue", "staff_name", "Staff Performance", "Revenue", "Staff")


CHARTS = {
    name: func
    for name, func in globals().items()
    if callable(func) and not name.startswith("_")
}


def render_chart(name, df):
    try:
        return CHARTS[name](df)
    except KeyError as exc:
        raise ValueError(f"Unknown chart: {name}") from exc
