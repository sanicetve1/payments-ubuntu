from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma(persist_directory="/Payments/Legal-documents/rag_vectorstore_local", embedding_function=embeddings)

print("[✅] RAG store loaded successfully")

