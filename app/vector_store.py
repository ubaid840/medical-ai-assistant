from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from config import (
    EMBEDDING_MODEL,
    CHROMA_DB_DIR,
)

# Create embedding model
embedding = OllamaEmbeddings(
    model=EMBEDDING_MODEL
)

# Load existing Chroma database
vector_db = Chroma(
    persist_directory=str(CHROMA_DB_DIR),
    embedding_function=embedding
)

# Create retriever
retriever = vector_db.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 3,
        "fetch_k": 10,
        "lambda_mult": 0.7
    }
)