from pathlib import Path
import streamlit as st

from chatbot import ask_medical_ai
from memory import get_session_history


def render_chat(session_id: str):
    """
    Medical Chat Interface
    """

    st.markdown(
        """
        <div class="card">

        <h3>🩺 Medical Consultation</h3>

        Ask questions from uploaded medical documents.

        </div>
        """,
        unsafe_allow_html=True,
    )

    history = get_session_history(session_id)

    # Display conversation
    for message in history.messages:

        role = "user" if message.type == "human" else "assistant"

        with st.chat_message(role):
            st.markdown(message.content)

    question = st.chat_input(
        "Ask a medical question..."
    )

    if not question:
        return

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Analyzing medical knowledge..."):

            try:

                response = ask_medical_ai(
                    question,
                    session_id,
                )

                answer = response.get(
                    "answer",
                    "No answer generated.",
                )

                st.markdown(answer)

                sources = response.get(
                    "sources",
                    [],
                )

                if sources:

                    with st.expander("📚 View Sources"):

                        for i, doc in enumerate(
                            sources,
                            start=1,
                        ):

                            filename = Path(
                                doc.metadata.get(
                                    "source",
                                    "Unknown",
                                )
                            ).name

                            page = (
                                doc.metadata.get(
                                    "page",
                                    0,
                                )
                                + 1
                            )

                            st.markdown(
                                f"""
**Source {i}**

📄 **File:** {filename}

📑 **Page:** {page}
"""
                            )

            except Exception as e:

                st.error(
                    f"❌ {e}"
                )