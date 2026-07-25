from langchain_chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

from config import (
    CHROMA_DB_DIR,
    EMBEDDING_MODEL,
    TOP_K
)

from rag_pipeline import create_chunks, create_chunks_for_file
import streamlit as st

@st.cache_resource
def get_cached_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def build_vector_database(data_dir):

    print("Loading documents...")

    chunks = create_chunks(data_dir)

    print(f"Chunks created: {len(chunks)}")

    if not chunks:
        print("No valid documents found to index.")
        return None

    embeddings = get_cached_embeddings()

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DB_DIR)
    )

    print("Vector database updated successfully.")

    return db



def get_retriever():

    embeddings = get_cached_embeddings()

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

    embeddings = get_cached_embeddings()

    db = Chroma(
        persist_directory=str(CHROMA_DB_DIR),
        embedding_function=embeddings
    )

    db.add_documents(documents=chunks)

    print("Document added to vector database.")


def delete_document_from_db(filename):
    print(f"Deleting document {filename} from vector database...")
    embeddings = get_cached_embeddings()
    db = Chroma(persist_directory=str(CHROMA_DB_DIR), embedding_function=embeddings)
    
    try:
        # Get all documents
        collection = db._collection
        
        # We need to find the IDs of the chunks that belong to this file.
        # Collection.get() returns dict with 'ids' and 'metadatas'
        # Then we delete those specific IDs.
        results = collection.get()
        ids_to_delete = []
        
        if results and "metadatas" in results:
            for idx, metadata in zip(results["ids"], results["metadatas"]):
                if metadata and metadata.get("source"):
                    if filename in metadata.get("source"):
                        ids_to_delete.append(idx)
                        
        if ids_to_delete:
            collection.delete(ids=ids_to_delete)
            print(f"Deleted {len(ids_to_delete)} chunks from vector database.")
        else:
            print("No matching chunks found to delete.")
            
    except Exception as e:
        print(f"Error deleting from vector database: {e}")