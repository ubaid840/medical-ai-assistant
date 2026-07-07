from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_groq import ChatGroq

from langchain_classic.chains.combine_documents import (
    create_stuff_documents_chain,
)
from langchain_classic.chains import create_retrieval_chain

from app.config import (
    CHROMA_DB_DIR,
    EMBEDDING_MODEL,
    LLM_MODEL,
    TOP_K,
)

from app.prompts import QA_PROMPT

# Embedding model
embedding = OllamaEmbeddings(
    model=EMBEDDING_MODEL
)

# Vector Database
vectorstore = Chroma(
    persist_directory=str(CHROMA_DB_DIR),
    embedding_function=embedding,
)

# Retriever
retriever = vectorstore.as_retriever(
    search_kwargs={"k": TOP_K}
)

# Groq LLM
llm = ChatGroq(
    model=LLM_MODEL,
    temperature=0,
)

# Document Chain
document_chain = create_stuff_documents_chain(
    llm,
    QA_PROMPT,
)

# Retrieval Chain
rag_chain = create_retrieval_chain(
    retriever,
    document_chain,
)

print("=" * 60)
print("Medical AI Assistant")
print("=" * 60)

while True:
    question = input("\nAsk a medical question (type 'exit'): ")

    if question.lower() == "exit":
        break

    response = rag_chain.invoke(
        {
            "input": question
        }
    )

    print("\nAnswer:\n")
    print(response["answer"])