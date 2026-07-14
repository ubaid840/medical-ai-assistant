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



    if not docs:

        return {
            "answer":
            "I couldn't find this information in the uploaded medical documents.",
            "sources":[]
        }



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



    # -------------------------------------------------
    # Prompt
    # -------------------------------------------------

    prompt = f"""
{SYSTEM_PROMPT}


Conversation History:

{history_text}



Retrieved Medical Context:

{context}



Current Question:

{question}



Instructions:

1. Answer only from medical context.
2. Use conversation history for references.
3. Explain clearly.
4. Do not diagnose.
5. If information is unavailable say:
"I couldn't find this information in the uploaded medical documents."


Answer:
"""



    # -------------------------------------------------
    # Groq Response
    # -------------------------------------------------

    response = client.chat.completions.create(

        model=LLM_MODEL,

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],

        temperature=0,

        max_tokens=700
    )


    answer = (
        response
        .choices[0]
        .message
        .content
        .strip()
    )



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

        "answer":answer,

        "sources":docs

    }