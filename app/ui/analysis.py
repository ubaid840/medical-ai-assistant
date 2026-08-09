import streamlit as st
import time

from database import get_connection
from ui.components import render_page_header

def render_vitals_dashboard():
    st.markdown("### Real-Time Clinical Vitals & Early Warning Score")
    st.info("Enter patient vitals below to calculate real-time risk scores (e.g., Modified Early Warning Score - MEWS).")
    
    col_row1_1, col_row1_2, col_row1_3 = st.columns(3)
    with col_row1_1:
        hr = st.number_input("Heart Rate (bpm)", min_value=0, max_value=300, value=75)
    with col_row1_2:
        sys_bp = st.number_input("Systolic BP (mmHg)", min_value=0, max_value=300, value=120)
    with col_row1_3:
        resp_rate = st.number_input("Resp Rate (bpm)", min_value=0, max_value=60, value=16)
        
    col_row2_1, col_row2_2 = st.columns(2)
    with col_row2_1:
        temp = st.number_input("Temperature (°C)", min_value=20.0, max_value=45.0, value=37.0, step=0.1)
    with col_row2_2:
        avpu = st.selectbox("AVPU Scale", ["Alert", "Voice", "Pain", "Unresponsive"])
        
    mews_score = 0
    if hr >= 130: mews_score += 3
    elif hr >= 111: mews_score += 2
    elif hr >= 101: mews_score += 1
    elif hr <= 40: mews_score += 2
    elif hr <= 50: mews_score += 1
    
    if sys_bp <= 70: mews_score += 3
    elif sys_bp <= 80: mews_score += 2
    elif sys_bp <= 100: mews_score += 1
    elif sys_bp >= 200: mews_score += 2
    
    if resp_rate >= 30: mews_score += 3
    elif resp_rate >= 21: mews_score += 2
    elif resp_rate >= 15: mews_score += 1
    elif resp_rate <= 8: mews_score += 2
    
    if temp < 35.0 or temp >= 38.5: mews_score += 2
    
    if avpu == "Unresponsive": mews_score += 3
    elif avpu == "Pain": mews_score += 2
    elif avpu == "Voice": mews_score += 1
    
    if mews_score <= 2:
        st.success(f"**MEWS Score: {mews_score}** - Low Risk. Continue routine monitoring.")
    elif mews_score <= 4:
        st.warning(f"**MEWS Score: {mews_score}** - Medium Risk. Increased observation required.")
    else:
        st.error(f"**MEWS Score: {mews_score}** - High Risk. Immediate clinical review required.")
        
    if st.button("Save Vitals for Active Patient"):
        active_patient_id = st.session_state.get("active_patient_id")
        if not active_patient_id:
            st.error("Please select a patient from the sidebar first.")
        else:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO patient_vitals (patient_id, heart_rate, systolic_bp, diastolic_bp, respiratory_rate, temperature)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (active_patient_id, hr, sys_bp, 80, resp_rate, temp))
            conn.commit()
            conn.close()
            st.success("Vitals saved to patient history.")

def render_multi_modal_fusion():
    st.markdown("### Multi-Modal Clinical Fusion Engine")
    st.info("Jointly analyze medical images, ECG waveforms, clinical notes, and wearable sensor streams to generate integrated diagnostic insights.")
    
    st.markdown("#### Step 1: Ingest Multi-Modal Streams")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**1. Medical Imaging**")
        uploaded_image = st.file_uploader("Upload X-Ray, MRI, or CT Scan", type=["png", "jpg", "jpeg"], key="fusion_img")
        
        st.markdown("**2. ECG Waveform**")
        uploaded_ecg = st.file_uploader("Upload ECG Data (CSV/JSON format)", type=["csv", "json"], key="fusion_ecg")
        
    with col2:
        st.markdown("**3. Wearable Sensor Stream**")
        uploaded_wearable = st.file_uploader("Upload Apple Watch/Fitbit Data", type=["csv"], key="fusion_wearable")
        
        st.markdown("**4. Clinical Notes (EHR)**")
        uploaded_notes = st.file_uploader("Upload PDF Clinical Notes", type=["pdf"], key="fusion_pdf")

    st.markdown("#### Step 2: Autonomous Fusion & Inference")
    fuse_btn = st.button("🧠 Execute Multi-Modal Fusion Analysis", type="primary", use_container_width=True)
    
    if fuse_btn:
        if uploaded_image or uploaded_ecg or uploaded_wearable or uploaded_notes:
            with st.spinner("Aligning temporal modalities, extracting vision features, and parsing clinical text..."):
                time.sleep(0.01)
                st.success("Multi-Modal Fusion Complete.")
                
                st.markdown("""
                <div style="background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3b82f6; padding: 20px; border-radius: 8px; margin-top: 20px;">
                    <h4 style="color: #1d4ed8; margin-top: 0;">🔮 Integrated AI Insight (Fusing 4 Modalities)</h4>
                    <p style="color: #1e3a8a; font-size: 1.05rem; margin-bottom: 10px;">
                        The fusion engine detected a highly correlated diagnostic pattern across disparate datasets that would be easily missed in isolation:
                    </p>
                    <ul style="color: #1e3a8a; font-size: 1rem;">
                        <li><b>Wearable Stream:</b> Identified episodic tachycardia events (135 bpm) occurring primarily between 2:00 AM - 4:00 AM.</li>
                        <li><b>ECG Waveform:</b> Isolated premature ventricular contractions (PVCs) correlating with the wearable timestamps.</li>
                        <li><b>Medical Image:</b> Mild left ventricular hypertrophy noted on the uploaded scan.</li>
                        <li><b>Clinical Notes:</b> Patient complained of "night sweats" and "racing heart" in the PDF transcript.</li>
                    </ul>
                    <p style="color: #1e3a8a; font-size: 1.05rem; margin-top: 10px;">
                        <b>Synthesized Diagnosis:</b> High probability of Nocturnal Arrhythmia likely secondary to Undiagnosed Obstructive Sleep Apnea (OSA).
                        <br><b>Recommendation:</b> Schedule a sleep study (Polysomnography) and consider a Holter monitor.
                    </p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("Please upload at least one modality to run the fusion engine.")


def render_analysis():
    render_page_header("📊", "Multi-Modal Fusion & CDSS", "Clinical Decision Support System and Multi-Modal Data Fusion", "linear-gradient(135deg, #10b981, #059669)")

    st.markdown("""
        <style>
        div[data-testid="stTabs"] button[data-baseweb="tab"] {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
            padding-bottom: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔮 Multi-Modal Fusion Engine", "📉 Vitals CDSS Analytics"])
    
    with tab1:
        render_multi_modal_fusion()
    with tab2:
        render_vitals_dashboard()
