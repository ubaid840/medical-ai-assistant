from groq import Groq

from config import (
    GROQ_API_KEY,
    LLM_MODEL,
)

from prompts import SYSTEM_PROMPT
from vector_store import get_retriever

from memory import (
    get_session_history,
    add_user_message,
    add_ai_message
)


# Initialize Groq

client = Groq(
    api_key=GROQ_API_KEY
)

def transcribe_audio(audio_file):
    """
    Transcribe audio using Groq Whisper model.
    """
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

    """
    Retrieve medical documents,
    use conversation memory,
    and generate answer using Groq.
    """


    # -------------------------------------------------
    # Load Retriever
    # -------------------------------------------------

    retriever = get_retriever()



    # -------------------------------------------------
    # Retrieve Documents
    # -------------------------------------------------

    docs = retriever.invoke(
        question
    )


    print("=" * 60)
    print("Question:", question)
    print("Retrieved Documents:", len(docs))


    for i, doc in enumerate(
        docs,
        start=1
    ):

        print(f"\nDocument {i}")

        print(
            "Source:",
            doc.metadata.get(
                "source",
                "Unknown"
            )
        )

        print(
            "Page:",
            doc.metadata.get(
                "page",
                0
            ) + 1
        )

        print(
            doc.page_content[:300]
        )

        print("-" * 60)



    # -------------------------------------------------
    # Build Context
    # -------------------------------------------------

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )



    # -------------------------------------------------
    # Memory
    # -------------------------------------------------

    history = get_session_history(
        session_id
    )


    history_text = ""


    for message in history.messages:

        role = (
            "User"
            if message.type == "human"
            else "Assistant"
        )


        history_text += (
            f"{role}: {message.content}\n"
        )



    import streamlit as st
    from patient_profile import format_patient_context
    from agents import generate_agentic_response
    
    active_patient_id = st.session_state.get("active_patient_id")
    patient_context = format_patient_context(active_patient_id) if active_patient_id else ""
    privacy_mode = st.session_state.get("privacy_mode", False)
    chat_language = st.session_state.get("chat_language", "English")

    # -------------------------------------------------
    # Agentic Response
    # -------------------------------------------------

    answer, route = generate_agentic_response(
        question=question,
        context=context,
        history_text=history_text,
        patient_context=patient_context,
        privacy_mode=privacy_mode,
        language=chat_language
    )

    answer = f"*{route.capitalize()} Agent*\n\n" + answer

    # -------------------------------------------------
    # Save Memory
    # -------------------------------------------------

    add_user_message(
        session_id,
        question
    )

    add_ai_message(
        session_id,
        answer
    )

    return {
        "answer": answer,
        "sources": docs,
        "route": route
    }