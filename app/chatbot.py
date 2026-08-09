from groq import Groq
import streamlit as st

from config import (
    GROQ_API_KEY,
)

from vector_store import get_retriever

from memory import (
    get_session_history,
    add_user_message,
)


# Initialize Groq
client = Groq(
    api_key=GROQ_API_KEY
)

def transcribe_audio(audio_file):
    transcription = client.audio.transcriptions.create(
      file=("audio.wav", audio_file.read()),
      model="whisper-large-v3",
      response_format="text",
    )
    return transcription.text

def ask_medical_ai(
    question: str,
    session_id: str = "default"
):
    # -------------------------------------------------
    # Load Retriever
    # -------------------------------------------------
    retriever = get_retriever()

    # -------------------------------------------------
    # Retrieve Documents
    # -------------------------------------------------
    docs = retriever.invoke(question)

    # -------------------------------------------------
    # Build Context
    # -------------------------------------------------
    context = "\n\n".join(doc.page_content for doc in docs)

    # -------------------------------------------------
    # Memory
    # -------------------------------------------------
    history = get_session_history(session_id)
    history_text = ""
    for message in history.messages:
        role = "User" if message.type == "human" else "Assistant"
        history_text += f"{role}: {message.content}\n"

    from patient_profile import format_patient_context
    from agents import generate_agentic_response
    
    active_patient_id = st.session_state.get("active_patient_id")
    patient_context = format_patient_context(active_patient_id) if active_patient_id else ""
    privacy_mode = st.session_state.get("privacy_mode", False)
    chat_language = st.session_state.get("chat_language", "English (US)")
    compliance_region = st.session_state.get("compliance_region", "US (FDA / HIPAA)")

    # -------------------------------------------------
    # Level 15: Self-Verifying AGI Pipeline (UI Simulation)
    # -------------------------------------------------
    # We yield a status block if this is the main chat interface
    
    # Generate the actual response
    answer_generator, route, sentiment, is_emergency, triage_score = generate_agentic_response(
        question=question,
        context=context,
        history_text=history_text,
        patient_context=patient_context,
        patient_id=active_patient_id,
        privacy_mode=privacy_mode,
        language=chat_language,
        compliance_region=compliance_region,
        stream=True
    )

    def stream_answer():
        if is_emergency or route == "emergency_triage":
            yield "🚨 **EMERGENCY TRIAGE SUPERVISOR** 🚨\n\n"
        elif route == "complex":
            yield "⚖️ **Chief Medical AI** *(Moderating Autonomous Debate...)*\n\n"
        else:
            pretty_name = route.replace("_", " ").title().replace("Ai", "AI")
            yield f"*{pretty_name}*\n\n"
            
        if isinstance(answer_generator, str):
            yield answer_generator
        else:
            for chunk in answer_generator:
                yield chunk

    # -------------------------------------------------
    # Save Memory
    # -------------------------------------------------
    add_user_message(session_id, question)

    return {
        "answer_generator": stream_answer(),
        "sources": docs,
        "route": route,
        "sentiment": sentiment,
        "is_emergency": is_emergency,
        "triage_score": triage_score
    }