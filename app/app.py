from pathlib import Path
import streamlit as st

from database import initialize_database
from chat_history import create_session

from ui.sidebar import render_sidebar
from ui.disclaimer import show_disclaimer
from ui.chat import render_chat
from ui.analysis import render_analysis
from ui.knowledge_base import render_knowledge_base


# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)
# =====================================================
# INITIALIZE DATABASE
# =====================================================

initialize_database()



# =====================================================
# PATHS
# =====================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(
    exist_ok=True
)



# =====================================================
# CUSTOM CSS
# =====================================================

def load_css():
    css_path = BASE_DIR / "assets" / "style.css"
    if css_path.exists():
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()


# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <div style="text-align: center; padding-top: 1rem; padding-bottom: 2rem;">
        <div style="position: relative; display: inline-flex; justify-content: center; align-items: center; margin-bottom: 1.5rem;">
            <div style="position: absolute; width: 120px; height: 120px; background: radial-gradient(circle, rgba(14,165,233,0.15) 0%, rgba(255,255,255,0) 70%); border-radius: 50%;"></div>
            <div style="display: inline-flex; align-items: center; justify-content: center; width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #0ea5e9, #6366f1); box-shadow: 0 10px 25px rgba(14, 165, 233, 0.4); z-index: 1;">
                <span style="font-size: 40px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2)); color: white;">🧬</span>
            </div>
        </div>
        <h1 style="font-size: 3.5rem; font-weight: 900; margin: 0 0 10px 0; background: linear-gradient(135deg, #0ea5e9, #6366f1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1.5px; line-height: 1.1;">
            Medical AI Assistant
        </h1>
        <p style="font-size: 1.15rem; color: #64748b; margin-top: 0; font-weight: 500; letter-spacing: 0.2px;">
            Advanced Clinical Intelligence & Diagnostic Analysis
        </p>
        <div style="margin-top: 1.5rem; display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
            <span style="background: white; color: #475569; padding: 6px 14px; border-radius: 30px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">⚡ Groq AI</span>
            <span style="background: white; color: #475569; padding: 6px 14px; border-radius: 30px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">🔗 LangChain</span>
            <span style="background: white; color: #475569; padding: 6px 14px; border-radius: 30px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">🗄️ ChromaDB</span>
            <span style="background: white; color: #475569; padding: 6px 14px; border-radius: 30px; font-size: 0.75rem; font-weight: 700; letter-spacing: 0.5px; text-transform: uppercase; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e2e8f0;">🦙 Ollama</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)



# =====================================================
# SESSION MANAGEMENT
# =====================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = create_session("New Chat")

if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = {}


# =====================================================
# SIDEBAR
# =====================================================

render_sidebar(session_id=st.session_state.session_id)



# =====================================================
# DISCLAIMER
# =====================================================

show_disclaimer()



# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3 = st.tabs(
    [
        "💬 Medical Chat",
        "📊 Health Analysis",
        "📚 Knowledge Base"
    ]
)



# =====================================================
# CHAT
# =====================================================

with tab1:

    render_chat(
        session_id=st.session_state.session_id
    )



# =====================================================
# ANALYSIS
# =====================================================

with tab2:

    render_analysis()



# =====================================================
# KNOWLEDGE BASE
# =====================================================

with tab3:

    render_knowledge_base()