import streamlit as st
import numpy as np

def render_imaging():
    st.markdown("""
        <div style="
        background: linear-gradient(135deg, #6366f1 0%, #4338ca 100%);
        border-radius: 20px;
        padding: 35px 30px;
        color: white;
        box-shadow: 0 20px 40px -10px rgba(99, 102, 241, 0.4);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.2);
        ">
        <div style="position: absolute; top: -50px; right: -50px; width: 250px; height: 250px; background: rgba(255,255,255,0.1); border-radius: 50%; filter: blur(30px); pointer-events: none;"></div>
        <div style="position: absolute; bottom: -80px; left: 10%; width: 200px; height: 200px; background: rgba(255,255,255,0.15); border-radius: 50%; filter: blur(25px); pointer-events: none;"></div>

        <div style="display: flex; align-items: center; gap: 25px; position: relative; z-index: 1;">
        <div style="background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); width: 80px; height: 80px; border-radius: 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.4);">
        <span style="font-size: 40px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));">🦴</span>
        </div>
        <div>
        <h2 style="margin: 0; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.15);">Advanced DICOM Viewer</h2>
        <p style="margin: 8px 0 0 0; font-size: 1.1rem; opacity: 0.95; font-weight: 500; letter-spacing: 0.2px;">Upload and visualize high-resolution medical imaging (DICOM) files.</p>
        </div>
        </div>
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
                st.markdown(
                    """
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                        <div style="background: linear-gradient(135deg, #818cf8, #4f46e5); color: white; width: 48px; height: 48px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 24px; box-shadow: 0 4px 10px rgba(79,70,229,0.3);">
                            🖼️
                        </div>
                        <h3 style="margin: 0; font-weight: 800; color: #0f172a; font-size: 1.5rem; letter-spacing: -0.5px;">Image Viewer</h3>
                    </div>
                    """, unsafe_allow_html=True
                )
                # Normalize pixel array for display
                image_2d = ds.pixel_array.astype(float)
                image_2d_scaled = (np.maximum(image_2d,0) / image_2d.max()) * 255.0
                image_2d_scaled = np.uint8(image_2d_scaled)
                
                st.image(image_2d_scaled, caption=f"Modality: {ds.get('Modality', 'Unknown')}", use_container_width=True, clamp=True)
                
            with col2:
                st.markdown(
                    """
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 20px;">
                        <div style="background: linear-gradient(135deg, #34d399, #059669); color: white; width: 48px; height: 48px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 24px; box-shadow: 0 4px 10px rgba(5,150,105,0.3);">
                            📋
                        </div>
                        <h3 style="margin: 0; font-weight: 800; color: #0f172a; font-size: 1.5rem; letter-spacing: -0.5px;">Patient Metadata</h3>
                    </div>
                    """, unsafe_allow_html=True
                )
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
