
import streamlit as st
import pandas as pd

from charts import render_chart
from database import read_view
from insights import generate_insight
from questions import QUESTIONS


st.set_page_config(
    page_title="Bike Stores Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }

        [data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.25);
            border-radius: 12px;
            padding: 16px;
            background-color: rgba(128, 128, 128, 0.05);
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.9rem;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.8rem;
            font-weight: 700;
        }

        .section-title {
            font-size: 1.35rem;
            font-weight: 700;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
        }

        .section-description {
            color: #777;
            margin-bottom: 1rem;
        }

        .insight-box {
            border-radius: 12px;
            padding: 1rem 1.25rem;
            margin-top: 1rem;
            border: 1px solid rgba(128, 128, 128, 0.25);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

@st.cache_data(ttl=300)
def load_view(view_name: str) -> pd.DataFrame:
    return read_view(view_name)


def load_analytics_view(view_name: str) -> pd.DataFrame | None:
    try:
        df = load_view(view_name)
    except Exception as exc:
        st.error(f"Unable to load analytics view: {view_name}")
        st.exception(exc)
        return None

    if df.empty:
        st.warning(f"No data is available in {view_name}.")
        return None

    return df


def format_currency(value) -> str:
    """Format a numeric value as currency."""
    if pd.isna(value):
        return "0.00"

    return f"{float(value):,.2f}"


def format_integer(value) -> str:
    if pd.isna(value):
        return "0"

    return f"{int(value):,}"


def get_top_rows(df: pd.DataFrame, value_column: str, n: int = 5) -> pd.DataFrame:
    if value_column not in df.columns:
        return pd.DataFrame()

    return (
        df.sort_values(value_column, ascending=False)
        .head(n)
        .reset_index(drop=True)
    )


def render_overview() -> None:
    st.title("📊 Bike Stores Analytics")

    st.markdown(
        """
        Monitor sales performance, products, stores, and staff
        using the enterprise data warehouse.
        """
    )

    summary_df = load_analytics_view(
        "dbo.vw_analytics_sales_summary"
    )

    if summary_df is None:
        return

    row = summary_df.iloc[0]

    st.markdown(
        '<div class="section-title">Business Overview</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "💰 Total Revenue",
        format_currency(row["total_revenue"]),
    )

    c2.metric(
        "🧾 Total Orders",
        format_integer(row["total_orders"]),
    )

    c3.metric(
        "📦 Items Sold",
        format_integer(row["total_items_sold"]),
    )

    c4.metric(
        "💵 Average Order Value",
        format_currency(row["average_order_value"]),
    )

    sales_df = load_analytics_view(
        "dbo.vw_analytics_sales_overview"
    )

    if sales_df is not None:

        st.markdown(
            '<div class="section-title">Sales Performance</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-description">'
            "Track how revenue and orders change over time."
            "</div>",
            unsafe_allow_html=True,
        )

        tab1, tab2 = st.tabs(
            [
                "💰 Revenue",
                "🧾 Orders",
            ]
        )

        with tab1:
            try:
                fig = render_chart(
                    "revenue_over_time",
                    sales_df,
                )
                st.pyplot(fig, use_container_width=True)
            except Exception as exc:
                st.error("Unable to render revenue trend.")
                st.exception(exc)

        with tab2:
            try:
                fig = render_chart(
                    "orders_over_time",
                    sales_df,
                )
                st.pyplot(fig, use_container_width=True)
            except Exception as exc:
                st.error("Unable to render orders trend.")
                st.exception(exc)

    st.markdown(
        '<div class="section-title">Business Performance</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🏆 Top Products")

        products_df = load_analytics_view(
            "dbo.vw_analytics_sales_by_product"
        )

        if products_df is not None:

            top_products = get_top_rows(
                products_df,
                "revenue",
                5,
            )

            if not top_products.empty:

                display_columns = [
                    column
                    for column in [
                        "product_name",
                        "category_name",
                        "revenue",
                        "items_sold",
                    ]
                    if column in top_products.columns
                ]

                display_df = top_products[display_columns].copy()

                if "revenue" in display_df.columns:
                    display_df["revenue"] = display_df["revenue"].map(
                        lambda x: f"{x:,.2f}"
                    )

                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                )

    with col2:

        st.subheader("🏪 Top Stores")

        stores_df = load_analytics_view(
            "dbo.vw_analytics_sales_by_store"
        )

        if stores_df is not None:

            top_stores = get_top_rows(
                stores_df,
                "revenue",
                5,
            )

            if not top_stores.empty:

                display_columns = [
                    column
                    for column in [
                        "store_name",
                        "city",
                        "state",
                        "revenue",
                        "orders_count",
                    ]
                    if column in top_stores.columns
                ]

                display_df = top_stores[display_columns].copy()

                if "revenue" in display_df.columns:
                    display_df["revenue"] = display_df["revenue"].map(
                        lambda x: f"{x:,.2f}"
                    )

                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                )

    st.markdown(
        '<div class="section-title">Category Performance</div>',
        unsafe_allow_html=True,
    )

    categories_df = load_analytics_view(
        "dbo.vw_analytics_sales_by_category"
    )

    if categories_df is not None:

        top_categories = get_top_rows(
            categories_df,
            "revenue",
            10,
        )

        if not top_categories.empty:

            display_columns = [
                column
                for column in [
                    "category_name",
                    "revenue",
                    "items_sold",
                    "orders_count",
                    "average_discount",
                ]
                if column in top_categories.columns
            ]

            display_df = top_categories[display_columns].copy()

            if "revenue" in display_df.columns:
                display_df["revenue"] = display_df["revenue"].map(
                    lambda x: f"{x:,.2f}"
                )

            if "average_discount" in display_df.columns:
                display_df["average_discount"] = display_df[
                    "average_discount"
                ].map(
                    lambda x: f"{x:,.2f}"
                )

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
            )

    insight = generate_insight(
        "Sales",
        "Business Overview",
        summary_df,
    )

    if insight:

        st.markdown(
            '<div class="section-title">💡 Business Insight</div>',
            unsafe_allow_html=True,
        )

        st.info(insight)

    with st.expander("🔎 View Summary Data"):

        st.dataframe(
            summary_df,
            use_container_width=True,
            hide_index=True,
        )


