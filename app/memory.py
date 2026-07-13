import streamlit as st
from langchain_core.chat_history import InMemoryChatMessageHistory


# -----------------------------------------
# Session Memory Storage
# -----------------------------------------

if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = {}


# -----------------------------------------
# Get Chat History
# -----------------------------------------

def get_session_history(session_id="default"):

    if session_id not in st.session_state.chat_memory:

        st.session_state.chat_memory[session_id] = (
            InMemoryChatMessageHistory()
        )

    return st.session_state.chat_memory[session_id]



# -----------------------------------------
# Add User Message
# -----------------------------------------

def add_user_message(
    session_id,
    message
):

    history = get_session_history(
        session_id
    )

    history.add_user_message(
        message
    )



# -----------------------------------------
# Add AI Message
# -----------------------------------------

def add_ai_message(
    session_id,
    message
):

    history = get_session_history(
        session_id
    )

    history.add_ai_message(
        message
    )



# -----------------------------------------
# Clear Memory
# -----------------------------------------

def clear_history(
    session_id="default"
):

    if session_id in st.session_state.chat_memory:

        del st.session_state.chat_memory[session_id]