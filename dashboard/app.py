import streamlit as st

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


@st.cache_data(ttl=300)
def load_view(view_name: str):
    return read_view(view_name)


def render_overview() -> None:
    st.title("Bike Stores Analytics")
    st.caption("Business-ready analytics powered by the SQL Server data warehouse.")

    try:
        df = load_view("dbo.vw_analytics_sales_summary")
    except Exception as exc:
        st.error("Unable to load the analytics summary.")
        st.exception(exc)
        return

    if df.empty:
        st.warning("No analytics data is available.")
        return

    row = df.iloc[0]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Revenue", f"{row['total_revenue']:,.2f}")
    c2.metric("Total Orders", f"{int(row['total_orders']):,}")
    c3.metric("Items Sold", f"{int(row['total_items_sold']):,}")
    c4.metric("Average Order Value", f"{row['average_order_value']:,.2f}")

    st.divider()
    st.subheader("Explore the business")
    st.write("Choose a business area from the sidebar, then select a stakeholder question.")


def render_question(category: str, question_name: str) -> None:
    config = QUESTIONS[category][question_name]

    st.title(question_name)
    st.markdown(f"### ❓ {config['question']}")
    st.divider()

    try:
        df = load_view(config["view"])
    except Exception as exc:
        st.error("Unable to load analytics data.")
        st.exception(exc)
        return

    if df.empty:
        st.warning("No data is available for this question.")
        return

    try:
        fig = render_chart(config["chart"], df)
        st.pyplot(fig, use_container_width=True)
    except Exception as exc:
        st.error("Unable to render the selected chart.")
        st.exception(exc)
        return

    insight = generate_insight(category, question_name, df)
    if insight:
        st.info(f"💡 {insight}")

    with st.expander("View analytics data"):
        st.dataframe(df, use_container_width=True)


with st.sidebar:
    st.title("📊 Analytics")
    st.caption("Bike Stores Data Warehouse")
    st.divider()

    page = st.radio("Navigation", ["Overview", *QUESTIONS.keys()])

    if page != "Overview":
        st.divider()
        selected_question = st.selectbox(
            "Stakeholder Question",
            list(QUESTIONS[page].keys()),
        )
    else:
        selected_question = None


if page == "Overview":
    render_overview()
else:
    render_question(page, selected_question)
