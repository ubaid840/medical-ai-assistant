from pathlib import Path

from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


# -------------------------------------------------
# Paths
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
CHROMA_DIR = BASE_DIR / "chroma_db"


# -------------------------------------------------
# Build Vector Database
# -------------------------------------------------

def build_vector_database():
    """
    Creates ChromaDB vector database from PDF documents.
    """

    print("📄 Loading documents...")


    documents = []


    # Load all PDFs from data folder
    for file in DATA_DIR.glob("*.pdf"):

        loader = PyPDFLoader(
            str(file)
        )

        docs = loader.load()

        documents.extend(docs)


    if not documents:
        raise Exception(
            "No PDF files found in data folder"
        )


    print(
        f"Loaded documents: {len(documents)}"
    )


    # -------------------------------------------------
    # Text Splitting
    # -------------------------------------------------

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )


    chunks = splitter.split_documents(
        documents
    )


    print(
        f"Created chunks: {len(chunks)}"
    )


    # -------------------------------------------------
    # Embedding Model
    # -------------------------------------------------

    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )


    # -------------------------------------------------
    # Create Chroma Database
    # -------------------------------------------------

    db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(CHROMA_DIR)
    )


    print(
        "✅ ChromaDB created successfully"
    )


    return db



# -------------------------------------------------
# Run directly
# -------------------------------------------------

if __name__ == "__main__":

    build_vector_database()