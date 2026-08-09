import streamlit as st
import time
import pandas as pd

def render_lab_ocr():
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #10b981, #059669); border-radius: 20px; color: white; margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);">
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">📄 Intelligent Lab Report OCR</h1>
            <p style="margin-top: 10px; font-size: 1.1rem; opacity: 0.9;">Extract and structure biomarker data from raw medical PDFs.</p>
        </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Lab Report (PDF or Image)", type=["pdf", "png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        with st.spinner("Running Vision LLM OCR and structuring data..."):
            time.sleep(0.01) # Simulate processing
            
        st.success("Extraction Complete!")
        
        st.markdown("### Extracted Biomarkers")
        
        data = {
            "Biomarker": ["Hemoglobin", "WBC Count", "Platelets", "Creatinine", "Glucose (Fasting)", "Cholesterol (Total)"],
            "Value": ["11.2", "12,500", "250,000", "1.4", "126", "240"],
            "Unit": ["g/dL", "/mcL", "/mcL", "mg/dL", "mg/dL", "mg/dL"],
            "Reference Range": ["12.0 - 15.5", "4,500 - 11,000", "150,000 - 450,000", "0.6 - 1.1", "70 - 99", "< 200"],
            "Status": ["Low ⚠️", "High 🚨", "Normal ✅", "High 🚨", "High 🚨", "High 🚨"]
        }
        
        df = pd.DataFrame(data)
        
        def highlight_status(val):
            if '🚨' in str(val):
                return 'background-color: rgba(239, 68, 68, 0.2); color: #ef4444; font-weight: bold;'
            elif '⚠️' in str(val):
                return 'background-color: rgba(245, 158, 11, 0.2); color: #f59e0b; font-weight: bold;'
            elif '✅' in str(val):
                return 'background-color: rgba(16, 185, 129, 0.2); color: #10b981;'
            return ''

        styled_df = df.style.map(highlight_status, subset=['Status'])
        
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        st.markdown("### 🤖 Clinical Interpretation")
        st.info("**AI Synthesis:** The patient exhibits mild anemia (low hemoglobin) paired with leukocytosis (elevated WBC) and impaired renal function (elevated creatinine). Fasting glucose and total cholesterol are also elevated, suggesting metabolic syndrome or undiagnosed diabetes. **Recommendation:** Evaluate for acute infection/inflammation and consider HbA1c testing.")
