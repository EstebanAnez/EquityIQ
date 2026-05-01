# streamlit file
# pip install streamlit
import streamlit as st
from EquityIQ_step_5 import initialize_messages, get_equityiq_response

# load the two images into the code
company_logo = "Images/EquityIQ_Big.jpeg"
equityiq_icon = "Images/EquityIQ_Small.png"

# this sets up the name in the browser tab
st.set_page_config(
    page_title="EquityIQ – AI-Powered Equity Research Agent",
    layout="centered"
)

# add background styling
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to bottom, #eef2f7, #dbe5f1);
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# add the company logo on top of the page
st.image(company_logo)

# add a title under the company logo
st.title("EquityIQ – AI-Powered Equity Research Agent")

# add a short description under the title
st.markdown(
    "Analyze stocks using structured, analyst-style reasoning. "
    "Explore valuation, growth, risks, performance, and real-time news insights."
)

st.divider()

# Initialize conversation memory once per session
# the conversation is initialized with the system prompt
# this code is using function initialize_messages() in the other file
if "messages" not in st.session_state:
    st.session_state.messages = initialize_messages()

# quick analysis options
st.markdown("### Quick Analysis Options")

col1, col2, col3 = st.columns(3)

button_prompt = None

if col1.button("📊 Full Company Analysis"):
    button_prompt = "Analyze Apple using financial ratios, price performance, news sentiment, latest headlines, and equity research style reasoning."

if col2.button("📰 News + Sentiment"):
    button_prompt = "Analyze recent news sentiment for Apple."

if col3.button("🧠 Latest Headlines"):
    button_prompt = "What are the latest news headlines for Apple?"

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user", avatar="📈").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant", avatar=equityiq_icon).write(msg["content"])

# Chat input
# allows the user to type in a new prompt
user_input = st.chat_input("Ask EquityIQ about a stock...")

# if a quick button is clicked, use that prompt
if button_prompt:
    user_input = button_prompt

if user_input:
    # displays the new prompt as part of the conversation
    st.chat_message("user", avatar="📈").write(user_input)

    # calls function get_equityiq_response()
    # from the other file. The function updates the list by appending the
    # new message(s) and returns the LLM response to the latest prompt
    with st.spinner("EquityIQ is analyzing..."):
        response, updated_messages = get_equityiq_response(
            st.session_state.messages,
            user_input
        )

    # replace the session_state.messages with the updated list of messages
    st.session_state.messages = updated_messages

    # display the LLMs latest response
    st.chat_message("assistant", avatar=equityiq_icon).write(response)