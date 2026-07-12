from langchain_core.chat_history import InMemoryChatMessageHistory


# Store sessions
chat_sessions = {}


def get_session_history(session_id: str):
    """
    Get or create conversation history
    """

    if session_id not in chat_sessions:

        chat_sessions[session_id] = (
            InMemoryChatMessageHistory()
        )

    return chat_sessions[session_id]



def add_user_message(
    session_id: str,
    message: str
):

    history = get_session_history(
        session_id
    )

    history.add_user_message(
        message
    )



def add_ai_message(
    session_id: str,
    message: str
):

    history = get_session_history(
        session_id
    )

    history.add_ai_message(
        message
    )



def get_chat_history(
    session_id: str
):

    history = get_session_history(
        session_id
    )

    return history.messages