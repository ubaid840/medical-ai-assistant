print("🔥 RAG PIPELINE STARTED")

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

# Load PDF
loader = PyPDFLoader("../data/diabetes.pdf")
docs = loader.load()

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