from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from config import (
    CHROMA_DB_DIR,
    DATA_DIR,
    EMBEDDING_MODEL,
)


def build_vector_database():
    """
    Creates ChromaDB vector database from PDF documents.
    """

    print("📄 Loading documents...")

    documents = []

    # Load all PDFs
    for file in DATA_DIR.glob("*.pdf"):
        loader = PyPDFLoader(str(file))
        docs = loader.load()
        documents.extend(docs)

    if not documents:
        raise Exception("No PDF files found in data folder")

    print(f"Loaded documents: {len(documents)}")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
    )

    chunks = splitter.split_documents(documents)

    print(f"Created chunks: {len(chunks)}")

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_DIR),
    )

    print("✅ ChromaDB created successfully")

    return db


if __name__ == "__main__":
    build_vector_database()