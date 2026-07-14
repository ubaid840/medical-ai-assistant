import streamlit as st
import os

from config import (
    DATA_DIR,
    EMBEDDING_MODEL,
    LLM_MODEL,
    TOP_K
)

from memory import clear_history, get_session_history
from chat_history import get_all_sessions, create_session, delete_session


def render_sidebar(session_id=None):

    st.sidebar.title("🩺 Medical AI Assistant")

    st.sidebar.caption(
        "Professional Medical RAG Chatbot"
    )
    
    st.sidebar.divider()

    # ==========================
    # Chat Sessions
    # ==========================
    
    st.sidebar.subheader("💬 Chat Sessions")
    
    if st.sidebar.button("➕ New Chat", use_container_width=True):
        st.session_state.session_id = create_session("New Chat")
        st.session_state.chat_memory = {}
        st.rerun()

    sessions = get_all_sessions()
    
    if sessions:
        # Create a dictionary of session titles {session_id: title}
        # sessions format: [(session_id, title, created_at), ...]
        session_opts = {s[0]: f"{s[1]} ({s[2][:10]})" for s in sessions} 
        
        # Determine current index
        current_id = st.session_state.session_id
        session_ids = list(session_opts.keys())
        current_index = session_ids.index(current_id) if current_id in session_ids else 0

        selected_id = st.sidebar.selectbox(
            "Select Past Chat",
            options=session_ids,
            format_func=lambda x: session_opts[x],
            index=current_index,
        )

        if selected_id != st.session_state.session_id:
            st.session_state.session_id = selected_id
            st.rerun()

        if st.sidebar.button("🗑️ Delete This Chat"):
            delete_session(st.session_state.session_id)
            if st.session_state.session_id in st.session_state.chat_memory:
                del st.session_state.chat_memory[st.session_state.session_id]
            st.session_state.session_id = create_session("New Chat")
            st.rerun()
    else:
        st.sidebar.info("No past chats.")

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

        clear_history(session_id)

        st.sidebar.success(
            "Chat history cleared"
        )

        st.rerun()

    # Chat Export
    history = get_session_history(session_id if session_id else "default")
    chat_text = "# Medical AI Chat History\n\n"
    
    has_messages = hasattr(history, "messages") and bool(history.messages)
    if has_messages:
        for msg in history.messages:
            role = "Patient" if msg.type == "human" else "AI Assistant"
            chat_text += f"**{role}**:\n{msg.content}\n\n---\n\n"
            
    st.sidebar.download_button(
        label="💾 Download Chat History",
        data=chat_text,
        file_name="medical_chat_history.md",
        mime="text/markdown"
    )

    st.sidebar.divider()


    # ==========================
    # Sidebar Footer
    # ==========================

    st.sidebar.markdown(
        """
        <div style="text-align:center; margin-top:20px;">

        <b>Designed by Ubaid Ashraf</b>
        <br>
        <span style="font-size: 14px; color: gray;">© 2026 All Rights Reserved</span>

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