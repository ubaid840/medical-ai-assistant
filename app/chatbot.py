from groq import Groq

from config import (
    GROQ_API_KEY,
    LLM_MODEL,
)

from prompts import SYSTEM_PROMPT
from vector_store import retriever


# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def ask_medical_ai(question: str):
    # Retrieve relevant documents
    docs = retriever.invoke(question)

    # Combine retrieved text into context
    context = "\n\n".join(doc.page_content for doc in docs)

    # Build prompt
    prompt = f"""
{SYSTEM_PROMPT}

Context:
{context}

Question:
{question}

Answer:
"""

    # Call Groq LLM
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
    )

    # Return answer and source documents
    return {
        "answer": response.choices[0].message.content,
        "sources": docs
    }