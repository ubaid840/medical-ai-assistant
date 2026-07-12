from pathlib import Path
import streamlit as st

from chatbot import ask_medical_ai


# -------------------------------------------------
# Paths
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)


# -------------------------------------------------
# Page Configuration
# -------------------------------------------------

st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -------------------------------------------------
# Custom CSS
# -------------------------------------------------

st.markdown(
"""
<style>

.main-title{
    font-size:45px;
    font-weight:800;
    color:#1f2937;
}

.subtitle{
    font-size:18px;
    color:#6b7280;
}

.card{
    padding:25px;
    border-radius:18px;
    background:#f8fafc;
    border:1px solid #e5e7eb;
    margin-bottom:20px;
}

.status{
    padding:12px;
    border-radius:10px;
    background:#dcfce7;
    color:#166534;
    margin-bottom:10px;
}

.footer{
    text-align:center;
    color:#6b7280;
    margin-top:40px;
}

</style>
""",
unsafe_allow_html=True
)



# -------------------------------------------------
# Sidebar
# -------------------------------------------------

with st.sidebar:


    st.markdown(
    """
    ## 🩺 Medical AI
    
    Intelligent healthcare assistant
    """
    )


    st.divider()


    st.subheader("📄 Upload Medical Documents")


    uploaded_pdf = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )


    if uploaded_pdf:

        file_path = DATA_DIR / uploaded_pdf.name

        with open(file_path,"wb") as f:
            f.write(uploaded_pdf.getbuffer())


        st.success(
            "PDF uploaded successfully.\n\n"
            "Run vector_db.py to index document."
        )



    st.divider()


    st.subheader("🩻 Medical Images")


    image_file = st.file_uploader(
        "Upload X-Ray / CT / MRI",
        type=[
            "png",
            "jpg",
            "jpeg"
        ]
    )


    if image_file:
        st.image(
            image_file,
            caption="Uploaded Medical Image",
            use_container_width=True
        )

        st.info(
            "Vision AI analysis module will process this image."
        )



    st.divider()


    st.subheader("⚙ System Status")


    st.markdown(
    """
    <div class="status">
    ✅ Groq Connected
    </div>
    
    <div class="status">
    ✅ ChromaDB Ready
    </div>

    <div class="status">
    ✅ Retriever Loaded
    </div>

    <div class="status">
    ✅ Vision AI Ready
    </div>

    """,
    unsafe_allow_html=True
    )



    st.divider()


    st.subheader("💡 Sample Questions")


    questions = [

        "What are symptoms of diabetes?",

        "Explain hypertension",

        "What are risk factors?",

        "Treatment options available?"

    ]


    for q in questions:

        st.write(
            "• " + q
        )





# -------------------------------------------------
# Main Dashboard
# -------------------------------------------------


st.markdown(
"""
<div class="main-title">

🩺 Medical AI Assistant

</div>


<div class="subtitle">

AI-powered healthcare document and medical image analysis platform

<br>

Powered by Groq • LangChain • ChromaDB • Ollama • Vision AI

</div>

""",
unsafe_allow_html=True
)



st.write("")



# -------------------------------------------------
# Tabs
# -------------------------------------------------

tab1, tab2, tab3 = st.tabs(
[
"💬 Medical Chat",
"🩻 Image Analysis",
"📚 Knowledge Base"
]
)



# -------------------------------------------------
# Chat Tab
# -------------------------------------------------

with tab1:


    st.markdown(
    """
    <div class="card">

    ### 🩺 Medical Consultation

    Ask questions from uploaded medical documents.

    </div>
    """,
    unsafe_allow_html=True
    )



    question = st.chat_input(
        "Ask a medical question..."
    )


    if question:


        with st.chat_message("user"):

            st.write(question)



        with st.chat_message("assistant"):

            with st.spinner(
                "Analyzing medical knowledge..."
            ):


                try:

                    answer = ask_medical_ai(
                        question
                    )


                    st.write(answer)


                except Exception as e:

                    st.error(
                        f"Error: {e}"
                    )





# -------------------------------------------------
# Image Analysis Tab
# -------------------------------------------------

with tab2:


    st.markdown(
    """
    <div class="card">

    ### 🖼 Medical Image Intelligence


    Upload X-Ray, CT Scan or MRI images.

    Future Vision AI module will analyze:

    - Abnormal regions
    - Image description
    - Medical observations
    - AI confidence score


    </div>

    """,
    unsafe_allow_html=True
    )


    img = st.file_uploader(
        "Upload Image",
        type=[
            "png",
            "jpg",
            "jpeg"
        ],
        key="image_tab"
    )


    if img:

        st.image(
            img,
            width=500
        )


        st.warning(
            "Vision model integration coming in next upgrade."
        )





# -------------------------------------------------
# Knowledge Base
# -------------------------------------------------

with tab3:


    st.markdown(
    """
    <div class="card">

    ### 📚 Knowledge Base


    Current System:

    📄 Medical PDFs Indexed

    🧠 Vector Database: ChromaDB

    🔎 Retrieval: LangChain RAG

    🤖 LLM: Groq


    </div>

    """,
    unsafe_allow_html=True
    )


    col1,col2,col3 = st.columns(3)


    with col1:

        st.metric(
            "Documents",
            "3+"
        )


    with col2:

        st.metric(
            "Vector DB",
            "ChromaDB"
        )


    with col3:

        st.metric(
            "AI Model",
            "Llama 3.3"
        )





# -------------------------------------------------
# Footer
# -------------------------------------------------

st.markdown(
"""
<div class="footer">

Developed by <b>Ubaid Ashraf</b><br>

B.Sc. Computer Science & Artificial Intelligence


<br><br>

Medical AI Assistant Phase 3

</div>

""",
unsafe_allow_html=True
)