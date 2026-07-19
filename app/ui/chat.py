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
<div style="
background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 100%);
border-radius: 20px;
padding: 35px 30px;
color: white;
box-shadow: 0 20px 40px -10px rgba(99, 102, 241, 0.4);
margin-bottom: 25px;
position: relative;
overflow: hidden;
border: 1px solid rgba(255,255,255,0.2);
">
<!-- Abstract background circles for depth -->
<div style="position: absolute; top: -50px; right: -50px; width: 250px; height: 250px; background: rgba(255,255,255,0.1); border-radius: 50%; filter: blur(30px); pointer-events: none;"></div>
<div style="position: absolute; bottom: -80px; left: 10%; width: 200px; height: 200px; background: rgba(255,255,255,0.15); border-radius: 50%; filter: blur(25px); pointer-events: none;"></div>

<div style="display: flex; align-items: center; gap: 25px; position: relative; z-index: 1;">
<div style="background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); width: 80px; height: 80px; border-radius: 20px; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 25px rgba(0,0,0,0.15); border: 1px solid rgba(255,255,255,0.4);">
<span style="font-size: 40px; filter: drop-shadow(0 4px 6px rgba(0,0,0,0.2));">💬</span>
</div>
<div>
<h2 style="margin: 0; font-size: 2.2rem; font-weight: 900; letter-spacing: -0.5px; text-shadow: 0 2px 4px rgba(0,0,0,0.15);">AI Clinical Consultation</h2>
<p style="margin: 8px 0 0 0; font-size: 1.1rem; opacity: 0.95; font-weight: 500; letter-spacing: 0.2px;">Secure, intelligent analysis of your medical history and symptoms.</p>
</div>
</div>
</div>
        """,
        unsafe_allow_html=True,
    )

    history = get_session_history(session_id)

    # Chat Container ensures all messages are drawn BEFORE the chat input
    chat_container = st.container()

    # Display conversation history
    with chat_container:
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



    if "submitted_question" not in st.session_state:
        st.session_state.submitted_question = None

    def handle_submit():
        st.session_state.submitted_question = st.session_state.chat_input_widget

    # Render Chat Input first so it's above the buttons
    st.chat_input("Ask a medical question...", key="chat_input_widget", on_submit=handle_submit)

    # Put upload buttons side-by-side UNDER the chat input
    col1, col2 = st.columns(2)

    with col1:
        with st.popover("🎤 Voice Input", use_container_width=True):
            st.info("If the live microphone isn't working (due to browser permissions), you can upload an audio file instead.")
            audio_value = st.audio_input("Record Voice Question", key=f"mic_in_{session_id}")
            uploaded_audio = st.file_uploader("📂 Or Upload Voice Note", type=["wav", "mp3", "m4a", "ogg", "webm"], key=f"mic_up_{session_id}")
            
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
                                st.session_state.submitted_question = transcribed_text
                        except Exception as e:
                            st.error(f"Voice transcription failed: {e}")

    with col2:
        with st.popover("📷 Image Upload", use_container_width=True):
            st.info("Upload photos of rashes, cuts, or skin spots for AI visual analysis. Note: Does not replace professional medical diagnosis.")
            uploaded_image = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"], key=f"img_up_{session_id}")
            
            if uploaded_image:
                if st.button("Analyze Image", key=f"img_btn_{session_id}"):
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

    question = st.session_state.submitted_question

    if not question:
        return
    
    # Clear the submission so it doesn't run twice
    st.session_state.submitted_question = None

    # Generate and display new AI response inside the chat container
    with chat_container:
        # Display user message
        with st.chat_message("user"):
            st.markdown(question)

        # Save user message to SQLite
        save_message(
            session_id=session_id,
            role="user",
            message=question,
        )
        
        # HIPAA Audit Log
        from database import log_audit
        active_patient_id = st.session_state.get("active_patient_id")
        log_audit("User Query", active_patient_id, "User submitted a medical query to the AI.")

        # Generate AI response
        with st.chat_message("assistant"):
            
            status = st.status("🧠 Processing medical query...", expanded=True)
        status.write("🌐 Retrieving context and routing to specialist...")

        try:

            response = ask_medical_ai(
                question,
                session_id,
            )
            
            route = response.get("route", "general")
            is_emergency = response.get("is_emergency", False)
            
            if is_emergency:
                status.write("🚨 **EMERGENCY DETECTED. HANDING OFF.** 🚨")
                log_audit("Emergency Escalation", active_patient_id, "AI detected a potential medical emergency and triggered triage handoff.")
                st.markdown(
                    """
                    <div style="background-color: #fef2f2; border: 2px solid #ef4444; border-radius: 12px; padding: 25px; margin-top: 15px; text-align: center; box-shadow: 0 10px 25px rgba(239, 68, 68, 0.3);">
                        <h1 style="color: #ef4444; margin: 0 0 10px 0; font-size: 2.5rem;">🚨 EMERGENCY DETECTED 🚨</h1>
                        <p style="color: #991b1b; font-size: 1.2rem; font-weight: bold; margin: 0;">This system is not for emergency use. Please call 911 immediately.</p>
                        <hr style="border-color: #fca5a5; margin: 15px 0;">
                        <p style="color: #7f1d1d; margin: 0;">The chat interface has been locked and human triage has been notified.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif route == "complex":
                status.write("✅ Routed to Pharmacology & Diagnostician Agents for Debate.")
            else:
                status.write(f"✅ Routed to {route.capitalize()} Agent.")
            status.update(label="Response generated", state="complete", expanded=False)

            answer_generator = response.get(
                "answer_generator",
                ["No answer generated."]
            )

            # Stream the response in real-time
            final_answer = st.write_stream(answer_generator)
            
            # Now that generation is complete, save to RAM cache
            from memory import add_ai_message
            add_ai_message(session_id, final_answer)

            # Save AI response to SQLite permanent storage
            save_message(
                session_id=session_id,
                role="assistant",
                message=final_answer,
            )
                
            # Instant Zero-Latency Voice Output (Web Speech API)
            # Escape backticks and standard quotes for JS template literal
            clean_text = final_answer.replace("`", "'").replace("\\", "\\\\")
            js_tts = f'''
                <div style="font-family: sans-serif; background: #f8fafc; padding: 12px; border-radius: 12px; border: 1px solid #e2e8f0; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);">
                    <button onclick="playTTS()" style="background: linear-gradient(135deg, #0ea5e9, #3b82f6); color: white; border: none; padding: 8px 14px; border-radius: 8px; cursor: pointer; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">▶️ Play</button>
                    <button onclick="pauseTTS()" style="background: #cbd5e1; color: #334155; border: none; padding: 8px 14px; border-radius: 8px; cursor: pointer; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">⏸️ Pause</button>
                    <button onclick="resumeTTS()" style="background: #cbd5e1; color: #334155; border: none; padding: 8px 14px; border-radius: 8px; cursor: pointer; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">⏯️ Resume</button>
                    <button onclick="stopTTS()" style="background: linear-gradient(135deg, #ef4444, #b91c1c); color: white; border: none; padding: 8px 14px; border-radius: 8px; cursor: pointer; font-weight: bold; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">⏹️ Stop</button>
                </div>
                <script>
                    const fullText = `{clean_text}`;
                    // Split text into sentences for dynamic volume control
                    const sentences = fullText.match(/[^.!?]+[.!?]+/g) || [fullText];
                    let currentIndex = 0;
                    let isPlaying = false;

                    function speakNext() {{
                        if (currentIndex >= sentences.length || !isPlaying) return;
                        
                        let utterance = new SpeechSynthesisUtterance(sentences[currentIndex]);
                        utterance.rate = 1.05;
                        utterance.pitch = 1.0;
                        
                        utterance.onend = function() {{
                            currentIndex++;
                            speakNext();
                        }};
                        
                        window.speechSynthesis.speak(utterance);
                    }}

                    function playTTS() {{
                        window.speechSynthesis.cancel();
                        currentIndex = 0;
                        isPlaying = true;
                        speakNext();
                    }}

                    function pauseTTS() {{ window.speechSynthesis.pause(); }}
                    function resumeTTS() {{ window.speechSynthesis.resume(); }}
                    
                    function stopTTS() {{
                        isPlaying = false;
                        window.speechSynthesis.cancel();
                    }}
                </script>
            '''
            import streamlit.components.v1 as components
            components.html(js_tts, height=80)

            # Add MP3 Download Option
            with st.expander("🎵 Download Audio (MP3)"):
                st.info("Download an offline MP3 of this response.")
                if st.button("Generate MP3", key="gen_mp3_btn"):
                    with st.spinner("Generating MP3 file... (This takes a few seconds)"):
                        try:
                            from gtts import gTTS
                            tts = gTTS(text=final_answer, lang='en')
                            tts.save("response.mp3")
                            with open("response.mp3", "rb") as f:
                                st.download_button("⬇️ Download MP3", f, file_name="ai_medical_response.mp3", mime="audio/mp3", key="dl_mp3_btn")
                        except Exception as e:
                            st.error(f"Failed to generate MP3: {e}")

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