def render_question(
    category: str,
    question_name: str,
) -> None:

    config = QUESTIONS[category][question_name]

    st.title(question_name)

    st.markdown(
        f"### ❓ {config['question']}"
    )

    st.divider()

    df = load_analytics_view(config["view"])

    if df is None:
        return

    try:

        fig = render_chart(
            config["chart"],
            df,
        )

        st.pyplot(
            fig,
            use_container_width=True,
        )

    except Exception as exc:

        st.error(
            "Unable to render the selected chart."
        )

        st.exception(exc)

        return

    insight = generate_insight(
        category,
        question_name,
        df,
    )

    if insight:

        st.markdown(
            '<div class="section-title">💡 Business Insight</div>',
            unsafe_allow_html=True,
        )

        st.info(insight)

    with st.expander("🔎 View Analytics Data"):

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
        )

with st.sidebar:

    st.title("📊 Bike Stores")

    st.caption(
        "Business Intelligence Dashboard"
    )

    st.divider()

    page = st.radio(
        "Business Area",
        [
            "Overview",
            *QUESTIONS.keys(),
        ],
    )

    if page != "Overview":

        st.divider()

        st.caption(
            f"Explore {page.lower()} performance"
        )

        selected_question = st.selectbox(
            "Stakeholder Question",
            list(QUESTIONS[page].keys()),
        )

    else:

        selected_question = None

if page == "Overview":

    render_overview()

else:

    render_question(
        page,
        selected_question,
    )

