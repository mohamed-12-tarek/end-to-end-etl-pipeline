import matplotlib.pyplot as plt
import seaborn as sns


sns.set_theme(
    style="whitegrid",
    context="notebook",
)


def revenue_over_time(df):
    fig, ax = plt.subplots(figsize=(12, 5))

    sns.lineplot(
        data=df,
        x="full_date",
        y="revenue",
        marker="o",
        ax=ax,
    )

    ax.set_title("Sales Revenue Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Revenue")
    fig.tight_layout()

    return fig


def orders_over_time(df):
    fig, ax = plt.subplots(figsize=(12, 5))

    sns.lineplot(
        data=df,
        x="full_date",
        y="orders_count",
        marker="o",
        ax=ax,
    )

    ax.set_title("Orders Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Orders")
    fig.tight_layout()

    return fig


def aov_over_time(df):
    fig, ax = plt.subplots(figsize=(12, 5))

    sns.lineplot(
        data=df,
        x="full_date",
        y="average_order_value",
        marker="o",
        ax=ax,
    )

    ax.set_title("Average Order Value Over Time")
    ax.set_xlabel("Date")
    ax.set_ylabel("Average Order Value")
    fig.tight_layout()

    return fig


def top_products_revenue(df):
    data = (
        df.sort_values("revenue", ascending=False)
        .head(10)
        .sort_values("revenue")
    )

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(
        data=data,
        x="revenue",
        y="product_name",
        ax=ax,
    )

    ax.set_title("Top 10 Products by Revenue")
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Product")
    fig.tight_layout()

    return fig


def product_performance(df):
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.scatterplot(
        data=df,
        x="items_sold",
        y="revenue",
        size="orders_count",
        hue="category_name",
        alpha=0.75,
        ax=ax,
    )

    ax.set_title("Product Performance")
    ax.set_xlabel("Items Sold")
    ax.set_ylabel("Revenue")
    fig.tight_layout()

    return fig


def store_revenue(df):
    data = df.sort_values("revenue", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=data,
        x="revenue",
        y="store_name",
        ax=ax,
    )

    ax.set_title("Revenue by Store")
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Store")
    fig.tight_layout()

    return fig


def staff_revenue(df):
    data = df.sort_values("revenue", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.barplot(
        data=data,
        x="revenue",
        y="staff_name",
        ax=ax,
    )

    ax.set_title("Revenue by Staff")
    ax.set_xlabel("Revenue")
    ax.set_ylabel("Staff")
    fig.tight_layout()

    return fig