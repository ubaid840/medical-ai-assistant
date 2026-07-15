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

    # ---------------- Interactive Dashboard ---------------- #
    with st.expander("📈 View Patient Vitals Dashboard", expanded=True):
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