# tools/rag_tool.py

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.tools import Tool
import sys
#import torch
import types
import os
print("✅ LOADED: tools/rag_tool.py (LIVE)")

sys.modules["torch.classes"] = types.ModuleType("torch.classes")

from app.config import RAG_VECTOR_PATH

# 🔍 Core function to query the vector store with debug
def query_rag_tool(query: str) -> str:
    print(f"\n📂 [RAG] Using vector store at: {RAG_VECTOR_PATH}")
    if not os.path.exists(RAG_VECTOR_PATH):
        return f"❌ Vector store not found at {RAG_VECTOR_PATH}"

    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        db = Chroma(
            persist_directory=RAG_VECTOR_PATH,
            embedding_function=embeddings
        )

        print(f"🔎 [RAG] Searching for query: {query}")
        results = db.similarity_search_with_score(query, k=3)

        if not results:
            print("⚠️ [RAG] No results found in vector store.")
            return "❌ No relevant content found in documents."

        response_lines = []
        for i, (doc, score) in enumerate(results):
            print(f"\n--- Match {i+1} ---")
            print(f"🔢 Similarity Score: {score:.3f}")
            print(f"📄 Content Snippet: {doc.page_content[:300]}...")
            response_lines.append(f"[Score: {score:.2f}]\n{doc.page_content[:800]}")

        return "\n\n".join(response_lines)

    except Exception as e:
        print(f"❌ [RAG] Error during query: {e}")
        return f"❌ RAG query failed: {e}"

# 🛠️ Wrap as a LangChain Tool
rag_tool = Tool.from_function(
    name="query_rag",
    description="Use this when the query involves regulation, legal documents, onboarding policies, or compliance requirements.",
    func=query_rag_tool
)
