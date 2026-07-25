import streamlit as st
import numpy as np

def render_imaging():
    st.markdown("""
        <div style='background: white; padding: 25px 30px; border-radius: 16px; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); border: 1px solid #f1f5f9; margin-bottom: 20px;'>
            <div style='display: flex; align-items: center; gap: 15px; margin-bottom: 8px;'>
                <div style='background: linear-gradient(135deg, #e0e7ff, #c7d2fe); color: #4f46e5; padding: 10px; border-radius: 12px; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);'>
                    <span style='font-size: 24px;'>🩻</span>
                </div>
                <h3 style='color: #0f172a; font-weight: 800; font-size: 1.7rem; margin: 0;'>Advanced DICOM Viewer</h3>
            </div>
            <p style='color: #64748b; font-size: 1.1rem; margin-top: 5px; margin-bottom: 0;'>Upload and visualize high-resolution medical imaging (DICOM) files.</p>
        </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload DICOM File (.dcm)", type=["dcm"])
    
    if uploaded_file is not None:
        try:
            import pydicom
            from pydicom.filebase import DicomBytesIO
            
            raw_bytes = uploaded_file.read()
            dicom_file = DicomBytesIO(raw_bytes)
            ds = pydicom.dcmread(dicom_file)
            
            col1, col2 = st.columns([0.6, 0.4])
            
            with col1:
                st.markdown("### 🖼️ Image Viewer")
                # Normalize pixel array for display
                image_2d = ds.pixel_array.astype(float)
                image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0
                image_2d_scaled = np.uint8(image_2d_scaled)
                
                st.image(image_2d_scaled, caption=f"Modality: {ds.get('Modality', 'Unknown')}", use_container_width=True, clamp=True)
                
            with col2:
                st.markdown("### 📋 Patient Metadata")
                metadata = {
                    "Patient ID": ds.get('PatientID', 'N/A'),
                    "Patient Name": str(ds.get('PatientName', 'N/A')),
                    "Study Date": ds.get('StudyDate', 'N/A'),
                    "Modality": ds.get('Modality', 'N/A'),
                    "Body Part": ds.get('BodyPartExamined', 'N/A'),
                    "Manufacturer": ds.get('Manufacturer', 'N/A')
                }
                st.json(metadata)
                
                with st.expander("🤖 AI Image Analysis", expanded=True):
                    st.write("Generate a simulated radiologist report based on the uploaded scan type.")
                    if st.button("Generate Radiology Report", use_container_width=True):
                        with st.spinner("Analyzing scan..."):
                            from chatbot import ask_medical_ai
                            prompt = f"Act as an expert Radiologist. The user has uploaded a {ds.get('Modality', 'medical scan')} of the {ds.get('BodyPartExamined', 'patient')}. Provide a simulated detailed mock radiology report outlining standard things you would look for and what a normal vs abnormal scan looks like."
                            response = ask_medical_ai(prompt, "radiologist_agent")
                            st.write_stream(response.get("answer_generator", ["Error"]))
        except Exception as e:
            st.error(f"Error reading DICOM file. Please ensure it is a valid .dcm file. Details: {e}")
