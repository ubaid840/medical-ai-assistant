from pathlib import Path
import streamlit as st


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

st.markdown(
    """
    <style>

    .main-title {

        text-align:center;
        font-size:50px;
        font-weight:800;
        margin-top:20px;

    }


    .sub-title {

        text-align:center;
        font-size:18px;
        color:#777;
        margin-bottom:30px;

    }


    .footer {

        position:fixed;
        bottom:10px;
        left:0;
        right:0;
        text-align:center;
        font-size:14px;
        color:gray;

    }


    </style>
    """,
    unsafe_allow_html=True
)



# =====================================================
# HEADER
# =====================================================

st.markdown(
    """
    <div class="main-title">

    🩺 Medical AI Assistant

    </div>


    <div class="sub-title">

    AI-powered Medical Knowledge Assistant
    <br>
    Powered by Groq • LangChain • ChromaDB • Ollama

    </div>

    """,
    unsafe_allow_html=True
)



# =====================================================
# SIDEBAR
# =====================================================

render_sidebar()



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
        session_id="default"
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



# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer">

    Designed by Ubaid Ashraf

    </div>

    """,
    unsafe_allow_html=True
)