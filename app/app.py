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
from ui.aiims_network import render_aiims_network
from ui.voice_scribe import render_voice_scribe
from ui.lab_ocr import render_lab_ocr
from ui.surgical_sim import render_surgical_sim
from ui.outbreak_sim import render_outbreak_sim
from ui.bci import render_bci_dashboard
from ui.nanobots import render_nanobot_controller

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

if st.session_state.get("privacy_mode", False):
    st.markdown("""
        <div style="background-color: #ecfdf5; border: 1px solid #10b981; color: #065f46; padding: 12px; border-radius: 12px; margin-bottom: 25px; display: flex; align-items: center; justify-content: center; gap: 10px; box-shadow: 0 4px 6px rgba(16,185,129,0.1);">
            <span style="font-size: 22px;">🔒</span>
            <span style="font-weight: 700; font-size: 1.05rem;">HIPAA Compliant / Zero-Trust Active: All Protected Health Information (PHI) is automatically masked and processed locally.</span>
        </div>
    """, unsafe_allow_html=True)

if st.session_state.get("elderly_mode", False):
    st.markdown("""
        <style>
        /* Elderly Accessibility Mode: High Contrast & Large Text */
        html, body, p, span, div, li, a, h1, h2, h3, h4, h5, h6 {
            font-size: 1.25rem !important; /* Base scale up */
            color: #000000 !important; /* Max contrast */
        }
        [data-testid="stSidebar"] {
            background-color: #ffffff !important;
            border-right: 3px solid #000000 !important;
        }
        .stButton>button {
            border: 2px solid #000000 !important;
            font-weight: 900 !important;
            color: #000000 !important;
            background-color: #fde047 !important; /* High contrast yellow */
        }
        .stButton>button:hover {
            background-color: #000000 !important;
            color: #fde047 !important;
        }
        /* Make inputs more visible */
        input, textarea, select {
            border: 2px solid #000000 !important;
            background-color: #ffffff !important;
            color: #000000 !important;
        }
        </style>
    """, unsafe_allow_html=True)



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
# NAVIGATION ROUTING
# =====================================================

st.divider()

selected_page = st.session_state.get("selected_page", "🩺 Chat")

if selected_page == "🩺 Chat":
    render_chat(session_id=st.session_state.session_id)
elif selected_page == "🏥 AIIMS":
    render_aiims_network()
elif selected_page == "🌍 Planetary":
    render_planetary_dashboard()
elif selected_page == "🕸️ Graph":
    render_knowledge_graph()
elif selected_page == "🌌 UHDT-PCSE":
    render_prediction_dashboard()
elif selected_page == "🧪 Diagnostics":
    render_advanced_diagnostics()
elif selected_page == "🏥 Hospital":
    render_hospital()
elif selected_page == "🔬 Analysis":
    render_analysis()
elif selected_page == "💊 Pharmacology":
    render_pharmacology()
elif selected_page == "🧠 Knowledge":
    render_knowledge_base()
elif selected_page == "📋 Intake":
    render_operations()
elif selected_page == "💉 Routines":
    render_routines()
elif selected_page == "⚕️ Audit":
    render_audit_dashboard()
elif selected_page == "🫁 Wellness":
    render_cbt_tab()
elif selected_page == "👶 Pediatrics":
    render_pediatrics()
elif selected_page == "🫀 Dashboard":
    render_dashboard()
elif selected_page == "🩻 Imaging":
    render_imaging()
elif selected_page == "⌚ Wearables":
    render_wearables()
elif selected_page == "🧫 Research":
    render_research()
elif selected_page == "🎙️ Voice Scribe":
    render_voice_scribe()
elif selected_page == "📄 Lab OCR":
    render_lab_ocr()
elif selected_page == "🔪 Surgical Sim":
    render_surgical_sim()
elif selected_page == "🦠 Outbreak Sim":
    render_outbreak_sim()
elif selected_page == "🧠 Neural BCI":
    render_bci_dashboard()
elif selected_page == "🦠 Nanobots":
    render_nanobot_controller()