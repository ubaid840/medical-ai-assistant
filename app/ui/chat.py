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

    st.markdown("#### Send a Message")
    input_mode = st.radio("Choose Input Method", ["💬 Text", "🎤 Voice"], horizontal=True, label_visibility="collapsed")
    
    question = None
    
    if input_mode == "💬 Text":
        question = st.chat_input("Ask a medical question...")
    else:
        st.info("If the live microphone isn't working (due to browser permissions), you can upload an audio file instead.")
        audio_value = st.audio_input("🎤 Record Voice Question")
        uploaded_audio = st.file_uploader("📂 Or Upload Voice Note", type=["wav", "mp3", "m4a", "ogg", "webm"])
        
        # Use whichever one is provided
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

                # Save AI response to SQLite
                save_message(
                    session_id=session_id,
                    role="assistant",
                    message=answer,
                )

                sources = response.get(
                    "sources",
                    [],
                )

                if sources:

                    with st.expander("📚 View Sources"):

                        for i, doc in enumerate(
                            sources,
                            start=1,
                        ):

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

                            st.markdown(
                                f"""
**Source {i}**

📄 **File:** {filename}

📑 **Page:** {page}
"""
                            )

            except Exception as e:

                st.error(f"❌ {e}")