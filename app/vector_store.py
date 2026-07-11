import streamlit as st
from pathlib import Path
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

BASE_DIR = Path(__file__).resolve().parent.parent
CHROMA_DIR = BASE_DIR / "chroma_db"


@st.cache_resource
def get_retriever():

    embedding = OllamaEmbeddings(
        model="nomic-embed-text"
    )

    db = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding,
    )

    return db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 8},
    )


retriever = get_retriever()