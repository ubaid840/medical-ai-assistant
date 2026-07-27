import shutil

from config import DATA_DIR, CHROMA_DB_DIR
from vector_store import build_vector_database


def save_document(uploaded_file):
    """
    Save uploaded PDF into data folder
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    file_path = DATA_DIR / uploaded_file.name

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path


def list_documents():
    """
    Return all uploaded PDF documents as Path objects
    """

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    return list(DATA_DIR.glob("*.pdf"))


def delete_document(file_name):
    """
    Delete selected PDF document
    """

    file_path = DATA_DIR / file_name

    if file_path.exists():
        file_path.unlink()

    return True


def delete_all_documents():
    """
    Delete all uploaded PDF documents
    """

    if DATA_DIR.exists():
        for file in DATA_DIR.glob("*.pdf"):
            file.unlink()

    if CHROMA_DB_DIR.exists():
        shutil.rmtree(CHROMA_DB_DIR)

    return True


def index_after_upload():
    """
    Rebuild vector database after upload
    """

    build_vector_database()


def index_after_delete():
    """
    Rebuild vector database after deletion
    """

    build_vector_database()