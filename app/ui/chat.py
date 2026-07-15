from pathlib import Path
import streamlit as st

from chatbot import ask_medical_ai
from memory import get_session_history
from chat_history import save_message


def render_chat(session_id: str):
    """
    Medical Chat Interface
    """

    st.markdown(
        """
        <div class="card">

        <h3>🩺 Medical Consultation</h3>

        Ask questions from uploaded medical documents.

        </div>
        """,
        unsafe_allow_html=True,
    )

    history = get_session_history(session_id)

    # Display conversation
    for message in history.messages:

        role = "user" if message.type == "human" else "assistant"

        with st.chat_message(role):
            st.markdown(message.content)

    # Advanced Features
    if len(history.messages) > 0:
        with st.expander("📝 Generate Clinical Notes & Export"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Generate SOAP Note", use_container_width=True):
                    from agents import generate_soap_note
                    from patient_profile import format_patient_context
                    active_patient_id = st.session_state.get("active_patient_id")
                    patient_context = format_patient_context(active_patient_id) if active_patient_id else ""
                    privacy_mode = st.session_state.get("privacy_mode", False)
                    
                    history_text = "\n".join([f"{'User' if m.type == 'human' else 'Assistant'}: {m.content}" for m in history.messages])
                    
                    with st.spinner("Generating SOAP note..."):
                        soap_note = generate_soap_note(history_text, patient_context, privacy_mode=privacy_mode)
                        st.session_state[f"soap_{session_id}"] = soap_note
                        
            with col2:
                if st.button("Export to FHIR JSON", use_container_width=True):
                    if f"soap_{session_id}" not in st.session_state:
                        st.warning("Please generate a SOAP note first.")
                    else:
                        from agents import generate_fhir_json
                        from patient_profile import format_patient_context
                        active_patient_id = st.session_state.get("active_patient_id")
                        patient_context = format_patient_context(active_patient_id) if active_patient_id else ""
                        privacy_mode = st.session_state.get("privacy_mode", False)
                        
                        with st.spinner("Converting to FHIR JSON..."):
                            fhir_json = generate_fhir_json(st.session_state[f"soap_{session_id}"], patient_context, privacy_mode=privacy_mode)
                            st.session_state[f"fhir_{session_id}"] = fhir_json

            if f"soap_{session_id}" in st.session_state:
                st.markdown("### Generated SOAP Note")
                st.info(st.session_state[f"soap_{session_id}"])
                st.download_button("Download SOAP", st.session_state[f"soap_{session_id}"], file_name="soap_note.md")
                
            if f"fhir_{session_id}" in st.session_state:
                st.markdown("### FHIR JSON Export")
                st.code(st.session_state[f"fhir_{session_id}"], language="json")
                st.download_button("Download FHIR", st.session_state[f"fhir_{session_id}"], file_name="patient_fhir.json")

    question = st.chat_input("Ask a medical question...")

    with st.popover("🎤 Voice Input"):
        st.info("If the live microphone isn't working (due to browser permissions), you can upload an audio file instead.")
        audio_value = st.audio_input("Record Voice Question")
        uploaded_audio = st.file_uploader("📂 Or Upload Voice Note", type=["wav", "mp3", "m4a", "ogg", "webm"])
        
        final_audio = audio_value if audio_value else uploaded_audio
        
        if final_audio:
            audio_bytes = final_audio.getvalue()
            current_hash = hash(audio_bytes)
            
            if st.session_state.get("last_audio_hash") != current_hash:
                st.session_state.last_audio_hash = current_hash
                from chatbot import transcribe_audio
                with st.spinner("Transcribing audio..."):
                    try:
                        transcribed_text = transcribe_audio(final_audio)
                        if transcribed_text:
                            question = transcribed_text
                    except Exception as e:
                        st.error(f"Voice transcription failed: {e}")

    with st.popover("📷 Image Upload"):
        st.info("Upload photos of rashes, cuts, or skin spots for AI visual analysis. Note: Does not replace professional medical diagnosis.")
        uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
        
        if uploaded_image:
            if st.button("Analyze Image"):
                from image_ai import analyze_medical_image
                from memory import add_user_message, add_ai_message
                
                chat_language = st.session_state.get("chat_language", "English")
                with st.spinner("Analyzing image..."):
                    try:
                        analysis_result = analyze_medical_image(uploaded_image, language=chat_language, mime_type=uploaded_image.type)
                        
                        user_msg = f"[Uploaded Image: {uploaded_image.name}]"
                        
                        # Save to SQLite permanent storage
                        save_message(session_id, "user", user_msg)
                        save_message(session_id, "assistant", analysis_result)
                        
                        # Save to RAM cache so it renders immediately
                        add_user_message(session_id, user_msg)
                        add_ai_message(session_id, analysis_result)
                        
                        st.rerun()
                    except Exception as e:
                        st.error(f"Image analysis failed: {e}")

    if not question:
        return

    # Display user message
    with st.chat_message("user"):
        st.markdown(question)

    # Save user message to SQLite
    save_message(
        session_id=session_id,
        role="user",
        message=question,
    )

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Analyzing medical knowledge..."):

            try:

                response = ask_medical_ai(
                    question,
                    session_id,
                )

                answer = response.get(
                    "answer",
                    "No answer generated.",
                )

                st.markdown(answer)
                
                # Add TTS (Voice Output)
                try:
                    from gtts import gTTS
                    import base64
                    tts = gTTS(text=answer, lang='en')
                    tts.save("response.mp3")
                    with open("response.mp3", "rb") as f:
                        audio_bytes = f.read()
                        audio_base64 = base64.b64encode(audio_bytes).decode()
                        audio_html = f'''
                            <audio controls style="height: 35px; margin-top: 10px;">
                                <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                            </audio>
                        '''
                        st.markdown(audio_html, unsafe_allow_html=True)
                except Exception as e:
                    pass

                # Save AI response to SQLite
                save_message(
                    session_id=session_id,
                    role="assistant",
                    message=answer,
                )
                
                # Advanced PDF Export
                if len(history.messages) > 0:
                    with st.expander("📄 Export Full Session Report (PDF)"):
                        if st.button("Generate PDF Report", key="pdf_btn"):
                            with st.spinner("Generating beautiful PDF report..."):
                                try:
                                    from fpdf import FPDF
                                    pdf = FPDF()
                                    pdf.add_page()
                                    pdf.set_font("Arial", size=12)
                                    pdf.cell(200, 10, txt="Medical AI Assistant - Session Report", ln=True, align='C')
                                    pdf.ln(10)
                                    
                                    for msg in history.messages:
                                        role = "Patient" if msg.type == "human" else "AI Assistant"
                                        pdf.set_font("Arial", 'B', 10)
                                        pdf.cell(200, 10, txt=f"{role}:", ln=True)
                                        pdf.set_font("Arial", size=10)
                                        # Handle special characters
                                        content = msg.content.encode('latin-1', 'replace').decode('latin-1')
                                        pdf.multi_cell(0, 10, txt=content)
                                        pdf.ln(5)
                                        
                                    pdf.output("session_report.pdf")
                                    with open("session_report.pdf", "rb") as f:
                                        st.download_button("Download PDF Report", f, file_name="session_report.pdf", mime="application/pdf")
                                except Exception as e:
                                    st.error(f"PDF generation failed: {e}")

                sources = response.get(
                    "sources",
                    [],
                )

                if sources:

                    with st.expander("📚 View Sources"):
                        
                        seen_sources = set()
                        display_count = 1

                        for doc in sources:

                            filename = Path(
                                doc.metadata.get(
                                    "source",
                                    "Unknown",
                                )
                            ).name

                            page = (
                                doc.metadata.get(
                                    "page",
                                    0,
                                )
                                + 1
                            )
                            
                            source_key = (filename, page)
                            if source_key in seen_sources:
                                continue
                                
                            seen_sources.add(source_key)

                            st.markdown(
                                f"""
**Source {display_count}**

📄 **File:** {filename}

📑 **Page:** {page}
"""
                            )
                            display_count += 1

            except Exception as e:

                st.error(f"❌ {e}")