from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

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
    search_kwargs={"k": 3}
)