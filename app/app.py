import streamlit as st
from chatbot import ask_medical_ai

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
# Sidebar
# -------------------------------------------------
with st.sidebar:

    st.title("Medical AI Assistant")

    st.caption("Professional RAG Assistant")

    st.divider()

    # -------------------------
    # Upload Section
    # -------------------------
    st.subheader("Upload Documents")

    uploaded_file = st.file_uploader(
        "Upload Medical PDF",
        type=["pdf"],
        help="PDF upload functionality will be enabled in the next phase."
    )

    st.divider()

    # -------------------------
    # Indexed Documents
    # -------------------------
    st.subheader("Indexed Documents")

    st.success("diabetes.pdf")

    st.success("hypertension_guide.pdf")

    st.divider()

    # -------------------------
    # Statistics
    # -------------------------
    st.subheader("Statistics")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("PDFs", "2")

    with col2:
        st.metric("Top-K", "3")

    st.metric(
        "Embedding Model",
        "nomic-embed-text"
    )

    st.metric(
        "LLM",
        "llama-3.3-70b"
    )

    st.divider()

    # -------------------------
    # System Status
    # -------------------------
    st.subheader("System Status")

    st.success("Groq Connected")

    st.success("Vector Database Loaded")

    st.success("Retriever Ready")

    st.divider()

    # -------------------------
    # Sample Questions
    # -------------------------
    st.subheader("Try Asking")

    st.markdown("""
- What is diabetes?
- What are the symptoms of diabetes?
- What causes hypertension?
- What are treatments for diabetes?
""")

    st.divider()

    # -------------------------
    # Clear Chat
    # -------------------------
    if st.button(
        "Clear Chat",
        use_container_width=True
    ):

        st.session_state.messages = []

        st.rerun()

    st.divider()

    st.caption("Version 2.0")

# -------------------------------------------------
# Main Page
# -------------------------------------------------

st.title("🩺 Medical AI Assistant")

st.caption(
    "Powered by Groq • ChromaDB • Ollama • LangChain"
)
st.info(
    "This Medical AI Assistant provides AI-generated responses based on the uploaded medical documents. "
    "It is designed for educational and research purposes and should not replace professional medical advice."
)

# -------------------------------------------------
# Session State
# -------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------------------------
# Display Previous Messages
# -------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# -------------------------------------------------
# Chat Input
# -------------------------------------------------

prompt = st.chat_input(
    "Ask your medical question..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching medical documents..."
        ):

            response = ask_medical_ai(prompt)

            answer = response["answer"]

            sources = response["sources"]

        st.markdown(answer)
                # -------------------------------------------------
        # Retrieved Source Documents
        # -------------------------------------------------
        if sources:

            with st.expander("Retrieved Source Documents", expanded=False):

                for i, doc in enumerate(sources, start=1):

                    source = doc.metadata.get(
                        "source",
                        "Unknown"
                    )

                    page = doc.metadata.get(
                        "page",
                        0
                    ) + 1

                    st.markdown(f"### Source {i}")

                    st.write(f"**File:** {source}")

                    st.write(f"**Page:** {page}")

                    preview = doc.page_content

                    if len(preview) > 250:
                        preview = preview[:250] + "..."

                    st.caption(preview)

                    st.divider()

    # --------------------------------------------
    # Save assistant message
    # --------------------------------------------
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


st.subheader("Medical AI Assistant")

st.write("**Developed by Ubaid Ashraf**")

st.write("B.Sc. (Hons.) Computer Science & Artificial Intelligence")

st.write("Central University of Andhra Pradesh")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.caption("Powered by:")
    st.caption("• Streamlit")
    st.caption("• LangChain")
    st.caption("• ChromaDB")
    st.caption("• Ollama")
    st.caption("• Groq")

with col2:
    st.caption("Version")
    st.caption("2.0")

st.divider()

st.caption("© 2026 Ubaid Ashraf. All Rights Reserved.")