from pathlib import Path
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"


def render_knowledge_base():
    """
    Knowledge Base UI
    """

    st.markdown(
        """
        <div class="card">

        <h3>📚 Knowledge Base</h3>

        Medical documents are stored using
        Retrieval Augmented Generation (RAG).

        </div>
        """,
        unsafe_allow_html=True,
    )

    pdf_files = list(DATA_DIR.glob("*.pdf"))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Medical PDFs",
            len(pdf_files),
        )

    with col2:
        st.metric(
            "Vector Database",
            "ChromaDB",
        )

    with col3:
        st.metric(
            "LLM",
            "Llama 3.3",
        )

    st.divider()

    st.subheader("📄 Documents")

    if pdf_files:

        for pdf in pdf_files:
            st.write(f"📄 {pdf.name}")

    else:

        st.warning("No documents found.")

    st.divider()

    st.subheader("🤖 AI Components")

    st.success("✅ Groq API")
    st.success("✅ LangChain")
    st.success("✅ ChromaDB")
    st.success("✅ Ollama Embeddings")