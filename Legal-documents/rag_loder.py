# rag_loader.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

PDF_FOLDER = r"C:\Users\San\Desktop\Projects\Payments\Legal-documents"
PERSIST_DIR = "rag_vectorstore_local"

def build_local_vector_store():
    documents = []
    for file in os.listdir(PDF_FOLDER):
        if file.lower().endswith(".pdf"):
            print(f"📄 Loading {file}")
            loader = PyPDFLoader(os.path.join(PDF_FOLDER, file))
            documents.extend(loader.load())

    print(f"📚 Loaded {len(documents)} pages.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = splitter.split_documents(documents)
    print(f"✂️ Split into {len(chunks)} chunks.")

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vectordb = Chroma.from_documents(chunks, embedding=embeddings, persist_directory=PERSIST_DIR)
    vectordb.persist()
    print(f"✅ Vector store created at '{PERSIST_DIR}' with {len(chunks)} chunks.")

if __name__ == "__main__":
    build_local_vector_store()
