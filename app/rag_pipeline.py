from groq import Groq

from config import GROQ_API_KEY, LLM_MODEL
from prompts import SYSTEM_PROMPT
from vector_store import retriever

client = Groq(api_key=GROQ_API_KEY)


def ask_question(question: str):

    docs = retriever.invoke(question)

    print("=" * 60)
    print("QUESTION:", question)
    print("Retrieved:", len(docs))

    context = ""

    for i, doc in enumerate(docs):
        print(f"\nChunk {i+1}")
        print(doc.page_content[:300])
        context += doc.page_content + "\n\n"

    if context.strip() == "":
        return (
            "I couldn't find this information in the uploaded medical documents.",
            docs,
        )

    prompt = f"""
Use ONLY the medical context below.

If the answer is unavailable, say:
"I couldn't find this information in the uploaded medical documents."

Medical Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=0.2,
        max_tokens=700,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )

    answer = response.choices[0].message.content

    return answer, docs