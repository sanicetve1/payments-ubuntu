# rag_query.py
from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

PERSIST_DIR = "rag_vectorstore_local"

def query_vector_store_local(question: str, top_k: int = 3):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = Chroma(persist_directory=PERSIST_DIR, embedding_function=embeddings)

    print(f"🔍 Searching for: {question}")
    results = vectordb.similarity_search(question, k=top_k)

    print(f"🔎 Top {top_k} relevant chunks:\n")
    for i, doc in enumerate(results):
        print(f"--- Result {i+1} ---")
        print(doc.page_content[:800])  # Limit to first 800 chars
        print()

if __name__ == "__main__":
    query = input("❓ Enter your test query: ")
    query_vector_store_local(query)

