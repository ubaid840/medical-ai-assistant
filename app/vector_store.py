from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from config import (
    CHROMA_DB_DIR,
    EMBEDDING_MODEL,
    TOP_K
)

from rag_pipeline import create_chunks, create_chunks_for_file


def build_vector_database(data_dir):

    print("Loading documents...")

    chunks = create_chunks(data_dir)

    print(f"Chunks created: {len(chunks)}")

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_DIR)
    )

    print("Vector database updated successfully.")

    return db



def get_retriever():

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )

    db = Chroma(
        persist_directory=str(CHROMA_DB_DIR),
        embedding_function=embeddings
    )

    retriever = db.as_retriever(
        search_kwargs={
            "k": TOP_K
        }
    )

    return retriever



def add_document_to_db(pdf_path):

    print(f"Loading document {pdf_path}...")

    chunks = create_chunks_for_file(pdf_path)

    print(f"Chunks created for new file: {len(chunks)}")

    embeddings = OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )

    db = Chroma(
        persist_directory=str(CHROMA_DB_DIR),
        embedding_function=embeddings
    )

    db.add_documents(documents=chunks)

    print("Document added to vector database.")