from pathlib import Path
import os
import uuid
import streamlit as st

from chatbot import ask_medical_ai
from vector_db import build_vector_database

# -------------------------------------------------
# Paths
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# Session State
# -------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# -------------------------------------------------
# Sidebar
# -------------------------------------------------

with st.sidebar:

    st.title("🩺 Medical AI Assistant")
    st.caption("Professional Medical RAG Chatbot")

    st.divider()

    # =====================================
    # Upload PDF
    # =====================================

    st.subheader("📂 Upload Medical PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"]
    )

    if uploaded_file is not None:

        save_path = DATA_DIR / uploaded_file.name

        if not save_path.exists():

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            with st.spinner("📚 Indexing PDF..."):
                st.cache_resource.clear()
                build_vector_database()

            st.success(f"✅ {uploaded_file.name} uploaded successfully!")
            st.rerun()

        else:
            st.warning("⚠️ This PDF already exists.")

    st.divider()

    # =====================================
    # Indexed Documents
    # =====================================

    st.subheader("📚 Indexed Documents")

    pdfs = sorted(DATA_DIR.glob("*.pdf"))

    if pdfs:

        for pdf in pdfs:

            col1, col2 = st.columns([6, 1])

            with col1:
                st.success(pdf.name)

            with col2:

                if st.button(
                    "🗑",
                    key=f"delete_{pdf.name}",
                    help="Delete PDF"
                ):

                    os.remove(pdf)

                    with st.spinner("Updating Vector Database..."):
                        st.cache_resource.clear()
                        build_vector_database()

                    st.success(f"{pdf.name} deleted successfully!")
                    st.rerun()

    else:
        st.warning("No PDF documents found.")

    st.divider()

    # =====================================
    # Statistics
    # =====================================

    st.subheader("📊 Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("PDFs", len(pdfs))

    with col2:
        st.metric("Top-K", "8")

    st.metric("Embedding Model", "nomic-embed-text")
    st.metric("LLM", "Llama 3.3 70B")

    st.divider()

    # =====================================
    # System Status
    # =====================================

    st.subheader("🟢 System Status")

    st.success("Groq Connected")
    st.success("ChromaDB Loaded")
    st.success("Retriever Ready")

    st.divider()

    # =====================================
    # Sample Questions
    # =====================================

    st.subheader("💡 Sample Questions")

    st.markdown("""
- What is diabetes?
- What are the symptoms of diabetes?
- What causes hypertension?
- What is insulin?
- Explain high blood pressure.
""")

    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    st.divider()

    st.caption("Medical AI Assistant v3.1")
    # -------------------------------------------------
# Main Page
# -------------------------------------------------

st.title("🩺 Medical AI Assistant")

st.caption(
    "Powered by Groq • ChromaDB • Ollama • LangChain"
)

st.info(
    """
This Medical AI Assistant uses Retrieval-Augmented Generation (RAG)
to answer questions based on your uploaded medical documents.

⚠️ This application is for educational purposes only and should not
replace professional medical advice.
"""
)

# -------------------------------------------------
# Display Previous Chat Messages
# -------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------------------------
# Chat Input
# -------------------------------------------------

prompt = st.chat_input("Ask a medical question...")

if prompt:

    # Save user message

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("🔍 Searching medical documents..."):

            response = ask_medical_ai(
                question=prompt,
                session_id=st.session_state.session_id
            )

        answer = response["answer"]
        sources = response["sources"]

        st.markdown(answer)

        # -----------------------------------------
        # Retrieved Source Documents
        # -----------------------------------------

        if sources:

            with st.expander(
                "📚 Retrieved Source Documents",
                expanded=False
            ):

                for i, doc in enumerate(sources, start=1):

                    source = Path(
                        doc.metadata.get("source", "Unknown")
                    ).name

                    page = (
                        doc.metadata.get("page", 0) + 1
                    )

                    st.markdown(f"### Source {i}")

                    st.write(f"**File:** {source}")
                    st.write(f"**Page:** {page}")

                    preview = doc.page_content

                    if len(preview) > 300:
                        preview = preview[:300] + "..."

                    st.caption(preview)

                    st.divider()

    # Save assistant response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )
    # -------------------------------------------------
# Footer
# -------------------------------------------------

st.divider()

st.subheader("🩺 Medical AI Assistant")

st.write("**Developed by Ubaid Ashraf**")

st.write(
    "B.Sc. (Hons.) Computer Science & Artificial Intelligence"
)

st.write(
    "Central University of Andhra Pradesh"
)

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.caption("Powered By")

    st.caption("• Streamlit")
    st.caption("• LangChain")
    st.caption("• ChromaDB")
    st.caption("• Ollama")
    st.caption("• Groq")

with col2:

    st.caption("Version")

    st.caption("v3.2")

st.divider()

st.caption("© 2026 Ubaid Ashraf. All Rights Reserved.")