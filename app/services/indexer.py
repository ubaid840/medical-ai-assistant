import shutil

from vector_store import build_vector_database
from config import (
    DATA_DIR,
    CHROMA_DB_DIR,
)


def rebuild_index():
    """
    Rebuild the complete Chroma database
    from all PDFs inside DATA_DIR.
    """

    if CHROMA_DB_DIR.exists():
        shutil.rmtree(CHROMA_DB_DIR)

    CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)

    build_vector_database(DATA_DIR)


def index_after_upload():
    """
    Called after uploading a PDF.
    """

    rebuild_index()


def index_after_delete():
    """
    Called after deleting a PDF.
    """

    rebuild_index()