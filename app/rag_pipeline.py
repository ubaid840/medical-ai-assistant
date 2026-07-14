from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def load_documents(data_dir):

    documents = []

    pdf_files = Path(data_dir).glob("*.pdf")

    for pdf in pdf_files:

        loader = PyPDFLoader(str(pdf))

        docs = loader.load()

        documents.extend(docs)

    return documents



def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_documents(documents)

    return chunks



def create_chunks(data_dir):

    documents = load_documents(data_dir)

    chunks = split_documents(documents)

    return chunks



def create_chunks_for_file(pdf_path):

    loader = PyPDFLoader(str(pdf_path))

    docs = loader.load()

    chunks = split_documents(docs)

    return chunks