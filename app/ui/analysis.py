import streamlit as st
from pathlib import Path
import plotly.express as px
import pandas as pd
import numpy as np

from image_ai import analyze_medical_image
from vector_store import add_document_to_db


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

    # ---------------- CDSS / Risk Prediction ---------------- #
    with st.expander("⚕️ Clinical Decision Support System (CDSS) - Risk Analytics", expanded=True):
        st.markdown("Enter patient vitals below to calculate real-time risk scores (e.g., Modified Early Warning Score - MEWS).")
        
        col_v1, col_v2, col_v3, col_v4 = st.columns(4)
        with col_v1:
            hr = st.number_input("Heart Rate (bpm)", min_value=0, max_value=300, value=75)
        with col_v2:
            sys_bp = st.number_input("Systolic BP (mmHg)", min_value=0, max_value=300, value=120)
        with col_v3:
            resp_rate = st.number_input("Resp Rate (bpm)", min_value=0, max_value=60, value=16)
        with col_v4:
            temp = st.number_input("Temperature (°C)", min_value=20.0, max_value=45.0, value=37.0, step=0.1)

        col_v5, col_v6 = st.columns(2)
        with col_v5:
            avpu = st.selectbox("Level of Consciousness (AVPU)", ["Alert", "Voice (Reacts to)", "Pain (Reacts to)", "Unresponsive"])
            
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
        
        st.markdown("### Risk Assessment")
        if mews_score <= 2:
            st.success(f"**MEWS Score: {mews_score}** - Low Risk. Continue routine monitoring.")
        elif mews_score <= 4:
            st.warning(f"**MEWS Score: {mews_score}** - Medium Risk. Increased observation required.")
        else:
            st.error(f"**MEWS Score: {mews_score}** - High Risk. Immediate clinical review required.")
            
        # Sepsis SIRS Criteria check (simplified)
        sirs_criteria = 0
        if hr > 90: sirs_criteria += 1
        if resp_rate > 20: sirs_criteria += 1
        if temp < 36.0 or temp > 38.0: sirs_criteria += 1
        
        if sirs_criteria >= 2:
            st.error(f"⚠️ **SIRS Alert:** Patient meets {sirs_criteria} SIRS criteria. Evaluate for potential infection/sepsis.")

    # ---------------- Interactive Dashboard ---------------- #
    with st.expander("📈 View Patient Vitals Dashboard", expanded=False):
        # Generate some mock data for the fabulous dashboard
        dates = pd.date_range(end=pd.Timestamp.today(), periods=30)
        heart_rate = np.random.normal(75, 5, size=30)
        blood_pressure_sys = np.random.normal(120, 8, size=30)
        
        df = pd.DataFrame({
            'Date': dates,
            'Heart Rate (bpm)': heart_rate,
            'Systolic BP': blood_pressure_sys
        })
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.line(df, x='Date', y='Heart Rate (bpm)', title='Heart Rate Trend', 
                           color_discrete_sequence=['#ff4b4b'])
            fig1.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig1, use_container_width=True)
            
        with col2:
            fig2 = px.bar(df, x='Date', y='Systolic BP', title='Blood Pressure (Systolic)',
                          color_discrete_sequence=['#0ea5e9'])
            fig2.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig2, use_container_width=True)

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
        return

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

        st.image(
            uploaded_file,
            use_container_width=True,
        )

        if st.button("Analyze Image"):
            with st.spinner(f"Analyzing {scan_type} with Vision AI..."):
                try:
                    uploaded_file.seek(0)
                    analysis = analyze_medical_image(uploaded_file, scan_type=scan_type)
                    st.markdown("### 🤖 AI Findings")
                    st.info(analysis)
                except Exception as e:
                    st.error(f"Failed to analyze image: {e}")