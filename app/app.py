import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

try:
    __import__('pysqlite3')
    import sys
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except ImportError:
    pass

from pathlib import Path
import streamlit as st

from database import initialize_database
from chat_history import create_session

from ui.sidebar import render_sidebar
from ui.disclaimer import show_disclaimer
from ui.chat import render_chat
from ui.analysis import render_analysis
from ui.pharmacology import render_pharmacology
from ui.knowledge_base import render_knowledge_base
from ui.operations import render_operations
from ui.routines import render_routines
from ui.audit import render_audit_dashboard
from ui.cbt import render_cbt_tab
from ui.pediatrics import render_pediatrics
from ui.dashboard import render_dashboard
from ui.imaging import render_imaging
from ui.wearables import render_wearables
from ui.research import render_research

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
<style>
.ekg-line {
    stroke-dasharray: 2000;
    stroke-dashoffset: 2000;
    animation: draw-ekg 6s infinite linear;
}
@keyframes draw-ekg {
    0% { stroke-dashoffset: 2000; }
    50% { stroke-dashoffset: 0; }
    100% { stroke-dashoffset: -2000; }
}
</style>
<div style="
position: relative;
overflow: hidden;
text-align: center; 
padding-top: 3rem; 
padding-bottom: 3rem; 
margin-bottom: 2rem;
border-radius: 20px;
background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
box-shadow: 0 10px 30px rgba(14, 165, 233, 0.05);
border: 2px solid #ef4444;
">
    <!-- Animated EKG Background -->
    <svg viewBox="0 0 1000 200" preserveAspectRatio="none" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.15; z-index: 0; pointer-events: none;">
        <path class="ekg-line" d="M0,100 L250,100 L270,70 L290,140 L320,30 L350,170 L370,80 L390,100 L700,100 L720,70 L740,140 L770,30 L800,170 L820,80 L840,100 L1000,100" fill="none" stroke="#0ea5e9" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>

<!-- Medical Plus Symbols -->
<div style="position: absolute; top: 25px; left: 25px; color: #991b1b; font-size: 2.5rem; font-weight: bold; line-height: 1; opacity: 0.6; z-index: 1;">+</div>
<div style="position: absolute; top: 25px; right: 25px; color: #991b1b; font-size: 2.5rem; font-weight: bold; line-height: 1; opacity: 0.6; z-index: 1;">+</div>

<div style="position: relative; z-index: 1;">
<div style="position: relative; display: inline-flex; justify-content: center; align-items: center; margin-bottom: 1.5rem;">
<div style="position: absolute; width: 120px; height: 120px; background: radial-gradient(circle, rgba(14,165,233,0.15) 0%, rgba(255,255,255,0) 70%); border-radius: 50%;"></div>
<div style="display: inline-flex; align-items: center; justify-content: center; width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #0ea5e9, #6366f1); box-shadow: 0 10px 25px rgba(14, 165, 233, 0.4); z-index: 1;">
<span style="font-size: 40px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2)); color: white;">🩺</span>
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

st.divider()

show_disclaimer()



# =====================================================
# TABS
# =====================================================

st.divider()

st.markdown("""
<style>
/* Aggressive CSS to add vertical bars between tabs */
div[data-testid="stTabs"] button[data-baseweb="tab"] {
    border-right: 2px solid #cbd5e1 !important;
    border-radius: 0px !important;
    margin-right: 0px !important;
}
div[data-testid="stTabs"] button[data-baseweb="tab"]:last-child {
    border-right: none !important;
}
/* For newer Streamlit versions */
div[data-testid="stTabs"] button[id^="tabs-bui"] {
    border-right: 2px solid #cbd5e1 !important;
    border-radius: 0px !important;
}
div[data-testid="stTabs"] button[id^="tabs-bui"]:last-child {
    border-right: none !important;
}
</style>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13 = st.tabs(
    [
        "💬 Chat",
        "｜ 🔬 Analysis",
        "｜ 💊 Pharmacology",
        "｜ 🧠 Knowledge",
        "｜ 📅 Intake",
        "｜ 💊 Routines",
        "｜ 🔒 Audit",
        "｜ 🧘 Wellness",
        "｜ 👶 Pediatrics",
        "｜ 📈 Dashboard",
        "｜ 🩻 Imaging",
        "｜ ⌚ Wearables",
        "｜ 🔬 Research"
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
# PHARMACOLOGY
# =====================================================

with tab3:
    render_pharmacology()

# =====================================================
# KNOWLEDGE BASE
# =====================================================

with tab4:
    render_knowledge_base()

# =====================================================
# OPERATIONS & INTAKE
# =====================================================

with tab5:
    render_operations()

# =====================================================
# CARE ROUTINES
# =====================================================

with tab6:
    render_routines()

# =====================================================
# AUDIT & SECURITY
# =====================================================

with tab7:
    render_audit_dashboard()

# =====================================================
# MENTAL WELLNESS / CBT
# =====================================================

with tab8:
    render_cbt_tab()

# =====================================================
# PEDIATRICS
# =====================================================

with tab9:
    render_pediatrics()

# =====================================================
# DASHBOARD
# =====================================================

with tab10:
    render_dashboard()

# =====================================================
# IMAGING
# =====================================================

with tab11:
    render_imaging()

# =====================================================
# WEARABLES
# =====================================================

with tab12:
    render_wearables()

# =====================================================
# RESEARCH
# =====================================================

with tab13:
    render_research()