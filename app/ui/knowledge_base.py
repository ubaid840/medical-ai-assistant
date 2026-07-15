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
        <div class="card" style="margin-bottom: 15px; padding: 20px;">
            <h3 style="margin-bottom: 5px;">📚 Knowledge Base</h3>
            <p style="color: #64748b; font-size: 0.95rem; margin-bottom: 0;">
                Medical documents are stored using Retrieval Augmented Generation (RAG).
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    extensions = ['*.pdf', '*.txt', '*.docx', '*.csv']
    all_files = []
    for ext in extensions:
        all_files.extend(list(DATA_DIR.glob(ext)))

    # Compact Stats Row
    st.markdown(
        f"""
        <div style="display: flex; gap: 15px; margin-bottom: 20px;">
            <div class="card" style="flex: 1; padding: 15px 20px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: center;">
                <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Medical Docs</div>
                <div style="color: #0ea5e9; font-size: 1.6rem; font-weight: 800;">{len(all_files)}</div>
            </div>
            <div class="card" style="flex: 1; padding: 15px 20px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: center;">
                <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">Vector Database</div>
                <div style="color: #0ea5e9; font-size: 1.4rem; font-weight: 800;">ChromaDB</div>
            </div>
            <div class="card" style="flex: 1; padding: 15px 20px; margin-bottom: 0; display: flex; flex-direction: column; justify-content: center;">
                <div style="color: #64748b; font-size: 0.85rem; font-weight: 600; text-transform: uppercase;">LLM Engine</div>
                <div style="color: #0ea5e9; font-size: 1.4rem; font-weight: 800;">Llama 3.3</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.subheader("📄 Indexed Documents")

    if all_files:
        st.markdown('<div class="card" style="padding: 15px;">', unsafe_allow_html=True)
        for doc_file in all_files:
            st.markdown(f'<div style="padding: 8px 0; border-bottom: 1px solid #f1f5f9;">📄 <b>{doc_file.name}</b></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("No medical documents have been indexed yet. Upload documents from the sidebar.")

    st.subheader("🤖 AI Stack Components")
    
    st.markdown(
        """
        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px;">
            <span style="background: rgba(14, 165, 233, 0.1); color: #0284c7; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(14, 165, 233, 0.2);">✅ Groq API</span>
            <span style="background: rgba(14, 165, 233, 0.1); color: #0284c7; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(14, 165, 233, 0.2);">✅ LangChain</span>
            <span style="background: rgba(14, 165, 233, 0.1); color: #0284c7; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(14, 165, 233, 0.2);">✅ ChromaDB</span>
            <span style="background: rgba(14, 165, 233, 0.1); color: #0284c7; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; border: 1px solid rgba(14, 165, 233, 0.2);">✅ Ollama Embeddings</span>
        </div>
        """,
        unsafe_allow_html=True
    )