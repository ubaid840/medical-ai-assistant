import streamlit as st
import os
import requests

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
from chat_history import get_all_sessions, create_session, delete_session


def render_sidebar(session_id=None):

    st.sidebar.markdown(
        """
<style>
.ekg-line-sidebar {
    stroke-dasharray: 2000;
    stroke-dashoffset: 2000;
    animation: draw-ekg-sidebar 4s infinite linear;
}
@keyframes draw-ekg-sidebar {
    0% { stroke-dashoffset: 2000; }
    50% { stroke-dashoffset: 0; }
    100% { stroke-dashoffset: -2000; }
}
.premium-sidebar-card {
    text-align: center;
    margin-top: 5px;
    margin-bottom: 25px;
    padding: 25px 15px;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    border-radius: 24px;
    box-shadow: 0 20px 40px -10px rgba(15, 23, 42, 0.5), inset 0 1px 0 rgba(255,255,255,0.1);
    position: relative;
    overflow: hidden;
    color: white;
}
.premium-glow {
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(56, 189, 248, 0.15) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}
</style>
<div class="premium-sidebar-card">
<div class="premium-glow"></div>
<!-- Animated EKG Background -->
<svg viewBox="0 0 1000 200" preserveAspectRatio="none" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; opacity: 0.25; z-index: 0; pointer-events: none;">
<path class="ekg-line-sidebar" d="M0,100 L250,100 L270,70 L290,140 L320,30 L350,170 L370,80 L390,100 L700,100 L720,70 L740,140 L770,30 L800,170 L820,80 L840,100 L1000,100" fill="none" stroke="#38bdf8" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>

<div style="position: relative; z-index: 1;">
<div style="display: inline-flex; align-items: center; justify-content: center; width: 72px; height: 72px; border-radius: 20px; background: linear-gradient(135deg, #0ea5e9, #4f46e5); box-shadow: 0 10px 25px rgba(14, 165, 233, 0.5); border: 1px solid rgba(255,255,255,0.2); margin-bottom: 15px;">
<span style="font-size: 36px; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3)); color: white;">🩺</span>
</div>
<h2 style="font-size: 1.8rem; font-weight: 800; margin: 0; color: #ffffff; letter-spacing: -0.5px; line-height: 1.2; text-shadow: 0 2px 10px rgba(0,0,0,0.2);">
Medical AI
</h2>
<div style="margin-top: 10px; display: inline-block; background: rgba(52, 211, 153, 0.1); border: 1px solid rgba(52, 211, 153, 0.2); padding: 5px 14px; border-radius: 20px; backdrop-filter: blur(10px);">
<p style="font-size: 0.75rem; font-weight: 700; color: #34d399; text-transform: uppercase; letter-spacing: 1.5px; margin: 0;">
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

    if selected_patient is not None:
        if st.sidebar.button("🗑️ Delete Profile", use_container_width=True):
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

    # ==========================
    # Chat Sessions
    # ==========================
    
    st.sidebar.subheader("💬 Chat Sessions")
    
    sessions = get_all_sessions()
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("➕ New Chat", use_container_width=True, type="primary"):
            st.session_state.session_id = create_session("New Chat")
            st.session_state.chat_memory = {}
            st.rerun()
            
    with col2:
        if sessions:
            if st.button("🗑️ Delete", use_container_width=True, type="primary"):
                delete_session(st.session_state.session_id)
                if st.session_state.session_id in st.session_state.chat_memory:
                    del st.session_state.chat_memory[st.session_state.session_id]
                st.session_state.session_id = create_session("New Chat")
                st.rerun()
        else:
            st.button("🗑️ Delete", use_container_width=True, type="primary", disabled=True)
            
    if sessions:
        # Filter out sessions with 0 messages, UNLESS it's the currently active session
        valid_sessions = [s for s in sessions if s[3] > 0 or s[0] == st.session_state.session_id]
        
        # If somehow valid_sessions is empty but sessions isn't, fallback to just the first one
        if not valid_sessions:
            valid_sessions = [sessions[0]]
            
        session_opts = {s[0]: f"💬 {s[1]} ({s[2][:10]}) - {s[3]} msgs" for s in valid_sessions} 
        
        current_id = st.session_state.session_id
        session_ids = list(session_opts.keys())
        current_index = session_ids.index(current_id) if current_id in session_ids else 0

        selected_id = st.sidebar.selectbox(
            "Select Past Chat",
            options=session_ids,
            format_func=lambda x: session_opts[x],
            index=current_index,
            label_visibility="collapsed"
        )

        if selected_id != st.session_state.session_id:
            st.session_state.session_id = selected_id
            st.rerun()
    else:
        st.sidebar.markdown(
            """
            <div style="background: rgba(241, 245, 249, 0.5); padding: 10px; border-radius: 8px; text-align: center; color: #64748b; font-size: 0.85rem; border: 1px dashed #cbd5e1; margin-top: 5px;">
                No past chats available.
            </div>
            """, 
            unsafe_allow_html=True
        )

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
        <div style="background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px); border-radius: 16px; padding: 18px; border: 1px solid rgba(255,255,255,0.8); box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); margin-bottom: 10px; transition: transform 0.2s;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #cbd5e1; padding-bottom: 12px; margin-bottom: 12px;">
                <span style="color: #475569; font-size: 0.85rem; font-weight: 700; display: flex; align-items: center; gap: 8px;"><div style="width:24px; height:24px; background:linear-gradient(135deg, #38bdf8, #0ea5e9); border-radius:6px; display:flex; align-items:center; justify-content:center; color:white; font-size:12px;">📄</div> Docs Indexed</span>
                <span style="color: #0f172a; font-weight: 900; font-size: 1.1rem;">{len(all_files)}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #cbd5e1; padding-bottom: 12px; margin-bottom: 12px;">
                <span style="color: #475569; font-size: 0.85rem; font-weight: 700; display: flex; align-items: center; gap: 8px;"><div style="width:24px; height:24px; background:linear-gradient(135deg, #f43f5e, #e11d48); border-radius:6px; display:flex; align-items:center; justify-content:center; color:white; font-size:12px;">🔍</div> Top-K Match</span>
                <span style="color: #0f172a; font-weight: 900; font-size: 1.1rem;">{TOP_K}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px dashed #cbd5e1; padding-bottom: 12px; margin-bottom: 12px;">
                <span style="color: #475569; font-size: 0.85rem; font-weight: 700; display: flex; align-items: center; gap: 8px;"><div style="width:24px; height:24px; background:linear-gradient(135deg, #a855f7, #7e22ce); border-radius:6px; display:flex; align-items:center; justify-content:center; color:white; font-size:12px;">🧬</div> Embedding</span>
                <span style="color: #7e22ce; font-weight: 800; font-size: 0.75rem; background: rgba(168,85,247,0.1); padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(168,85,247,0.2);">{EMBEDDING_MODEL}</span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="color: #475569; font-size: 0.85rem; font-weight: 700; display: flex; align-items: center; gap: 8px;"><div style="width:24px; height:24px; background:linear-gradient(135deg, #10b981, #059669); border-radius:6px; display:flex; align-items:center; justify-content:center; color:white; font-size:12px;">🧠</div> Core LLM</span>
                <span style="color: #059669; font-weight: 800; font-size: 0.75rem; background: rgba(16,185,129,0.1); padding: 4px 10px; border-radius: 20px; border: 1px solid rgba(16,185,129,0.2); max-width: 110px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="{LLM_MODEL}">{LLM_MODEL}</span>
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
        <div style="background: rgba(15, 23, 42, 0.95); border-radius: 16px; padding: 18px; border: 1px solid rgba(255,255,255,0.1); box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2); margin-bottom: 10px;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">
                <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">LLM Engine</span>
                <div style="display: flex; align-items: center; gap: 8px; background: rgba(0,0,0,0.3); padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
                    <div style="width: 8px; height: 8px; border-radius: 50%; background-color: {llm_status_color}; box-shadow: 0 0 12px {llm_status_color};"></div>
                    <span style="color: #f8fafc; font-size: 0.8rem; font-weight: 800;">{llm_status_text}</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px;">
                <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">Vector DB</span>
                <div style="display: flex; align-items: center; gap: 8px; background: rgba(0,0,0,0.3); padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
                    <div style="width: 8px; height: 8px; border-radius: 50%; background-color: #10b981; box-shadow: 0 0 12px #10b981;"></div>
                    <span style="color: #f8fafc; font-size: 0.8rem; font-weight: 800;">ChromaDB Ready</span>
                </div>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">RAG System</span>
                <div style="display: flex; align-items: center; gap: 8px; background: rgba(0,0,0,0.3); padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.05);">
                    <div style="width: 8px; height: 8px; border-radius: 50%; background-color: #38bdf8; box-shadow: 0 0 12px #38bdf8;"></div>
                    <span style="color: #f8fafc; font-size: 0.8rem; font-weight: 800;">Retriever Loaded</span>
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
        <div style="text-align: center; margin-top: 40px; padding: 25px 15px; border-radius: 16px; background: linear-gradient(135deg, #f8fafc, #f1f5f9); border: 1px solid #e2e8f0; box-shadow: inset 0 2px 4px rgba(255,255,255,0.5);">
            <div style="width: 40px; height: 4px; background: linear-gradient(90deg, #0ea5e9, #4f46e5); border-radius: 2px; margin: 0 auto 15px auto;"></div>
            <p style="font-size: 0.95rem; font-weight: 800; color: #0f172a; margin-bottom: 2px; letter-spacing: -0.2px;">
                Designed by Ubaid Ashraf
            </p>
            <p style="font-size: 0.75rem; color: #64748b; margin-bottom: 20px; font-weight: 500;">
                © 2026 All Rights Reserved
            </p>
            <p style="font-size: 0.65rem; font-weight: 800; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 12px;">
                Powered by
            </p>
            <div style="display: flex; justify-content: center; gap: 8px; flex-wrap: wrap;">
                <span style="font-size: 0.7rem; background: white; padding: 5px 12px; border-radius: 20px; color: #334155; font-weight: 600; border: 1px solid #cbd5e1; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">Streamlit</span>
                <span style="font-size: 0.7rem; background: white; padding: 5px 12px; border-radius: 20px; color: #334155; font-weight: 600; border: 1px solid #cbd5e1; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">LangChain</span>
                <span style="font-size: 0.7rem; background: white; padding: 5px 12px; border-radius: 20px; color: #334155; font-weight: 600; border: 1px solid #cbd5e1; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">ChromaDB</span>
                <span style="font-size: 0.7rem; background: white; padding: 5px 12px; border-radius: 20px; color: #334155; font-weight: 600; border: 1px solid #cbd5e1; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">Ollama</span>
                <span style="font-size: 0.7rem; background: white; padding: 5px 12px; border-radius: 20px; color: #334155; font-weight: 600; border: 1px solid #cbd5e1; box-shadow: 0 2px 4px rgba(0,0,0,0.02);">Groq</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )