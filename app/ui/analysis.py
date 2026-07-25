import streamlit as st
from pathlib import Path
import plotly.express as px
import pandas as pd
import numpy as np

from image_ai import analyze_medical_image
from vector_store import add_document_to_db
from database import get_connection


def render_analysis():
    """
    Medical Analysis UI
    """

    st.markdown(
        """
        <div class="card">
        <h3>🩻 Medical Analysis & Dashboards</h3>
        <p>Upload medical reports or medical images below, or view patient analytics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================
    # 1. FILE UPLOAD & IMAGE ANALYSIS
    # =====================================================

    uploaded_file = st.file_uploader(
        "Upload Medical Report or Image",
        type=["pdf", "png", "jpg", "jpeg"],
        key="medical_file",
        label_visibility="collapsed"
    )

    st.markdown(
        """
        <div style="font-size: 14px; color: gray; margin-bottom: 20px;">
        <b>Supported Files:</b> 📄 PDF Reports &nbsp;|&nbsp; 🩻 X-Ray Images &nbsp;|&nbsp; 🧠 MRI Scans &nbsp;|&nbsp; 🩺 CT Scans &nbsp;|&nbsp; 🖼️ JPG / PNG Images
        </div>
        """,
        unsafe_allow_html=True
    )

    if uploaded_file is None:
        st.info("Upload a medical file to begin.")
    else:
        extension = uploaded_file.name.split(".")[-1].lower()

        # ---------------- PDF ---------------- #
        if extension == "pdf":
            st.success("📄 Medical PDF Uploaded")
            st.write(f"**File:** {uploaded_file.name}")
            with st.spinner("Indexing PDF into Knowledge Base..."):
                try:
                    data_dir = Path(__file__).resolve().parent.parent / "data"
                    data_dir.mkdir(exist_ok=True, parents=True)
                    file_path = data_dir / uploaded_file.name
                    
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    add_document_to_db(file_path)
                    st.success("✅ Document indexed successfully! You can now ask questions about it in the Medical Chat tab.")
                except Exception as e:
                    st.error(f"Failed to index PDF: {e}")

        # ---------------- Images ---------------- #
        else:
            st.success("🩻 Medical Image Uploaded")
            scan_type = st.selectbox(
                "Select Scan Type for Analysis",
                ["General Medical Image", "X-Ray", "MRI Scan", "CT Scan"]
            )
            st.image(uploaded_file, use_container_width=True)
            if st.button("Analyze Image"):
                with st.spinner(f"Analyzing {scan_type} with Vision AI..."):
                    try:
                        uploaded_file.seek(0)
                        analysis = analyze_medical_image(uploaded_file, scan_type=scan_type)
                        st.markdown("### 🤖 AI Findings")
                        st.info(analysis)
                    except Exception as e:
                        st.error(f"Failed to analyze image: {e}")

    # =====================================================
    # 2. CDSS / RISK PREDICTION
    # =====================================================
    st.markdown("<br><hr style='border: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: white; padding: 25px 30px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025); border: 1px solid #f1f5f9; margin-bottom: 25px;'>
            <div style='display: flex; align-items: center; gap: 15px; margin-bottom: 8px;'>
                <div style='background: linear-gradient(135deg, #fee2e2, #fca5a5); color: #b91c1c; padding: 10px; border-radius: 12px; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);'>
                    <span style='font-size: 24px;'>⚕️</span>
                </div>
                <h3 style='color: #0f172a; font-weight: 800; font-size: 1.7rem; margin: 0;'>Clinical Decision Support System</h3>
            </div>
            <p style='color: #64748b; font-size: 1.1rem; margin-top: 5px; margin-bottom: 0;'>Calculate real-time risk scores (MEWS) based on patient vitals.</p>
        </div>
    """, unsafe_allow_html=True)
    
    col_v1, col_v2, col_v3, col_v4 = st.columns(4)
    with col_v1:
        hr = st.number_input("Heart Rate (bpm)", min_value=0, max_value=300, value=75)
    with col_v2:
        sys_bp = st.number_input("Systolic BP (mmHg)", min_value=0, max_value=300, value=120)
    with col_v3:
        resp_rate = st.number_input("Resp Rate (bpm)", min_value=0, max_value=60, value=16)
    with col_v4:
        temp = st.number_input("Temperature (°C)", min_value=20.0, max_value=45.0, value=37.0, step=0.1)

    col_v5, col_v6 = st.columns([0.5, 0.5])
    with col_v5:
        avpu = st.selectbox("Level of Consciousness", ["Alert", "Voice (Reacts to)", "Pain (Reacts to)", "Unresponsive"])
    with col_v6:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save Vitals for Active Patient", use_container_width=True):
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
                st.toast("✅ Vitals saved to patient history.")

    mews_score = 0
    # Calculate MEWS (Simplified)
    if hr <= 40 or hr >= 130: mews_score += 3
    elif hr >= 111: mews_score += 2
    elif hr <= 50 or hr >= 101: mews_score += 1
    
    if sys_bp <= 70: mews_score += 3
    elif sys_bp <= 80: mews_score += 2
    elif sys_bp <= 100 or sys_bp >= 200: mews_score += 1
    
    if resp_rate <= 8 or resp_rate >= 30: mews_score += 3
    elif resp_rate >= 21: mews_score += 2
    elif resp_rate >= 15: mews_score += 1
    
    if temp <= 35.0 or temp >= 38.5: mews_score += 2
    
    if avpu == "Unresponsive" or avpu == "Pain (Reacts to)": mews_score += 3
    elif avpu == "Voice (Reacts to)": mews_score += 1

    st.markdown("<h4 style='color: #0f172a; font-weight: 700; margin-top: 15px; margin-bottom: 10px;'>📊 Real-time Risk Assessment</h4>", unsafe_allow_html=True)
    if mews_score <= 2:
        st.success(f"**MEWS Score: {mews_score}** — Low Risk. Continue routine monitoring.", icon="✅")
    elif mews_score <= 4:
        st.warning(f"**MEWS Score: {mews_score}** — Medium Risk. Increased observation required.", icon="⚠️")
    else:
        st.error(f"**MEWS Score: {mews_score}** — High Risk. Immediate clinical review required.", icon="🚨")

    # ---------------- Multi-Agent Case Conference ---------------- #
    st.markdown("<br><hr style='border: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background: white; padding: 25px 30px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05), 0 4px 6px -2px rgba(0, 0, 0, 0.025); border: 1px solid #f1f5f9; margin-bottom: 20px;'>
            <div style='display: flex; align-items: center; gap: 15px; margin-bottom: 8px;'>
                <div style='background: linear-gradient(135deg, #f3e8ff, #d8b4fe); color: #7e22ce; padding: 10px; border-radius: 12px; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);'>
                    <span style='font-size: 24px;'>🕵️</span>
                </div>
                <h3 style='color: #0f172a; font-weight: 800; font-size: 1.7rem; margin: 0;'>Multi-Agent Case Conference</h3>
            </div>
            <p style='color: #64748b; font-size: 1.1rem; margin-top: 5px; margin-bottom: 0;'>Submit a complex medical case. Three specialized AI agents will debate the diagnosis live.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h4 style='color: #334155; font-size: 1.1rem; margin-bottom: -40px; font-weight: 600;'>📋 Patient Case / Symptoms</h4>", unsafe_allow_html=True)
    mystery_case = st.text_area(
        "", 
        placeholder="e.g. 45yo male with recurring syncope, elevated troponin, but normal ECG...\n\n(Type the case details here...)",
        height=160
    )
    
    col_d_empty, col_d_btn = st.columns([0.7, 0.3])
    with col_d_btn:
        start_btn = st.button("Start AI Conference 🎙️", use_container_width=True, type="primary")

    if start_btn:
        if not mystery_case.strip():
            st.warning("Please enter a case.")
        else:
            from chatbot import ask_medical_ai
            
            col_d1, col_d2, col_d3 = st.columns(3)
            
            with col_d1:
                st.markdown("### 🩺 Lead Diagnostician")
                with st.spinner("Analyzing..."):
                    diag_resp = ask_medical_ai(f"Act as a Lead Diagnostician. Provide initial differential diagnosis for: {mystery_case}", "diag_agent")
                    st.write_stream(diag_resp.get("answer_generator", ["Error"]))
                    
            with col_d2:
                st.markdown("### 💊 Clinical Pharmacologist")
                with st.spinner("Reviewing..."):
                    pharm_resp = ask_medical_ai(f"Act as a Clinical Pharmacologist. Review this case focusing on toxicological, drug-induced, or metabolic causes: {mystery_case}", "pharm_agent")
                    st.write_stream(pharm_resp.get("answer_generator", ["Error"]))

            with col_d3:
                st.markdown("### 🧬 Specialist Consultant")
                with st.spinner("Debating..."):
                    spec_resp = ask_medical_ai(f"Act as a critical Specialist. Challenge the typical diagnoses and offer alternative rare or overlooked diagnoses for: {mystery_case}", "spec_agent")
                    st.write_stream(spec_resp.get("answer_generator", ["Error"]))