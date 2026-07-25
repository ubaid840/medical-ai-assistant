import streamlit as st
import os
import requests
from streamlit_lottie import st_lottie

def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

from config import (
    DATA_DIR,
    EMBEDDING_MODEL,
    LLM_MODEL,
    TOP_K
)

from memory import clear_history, get_session_history
from chat_history import get_all_sessions, create_session, delete_session, cleanup_empty_sessions


def render_sidebar(session_id=None):

    st.sidebar.markdown(
        """
<style>
.ekg-line-sidebar {
    stroke-dasharray: 2000;
    stroke-dashoffset: 2000;
    animation: draw-ekg-sidebar 6s infinite linear;
}
@keyframes draw-ekg-sidebar {
    0% { stroke-dashoffset: 2000; }
    50% { stroke-dashoffset: 0; }
    100% { stroke-dashoffset: -2000; }
}
</style>
<div style="text-align: center; margin-top: 5px; margin-bottom: 25px; padding: 20px 10px; background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%); border-radius: 20px; border: 2px solid #ef4444; box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05); position: relative; overflow: hidden;">
<!-- Animated EKG Background -->
<svg viewBox="0 0 1000 200" preserveAspectRatio="none" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.15; z-index: 0; pointer-events: none;">
<path class="ekg-line-sidebar" d="M0,100 L250,100 L270,70 L290,140 L320,30 L350,170 L370,80 L390,100 L700,100 L720,70 L740,140 L770,30 L800,170 L820,80 L840,100 L1000,100" fill="none" stroke="#0ea5e9" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
<!-- Medical Plus Symbols -->
<div style="position: absolute; top: 15px; left: 15px; color: #991b1b; font-size: 2rem; font-weight: bold; line-height: 1; opacity: 0.6; z-index: 1;">+</div>
<div style="position: absolute; top: 15px; right: 15px; color: #991b1b; font-size: 2rem; font-weight: bold; line-height: 1; opacity: 0.6; z-index: 1;">+</div>

<div style="position: relative; z-index: 1;">
<div style="position: absolute; top: -20px; left: -20px; width: 80px; height: 80px; background: radial-gradient(circle, rgba(14,165,233,0.1) 0%, rgba(255,255,255,0) 70%); border-radius: 50%;"></div>
<div style="display: inline-flex; align-items: center; justify-content: center; width: 64px; height: 64px; border-radius: 50%; background: linear-gradient(135deg, #0ea5e9, #6366f1); box-shadow: 0 8px 20px rgba(14, 165, 233, 0.35); margin-bottom: 15px;">
<span style="font-size: 32px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2)); color: white;">🩺</span>
</div>
<h2 style="font-size: 1.6rem; font-weight: 900; margin: 0; color: #0f172a; letter-spacing: -0.5px; line-height: 1.2;">
Medical AI
</h2>
<div style="margin-top: 8px; display: inline-block; background: #f0fdf4; border: 1px solid #bbf7d0; padding: 4px 12px; border-radius: 20px;">
<p style="font-size: 0.75rem; font-weight: 700; color: #16a34a; text-transform: uppercase; letter-spacing: 1px; margin: 0;">
Clinical Assistant
</p>
</div>
</div>
</div>
        """,
        unsafe_allow_html=True
    )
    
    st.sidebar.divider()

    # ==========================
    # Patient Profiles
    # ==========================
    st.sidebar.subheader("👤 Patient Profiles")
    from patient_profile import get_all_patients, create_patient_profile, delete_patient
    
    patients = get_all_patients()
    patient_opts = {p['id']: p['name'] for p in patients}
    patient_opts[None] = "Guest / No Profile"

    current_patient_id = st.session_state.get("active_patient_id", None)
    
    selected_patient = st.sidebar.selectbox(
        "Active Patient",
        options=list(patient_opts.keys()),
        format_func=lambda x: patient_opts[x],
        index=list(patient_opts.keys()).index(current_patient_id) if current_patient_id in patient_opts else 0,
        label_visibility="collapsed"
    )

    if selected_patient != current_patient_id:
        st.session_state.active_patient_id = selected_patient
        st.rerun()

    if st.sidebar.button("🗑️ Delete Profile", use_container_width=True, disabled=(selected_patient is None)):
        if selected_patient is not None:
            delete_patient(selected_patient)
            st.session_state.active_patient_id = None
            st.toast("Profile deleted.", icon="🗑️")
            st.rerun()

    with st.sidebar.expander("➕ Add New Patient"):
        with st.form("new_patient_form"):
            p_name = st.text_input("Name*")
            p_age = st.number_input("Age", min_value=0, max_value=120, value=30)
            p_gender = st.selectbox("Gender", ["Male", "Female", "Other"])
            p_chronic = st.text_area("Chronic Conditions")
            p_allergies = st.text_area("Allergies")
            p_meds = st.text_area("Current Medications")
            
            if st.form_submit_button("Save Patient"):
                if p_name:
                    create_patient_profile(p_name, p_age, p_gender, p_chronic, p_allergies, p_meds)
                    st.toast(f"Patient {p_name} added successfully!", icon="✅")
                    st.rerun()
                else:
                    st.error("Name is required.")

    st.sidebar.divider()



    st.sidebar.subheader("📄 Upload Medical Documents")

    uploaded_file = st.sidebar.file_uploader(
        "Upload Document",
        type=["pdf", "txt", "docx", "csv"],
        label_visibility="collapsed"
    )

    if uploaded_file:

        save_path = DATA_DIR / uploaded_file.name

        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.sidebar.success(
            f"Uploaded: {uploaded_file.name}"
        )

        st.sidebar.info(
            "Restart app and rebuild index."
        )


    st.sidebar.divider()


    # ==========================
    # Indexed Documents
    # ==========================

    st.sidebar.subheader("📚 Indexed Documents")
    
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔄 Sync", use_container_width=True, help="Rebuild vector database from files"):
            with st.spinner("Rebuilding database..."):
                from vector_store import build_vector_database
                build_vector_database(DATA_DIR)
                st.rerun()
    with col2:
        if st.button("🗑️ Clear All", use_container_width=True, help="Delete all documents"):
            import shutil
            from config import CHROMA_DB_DIR
            for ext in ['*.pdf', '*.txt', '*.docx', '*.csv']:
                for f in DATA_DIR.glob(ext):
                    try:
                        os.remove(f)
                    except:
                        pass
            if os.path.exists(CHROMA_DB_DIR):
                shutil.rmtree(CHROMA_DB_DIR, ignore_errors=True)
            st.rerun()

    extensions = ['*.pdf', '*.txt', '*.docx', '*.csv']
    all_files = []
    for ext in extensions:
        all_files.extend(list(DATA_DIR.glob(ext)))


    if all_files:

        for doc_file in all_files:

            col1, col2 = st.sidebar.columns([3, 1])


            with col1:
                st.write(
                    f"📄 {doc_file.name}"
                )


            with col2:

                if st.button(
                    "🗑️",
                    key=f"delete_{doc_file.name}"
                ):

                    try:
                        from vector_store import delete_document_from_db
                        delete_document_from_db(doc_file.name)
                        os.remove(doc_file)

                        st.sidebar.success(
                            f"{doc_file.name} deleted"
                        )

                        st.rerun()


                    except Exception as e:

                        st.sidebar.error(
                            str(e)
                        )


    else:

        st.sidebar.markdown(
            """
            <div style="background: rgba(241, 245, 249, 0.5); padding: 10px; border-radius: 8px; text-align: center; color: #64748b; font-size: 0.85rem; border: 1px dashed #cbd5e1; margin-top: 5px;">
                No documents found.
            </div>
            """, 
            unsafe_allow_html=True
        )



    st.sidebar.divider()


    # ==========================
    # Statistics
    # ==========================

    st.sidebar.subheader("📊 Statistics")

    st.sidebar.markdown(
        f"""
        <div style="background: white; border-radius: 12px; padding: 15px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 10px;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px; margin-bottom: 10px;">
                <span style="color: #64748b; font-size: 0.8rem; font-weight: 600;">📄 Docs Indexed</span>
                <span style="color: #0ea5e9; font-weight: 800; font-size: 0.95rem;">{len(all_files)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px; margin-bottom: 10px;">
                <span style="color: #64748b; font-size: 0.8rem; font-weight: 600;">🔍 Top-K Match</span>
                <span style="color: #0ea5e9; font-weight: 800; font-size: 0.95rem;">{TOP_K}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px; margin-bottom: 10px;">
                <span style="color: #64748b; font-size: 0.8rem; font-weight: 600;">🧬 Embedding</span>
                <span style="color: #8b5cf6; font-weight: 700; font-size: 0.7rem; background: #ede9fe; padding: 3px 8px; border-radius: 12px;">{EMBEDDING_MODEL}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #64748b; font-size: 0.8rem; font-weight: 600;">🧠 Core LLM</span>
                <span style="color: #10b981; font-weight: 700; font-size: 0.7rem; background: #d1fae5; padding: 3px 8px; border-radius: 12px; max-width: 130px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{LLM_MODEL}">{LLM_MODEL}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



    st.sidebar.divider()


    # ==========================
    # System Status
    # ==========================

    st.sidebar.subheader("⚙️ System Status")
    
    st.session_state.privacy_mode = st.sidebar.toggle("🔒 Strict Privacy Mode", value=st.session_state.get("privacy_mode", False), help="Bypass Groq cloud and process all data locally via Ollama for maximum HIPAA compliance.")
    
    st.session_state.chat_language = st.sidebar.selectbox(
        "🌐 Chat Language",
        options=[
            "English", "Hindi", "Bengali", "Marathi", "Telugu", "Tamil", "Gujarati", 
            "Urdu", "Kannada", "Odia", "Malayalam", "Punjabi", "Assamese", "Maithili",
            "Spanish", "French", "German", "Chinese", "Arabic", "Russian", "Japanese"
        ],
        index=0,
        help="Select the language the AI Assistant should respond in."
    )

    llm_status_color = "#f59e0b" if st.session_state.privacy_mode else "#10b981"
    llm_status_text = "Ollama (Local)" if st.session_state.privacy_mode else "Groq (Cloud)"

    st.sidebar.markdown(
        f"""
        <div style="background: white; border-radius: 12px; padding: 12px 15px; border: 1px solid #e2e8f0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); margin-bottom: 10px;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748b; font-size: 0.8rem; font-weight: 600;">LLM Engine</span>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <div style="width: 8px; height: 8px; border-radius: 50%; background-color: {llm_status_color}; box-shadow: 0 0 8px {llm_status_color};"></div>
                    <span style="color: #334155; font-size: 0.8rem; font-weight: 700;">{llm_status_text}</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #64748b; font-size: 0.8rem; font-weight: 600;">Vector DB</span>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <div style="width: 8px; height: 8px; border-radius: 50%; background-color: #10b981; box-shadow: 0 0 8px #10b981;"></div>
                    <span style="color: #334155; font-size: 0.8rem; font-weight: 700;">ChromaDB Ready</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="color: #64748b; font-size: 0.8rem; font-weight: 600;">RAG System</span>
                <div style="display: flex; align-items: center; gap: 6px;">
                    <div style="width: 8px; height: 8px; border-radius: 50%; background-color: #10b981; box-shadow: 0 0 8px #10b981;"></div>
                    <span style="color: #334155; font-size: 0.8rem; font-weight: 700;">Retriever Loaded</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )



    st.sidebar.divider()


    # ==========================
    # Chat Controls
    # ==========================

    st.sidebar.subheader("💬 Chat Controls")

    col1, col2 = st.sidebar.columns(2)

    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            clear_history(session_id)
            st.sidebar.success("History cleared")
            st.rerun()

    with col2:
        # Chat Export
        history = get_session_history(session_id if session_id else "default")
        chat_text = "# Medical AI Chat History\n\n"
        
        has_messages = hasattr(history, "messages") and bool(history.messages)
        if has_messages:
            for msg in history.messages:
                role = "Patient" if msg.type == "human" else "AI Assistant"
                chat_text += f"**{role}**:\n{msg.content}\n\n---\n\n"
                
        st.download_button(
            label="💾 Download",
            data=chat_text,
            file_name="medical_chat_history.md",
            mime="text/markdown",
            use_container_width=True
        )

    # ==========================
    # Sidebar Footer
    # ==========================

    st.sidebar.markdown(
        """
        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(14, 165, 233, 0.2);">
            <p style="font-size: 0.9rem; font-weight: 700; color: #334155; margin-bottom: 2px;">
                Designed by Ubaid Ashraf
            </p>
            <p style="font-size: 0.75rem; color: #94a3b8; margin-bottom: 20px;">
                © 2026 All Rights Reserved
            </p>
            <p style="font-size: 0.7rem; font-weight: 700; color: #64748b; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px;">
                Powered by
            </p>
            <div style="display: flex; justify-content: center; gap: 6px; flex-wrap: wrap;">
                <span style="font-size: 0.7rem; background: white; padding: 4px 10px; border-radius: 20px; color: #475569; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">Streamlit</span>
                <span style="font-size: 0.7rem; background: white; padding: 4px 10px; border-radius: 20px; color: #475569; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">LangChain</span>
                <span style="font-size: 0.7rem; background: white; padding: 4px 10px; border-radius: 20px; color: #475569; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">ChromaDB</span>
                <span style="font-size: 0.7rem; background: white; padding: 4px 10px; border-radius: 20px; color: #475569; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">Ollama</span>
                <span style="font-size: 0.7rem; background: white; padding: 4px 10px; border-radius: 20px; color: #475569; border: 1px solid #e2e8f0; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">Groq</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )