import streamlit as st
import time

def render_voice_scribe():
    st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #4f46e5, #0ea5e9); border-radius: 20px; color: white; margin-bottom: 2rem; box-shadow: 0 10px 25px rgba(14, 165, 233, 0.3);">
            <h1 style="margin: 0; font-size: 2.5rem; font-weight: 800;">🎙️ Ambient Voice Scribe</h1>
            <p style="margin-top: 10px; font-size: 1.1rem; opacity: 0.9;">Real-time clinical dictation and automated EHR structuring.</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.info("💡 **Tip:** Speak clearly into your microphone to dictate patient notes. The AI will automatically structure them into SOAP format.")

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🗣️ Audio Input")
        
        # We use a placeholder for the audio input, as some versions of Streamlit support it directly
        # If st.audio_input is available (Streamlit 1.39+) we use it, otherwise fallback
        if hasattr(st, 'audio_input'):
            audio = st.audio_input("Record Patient Encounter")
        else:
            st.warning("Audio recording requires a newer version of Streamlit. Using mock upload for demonstration.")
            audio = st.file_uploader("Upload Audio Note", type=['wav', 'mp3'])
            
        if audio is not None:
            with st.spinner("Transcribing and processing via Groq Whisper..."):
                time.sleep(0.01)  # Simulate processing delay
                st.success("Transcription Complete!")
                
                st.markdown("#### Raw Transcription")
                st.write("*\"Patient presents with a 3-day history of acute lower back pain radiating down the left leg. No history of trauma. Denies fever or bowel incontinence. Suspect sciatica or herniated disc. Plan for MRI and prescribe NSAIDs.\"*")
                
                st.session_state['transcription_done'] = True

    with col2:
        st.markdown("### 📋 Structured Output (SOAP)")
        
        if st.session_state.get('transcription_done', False):
            st.markdown("""
                <div style="background: rgba(255, 255, 255, 0.5); border: 1px solid rgba(0,0,0,0.1); border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <h4 style="color: #4f46e5; margin-top: 0;">Subjective</h4>
                    <p>3-day history of acute lower back pain radiating to left leg. No trauma. No fever or bowel incontinence.</p>
                    
                    <h4 style="color: #4f46e5;">Objective</h4>
                    <p><em>Pending physical examination details.</em></p>
                    
                    <h4 style="color: #4f46e5;">Assessment</h4>
                    <p>Likely sciatica or lumbar disc herniation.</p>
                    
                    <h4 style="color: #4f46e5;">Plan</h4>
                    <ul>
                        <li>Schedule Lumbar MRI</li>
                        <li>Prescribe NSAIDs (e.g., Naproxen 500mg BID)</li>
                        <li>Follow-up in 1 week</li>
                    </ul>
                    
                    <hr/>
                    <div style="display: flex; gap: 10px;">
                        <button style="background: #10b981; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Export to EHR</button>
                        <button style="background: #3b82f6; color: white; border: none; padding: 8px 15px; border-radius: 5px; cursor: pointer;">Generate Audio Summary (TTS)</button>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="display: flex; align-items: center; justify-content: center; height: 300px; border: 2px dashed #cbd5e1; border-radius: 15px; color: #64748b;">
                    <em>Awaiting transcription...</em>
                </div>
            """, unsafe_allow_html=True)
