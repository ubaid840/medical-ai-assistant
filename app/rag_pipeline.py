from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    Docx2txtLoader,
    CSVLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_loader(file_path):
    ext = Path(file_path).suffix.lower()
    if ext == '.pdf':
        return PyPDFLoader(str(file_path))
    elif ext == '.txt':
        return TextLoader(str(file_path))
    elif ext == '.docx':
        return Docx2txtLoader(str(file_path))
    elif ext == '.csv':
        return CSVLoader(str(file_path))
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def load_documents(data_dir):

    documents = []
    
    extensions = ['*.pdf', '*.txt', '*.docx', '*.csv']
    all_files = []
    for ext in extensions:
        all_files.extend(Path(data_dir).glob(ext))

    for file_path in all_files:
        try:
            loader = get_loader(file_path)
            docs = loader.load()
            documents.extend(docs)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")

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



def create_chunks_for_file(file_path):

    loader = get_loader(file_path)

    docs = loader.load()

    chunks = split_documents(docs)

    return chunks