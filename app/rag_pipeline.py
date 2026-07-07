print("🔥 RAG PIPELINE STARTED")

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader

docs = []

for pdf in Path("../data").glob("*.pdf"):
    print(f"Loading: {pdf.name}")
    loader = PyPDFLoader(str(pdf))
    docs.extend(loader.load())

print(f"Total Pages: {len(docs)}")

print(f"Pages: {len(docs)}")

# Split text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = splitter.split_documents(docs)

print(f"Chunks: {len(chunks)}")

# Embedding model
embedding = OllamaEmbeddings(model="nomic-embed-text")

# Store in vector DB
db = Chroma.from_documents(
    documents=chunks,
    embedding=embedding,
    persist_directory="chroma_db"
)

print("✅ RAG setup complete")