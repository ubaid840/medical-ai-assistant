import streamlit as st


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

        st.info(
            """
PDF analysis module is ready.

Future versions will automatically:

• Extract text
• OCR scanned PDFs
• Create embeddings
• Add to the Knowledge Base
• Enable Medical Chat immediately
"""
        )

    # ---------------- Images ---------------- #

    else:

        st.success("🩻 Medical Image Uploaded")

        st.image(
            uploaded_file,
            use_container_width=True,
        )

        st.info(
            """
Vision AI module will support:

• Chest X-Ray Analysis
• CT Scan Analysis
• MRI Analysis
• Ultrasound Analysis
• Medical Image Captioning
• AI-assisted Findings
"""
        )

    st.divider()

    st.subheader("🚀 Upcoming Features")

    col1, col2 = st.columns(2)

    with col1:
        st.checkbox("Automatic PDF Indexing", value=False, disabled=True)
        st.checkbox("OCR for Scanned Reports", value=False, disabled=True)
        st.checkbox("Blood Report Analysis", value=False, disabled=True)

    with col2:
        st.checkbox("X-Ray AI", value=False, disabled=True)
        st.checkbox("MRI AI", value=False, disabled=True)
        st.checkbox("CT Scan AI", value=False, disabled=True)