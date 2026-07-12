from groq import Groq

from config import (
    GROQ_API_KEY,
    LLM_MODEL,
)

from prompts import SYSTEM_PROMPT
from vector_store import get_retriever
from memory import get_session_history

# -------------------------------------------------
# Initialize Groq Client
# -------------------------------------------------

client = Groq(api_key=GROQ_API_KEY)


def ask_medical_ai(question: str, session_id: str = "default"):
    """
    Retrieve relevant documents from ChromaDB,
    use conversation memory,
    and generate an answer using Groq.
    """

    # -------------------------------------------------
    # Load Retriever
    # -------------------------------------------------

    retriever = get_retriever()

    # -------------------------------------------------
    # Retrieve Relevant Documents
    # -------------------------------------------------

    docs = retriever.invoke(question)

    print("=" * 60)
    print("Question:", question)
    print("Retrieved Documents:", len(docs))

    for i, doc in enumerate(docs, start=1):
        print(f"\nDocument {i}")
        print("Source:", doc.metadata.get("source", "Unknown"))
        print("Page:", doc.metadata.get("page", 0) + 1)
        print(doc.page_content[:300])
        print("-" * 60)

    if not docs:
        return {
            "answer": "I couldn't find this information in the uploaded medical documents.",
            "sources": []
        }

    # -------------------------------------------------
    # Build Context
    # -------------------------------------------------

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    # -------------------------------------------------
    # Conversation Memory
    # -------------------------------------------------

    history = get_session_history(session_id)

    history_text = ""

    for message in history.messages:
        role = "User" if message.type == "human" else "Assistant"
        history_text += f"{role}: {message.content}\n"

    # -------------------------------------------------
    # Prompt
    # -------------------------------------------------

    prompt = f"""
{SYSTEM_PROMPT}

You are a professional Medical AI Assistant.

Use ONLY the retrieved medical context.

Conversation History:
{history_text}

Medical Context:
{context}

Current Question:
{question}

Rules:
1. Use ONLY the medical context.
2. Use conversation history only to understand references like "it", "that disease", etc.
3. Never invent medical facts.
4. If the answer is unavailable, reply:
"I couldn't find this information in the uploaded medical documents."

Answer:
"""

    # -------------------------------------------------
    # LLM Response
    # -------------------------------------------------

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=700,
    )

    answer = response.choices[0].message.content.strip()

    # -------------------------------------------------
    # Save Conversation
    # -------------------------------------------------

    history.add_user_message(question)
    history.add_ai_message(answer)

    return {
        "answer": answer,
        "sources": docs
    }