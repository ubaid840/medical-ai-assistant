from langchain_chroma import Chroma
from langchain_community.embeddings import OllamaEmbeddings

embedding = OllamaEmbeddings(
    model="nomic-embed-text"
)

db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embedding
)

retriever = db.as_retriever(search_kwargs={"k": 3})

query = input("Ask a medical question: ")

docs = retriever.invoke(query)

print("\nRetrieved Documents:\n")

for i, doc in enumerate(docs, 1):
    print(f"Document {i}")
    print(doc.page_content)
    print("-"*60)