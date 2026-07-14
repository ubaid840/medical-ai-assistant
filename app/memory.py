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

        from chat_history import get_messages
        history = InMemoryChatMessageHistory()
        
        # Load from SQLite if exists
        try:
            db_messages = get_messages(session_id)
            for role, msg, ts in db_messages:
                if role == "user":
                    history.add_user_message(msg)
                else:
                    history.add_ai_message(msg)
        except Exception:
            pass

        st.session_state.chat_memory[session_id] = history

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