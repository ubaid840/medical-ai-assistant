from groq import Groq

from config import (
    GROQ_API_KEY,
    LLM_MODEL,
)

from prompts import SYSTEM_PROMPT
from vector_store import get_retriever

# -------------------------------------------------
# Initialize Groq Client
# -------------------------------------------------

client = Groq(api_key=GROQ_API_KEY)


def ask_medical_ai(question: str):
    """
    Retrieve relevant documents from ChromaDB
    and generate an answer using the Groq LLM.
    """

    # ---------------------------------------------
    # Load retriever only when needed
    # ---------------------------------------------

    retriever = get_retriever()

    # Retrieve documents
    docs = retriever.invoke(question)

    # ---------------------------------------------
    # Debug Information
    # ---------------------------------------------

    print("=" * 60)
    print("Question:", question)
    print("Retrieved Documents:", len(docs))

    for i, doc in enumerate(docs, start=1):
        print(f"\nDocument {i}")
        print("Source:", doc.metadata.get("source", "Unknown"))
        print("Page:", doc.metadata.get("page", 0) + 1)
        print(doc.page_content[:300])
        print("-" * 60)

    # ---------------------------------------------
    # No documents found
    # ---------------------------------------------

    if not docs:
        return {
            "answer": "I couldn't find this information in the uploaded medical documents.",
            "sources": []
        }

    # ---------------------------------------------
    # Build Context
    # ---------------------------------------------

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    # ---------------------------------------------
    # Prompt
    # ---------------------------------------------

    prompt = f"""
{SYSTEM_PROMPT}

You are a Medical AI Assistant.

Use ONLY the information from the CONTEXT below.

Rules:
1. Answer only using the retrieved context.
2. Do NOT use outside knowledge.
3. If the answer is not present in the context, reply exactly:
"I couldn't find this information in the uploaded medical documents."

---------------- CONTEXT ----------------

{context}

-----------------------------------------

Question:
{question}

Answer:
"""

    # ---------------------------------------------
    # Generate Response
    # ---------------------------------------------

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

    return {
        "answer": answer,
        "sources": docs
    }