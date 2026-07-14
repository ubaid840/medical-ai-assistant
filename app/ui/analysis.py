import streamlit as st
from pathlib import Path

from image_ai import analyze_medical_image
from vector_store import add_document_to_db


def render_analysis():
    """
    Medical Analysis UI
    """

    st.markdown(
        """
        <div class="card">

        <h3>🩻 Medical Analysis</h3>

        Upload medical reports or medical images.

        <br><br>

        <b>Supported Files</b>

        <ul>
            <li>📄 PDF Reports</li>
            <li>🩻 X-Ray Images</li>
            <li>🧠 MRI Scans</li>
            <li>🩺 CT Scans</li>
            <li>🖼️ JPG / PNG Images</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_file = st.file_uploader(
        "Upload Medical Report or Image",
        type=[
            "pdf",
            "png",
            "jpg",
            "jpeg",
        ],
        key="medical_file",
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