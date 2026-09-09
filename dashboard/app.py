import streamlit as st

from questions import QUESTIONS
from database import read_view
import charts


st.set_page_config(
    page_title="Bike Stores Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:

    st.title("📊 Analytics")
    st.divider()

    category = st.radio(
        "Business Area",
        list(QUESTIONS.keys()),
    )

    st.divider()
    questions = QUESTIONS[category]

    selected_question = st.selectbox(
        "Stakeholder Question",
        list(questions.keys()),
    )

question_config = questions[selected_question]
question_text = question_config["question"]
view_name = question_config["view"]
chart_name = question_config["chart"]


st.title(selected_question)

st.markdown(f"### ❓ {question_text}")

st.divider()


@st.cache_data(ttl=300)
def load_data(view):
    return read_view(view)


try:
    df = load_data(view_name)
except Exception as exc:
    st.error("Unable to load analytics data.")
    st.exception(exc)
    st.stop()

chart_function = getattr(
    charts,
    chart_name,
    None,
)


if chart_function is None:
    st.error(f"Chart '{chart_name}' is not implemented.")
    st.stop()

fig = chart_function(df)
st.pyplot(fig, use_container_width=True)