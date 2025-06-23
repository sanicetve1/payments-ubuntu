from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

def init_rag_store(persist_dir="./rag_store"):
    return Chroma(
        persist_directory=persist_dir,
        embedding_function=HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    )

def secure_rag_query(query: str, k: int = 5):
    store = init_rag_store()
    results = store.similarity_search(query, k=k)
    return [doc.metadata for doc in results]

def full_rag_query(query: str, k: int = 5):
    store = init_rag_store()
    results = store.similarity_search(query, k=k)
    return [doc.page_content for doc in results]
