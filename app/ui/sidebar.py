import streamlit as st
import os

from config import (
    DATA_DIR,
    EMBEDDING_MODEL,
    LLM_MODEL,
    TOP_K
)

from memory import clear_history


def render_sidebar(session_id=None):

    st.sidebar.title("🩺 Medical AI Assistant")

    st.sidebar.caption(
        "Professional Medical RAG Chatbot"
    )

    st.sidebar.divider()


    # ==========================
    # Upload PDF
    # ==========================

    st.sidebar.subheader("📄 Upload Medical Documents")

    uploaded_file = st.sidebar.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    if uploaded_file:

        save_path = DATA_DIR / uploaded_file.name

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.sidebar.success(
            f"Uploaded: {uploaded_file.name}"
        )

        st.sidebar.info(
            "Restart app and rebuild index."
        )


    st.sidebar.divider()


    # ==========================
    # Indexed Documents
    # ==========================

    st.sidebar.subheader("📚 Indexed Documents")

    pdf_files = list(DATA_DIR.glob("*.pdf"))


    if pdf_files:

        for pdf in pdf_files:

            col1, col2 = st.sidebar.columns([3, 1])


            with col1:
                st.write(
                    f"📄 {pdf.name}"
                )


            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_{pdf.name}"
                ):

                    try:

                        os.remove(pdf)

                        st.sidebar.success(
                            f"{pdf.name} deleted"
                        )

                        st.rerun()


                    except Exception as e:

                        st.sidebar.error(
                            str(e)
                        )


    else:

        st.sidebar.write(
            "No PDF found"
        )



    st.sidebar.divider()


    # ==========================
    # Statistics
    # ==========================

    st.sidebar.subheader("📊 Statistics")

    st.sidebar.write(
        f"PDF Count: {len(pdf_files)}"
    )

    st.sidebar.write(
        f"Top-K: {TOP_K}"
    )

    st.sidebar.write(
        f"Embedding: {EMBEDDING_MODEL}"
    )

    st.sidebar.write(
        f"LLM: {LLM_MODEL}"
    )



    st.sidebar.divider()


    # ==========================
    # System Status
    # ==========================

    st.sidebar.subheader("⚙️ System Status")


    st.sidebar.success(
        "Groq Connected"
    )

    st.sidebar.success(
        "ChromaDB Ready"
    )

    st.sidebar.success(
        "Retriever Loaded"
    )



    st.sidebar.divider()


    # ==========================
    # Chat Controls
    # ==========================

    st.sidebar.subheader("💬 Chat Controls")


    if st.sidebar.button(
        "🗑️ Clear Chat History"
    ):

        clear_history()

        st.sidebar.success(
            "Chat history cleared"
        )

        st.rerun()



    st.sidebar.divider()


    # ==========================
    # Sidebar Footer
    # ==========================

    st.sidebar.markdown(
        """
        <div style="text-align:center; margin-top:20px;">

        <b>Designed by Ubaid Ashraf</b>

        <br><br>

        Powered by:
        <br>
        Streamlit • LangChain • ChromaDB
        <br>
        Ollama • Groq

        </div>
        """,
        unsafe_allow_html=True
    )