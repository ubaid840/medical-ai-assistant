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
from ui.prediction import render_prediction_dashboard
from ui.advanced_diagnostics import render_advanced_diagnostics
from ui.hospital import render_hospital
from ui.research import render_research
from ui.planetary import render_planetary_dashboard
from ui.knowledge_graph import render_knowledge_graph


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
padding-top: 3.5rem; 
padding-bottom: 3.5rem; 
margin-bottom: 2.5rem;
border-radius: 28px;
background: rgba(255, 255, 255, 0.6);
backdrop-filter: blur(20px);
-webkit-backdrop-filter: blur(20px);
box-shadow: 0 25px 50px -12px rgba(14, 165, 233, 0.15), inset 0 1px 0 rgba(255,255,255,0.8);
border: 1px solid rgba(255, 255, 255, 0.8);
">
    <!-- Animated EKG Background -->
    <svg viewBox="0 0 1000 200" preserveAspectRatio="none" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.12; z-index: 0; pointer-events: none;">
        <path class="ekg-line" d="M0,100 L250,100 L270,70 L290,140 L320,30 L350,170 L370,80 L390,100 L700,100 L720,70 L740,140 L770,30 L800,170 L820,80 L840,100 L1000,100" fill="none" stroke="#0ea5e9" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>

<!-- Medical Plus Symbols -->
<div style="position: absolute; top: 30px; left: 30px; color: #ef4444; font-size: 2.5rem; font-weight: bold; line-height: 1; opacity: 0.4; z-index: 1;">+</div>
<div style="position: absolute; top: 30px; right: 30px; color: #ef4444; font-size: 2.5rem; font-weight: bold; line-height: 1; opacity: 0.4; z-index: 1;">+</div>
<div style="position: absolute; bottom: 30px; left: 40px; color: #ef4444; font-size: 1.5rem; font-weight: bold; line-height: 1; opacity: 0.4; z-index: 1;">+</div>

<div style="position: relative; z-index: 1;">
<div style="position: relative; display: inline-flex; justify-content: center; align-items: center; margin-bottom: 1.8rem;">
<div style="position: absolute; width: 140px; height: 140px; background: radial-gradient(circle, rgba(14,165,233,0.2) 0%, rgba(255,255,255,0) 70%); border-radius: 50%;"></div>
<div style="display: inline-flex; align-items: center; justify-content: center; width: 88px; height: 88px; border-radius: 28px; background: linear-gradient(135deg, #0ea5e9, #4f46e5); box-shadow: 0 15px 35px rgba(14, 165, 233, 0.4), inset 0 2px 4px rgba(255,255,255,0.3); z-index: 1;">
<span style="font-size: 46px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2)); color: white;">🩺</span>
</div>
</div>
<h1 style="font-size: 3.8rem; font-weight: 900; margin: 0 0 12px 0; background: linear-gradient(135deg, #0f172a, #3b82f6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: -1.5px; line-height: 1.1; text-shadow: 0 10px 30px rgba(14,165,233,0.1);">
Medical AI Assistant
</h1>
<p style="font-size: 1.25rem; color: #475569; margin-top: 0; font-weight: 600; letter-spacing: 0.2px;">
Advanced Clinical Intelligence & Diagnostic Analysis
</p>
<div style="margin-top: 1.8rem; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
<span style="background: rgba(255,255,255,0.7); backdrop-filter: blur(5px); color: #0f172a; padding: 8px 18px; border-radius: 30px; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid rgba(255,255,255,0.8);">⚡ Groq AI</span>
<span style="background: rgba(255,255,255,0.7); backdrop-filter: blur(5px); color: #0f172a; padding: 8px 18px; border-radius: 30px; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid rgba(255,255,255,0.8);">🔗 LangChain</span>
<span style="background: rgba(255,255,255,0.7); backdrop-filter: blur(5px); color: #0f172a; padding: 8px 18px; border-radius: 30px; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid rgba(255,255,255,0.8);">🗄️ ChromaDB</span>
<span style="background: rgba(255,255,255,0.7); backdrop-filter: blur(5px); color: #0f172a; padding: 8px 18px; border-radius: 30px; font-size: 0.75rem; font-weight: 800; letter-spacing: 0.8px; text-transform: uppercase; box-shadow: 0 4px 15px rgba(0,0,0,0.05); border: 1px solid rgba(255,255,255,0.8);">🦙 Ollama</span>
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

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10, tab11, tab12, tab13, tab14, tab15, tab16, tab17, tab18 = st.tabs(
    [
        "🩺 Chat",
        "｜ 🌍 Planetary",
        "｜ 🕸️ Graph",
        "｜ 🌌 UHDT-PCSE",
        "｜ 🧪 Diagnostics",
        "｜ 🏥 Hospital",
        "｜ 🔬 Analysis",
        "｜ 💊 Pharmacology",
        "｜ 🧠 Knowledge",
        "｜ 📋 Intake",
        "｜ 💉 Routines",
        "｜ ⚕️ Audit",
        "｜ 🫁 Wellness",
        "｜ 👶 Pediatrics",
        "｜ 🫀 Dashboard",
        "｜ 🩻 Imaging",
        "｜ ⌚ Wearables",
        "｜ 🧫 Research"
    ]
)



# =====================================================
# CHAT
# =====================================================

with tab1:
    render_chat(session_id=st.session_state.session_id)

with tab2:
    render_planetary_dashboard()

with tab3:
    render_knowledge_graph()

with tab4:
    render_prediction_dashboard()

with tab5:
    render_advanced_diagnostics()

with tab6:
    render_hospital()

with tab7:
    render_analysis()

with tab8:
    render_pharmacology()

with tab9:
    render_knowledge_base()

with tab10:
    render_operations()

with tab11:
    render_routines()

with tab12:
    render_audit_dashboard()

with tab13:
    render_cbt_tab()

with tab14:
    render_pediatrics()

with tab15:
    render_dashboard()

with tab16:
    render_imaging()

with tab17:
    render_wearables()

with tab18:
    render_research()