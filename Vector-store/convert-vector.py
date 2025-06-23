# build_vectorstore_from_payments.py

import sqlite3
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.schema import Document
import os

# --- Config ---
DB_PATH = "C:/Users/San/Desktop/projects/Payments/stripe/stripe_test.db"  # update if needed
PERSIST_DIR = "./rag_store"

# --- Load all payments from SQLite ---
def load_payments():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM payments")
    rows = cur.fetchall()
    conn.close()
    return rows

# --- Convert each row to a LangChain Document ---
def format_as_document(row):
    text = (
        f"Payment ID: {row['id']}\n"
        f"Customer ID: {row['customer_id']}\n"
        f"Amount: {row['amount']}\n"
        f"Currency: {row['currency']}\n"
        f"Method: {row['payment_method']}\n"
        f"Status: {row['status']}\n"
        f"Description: {row['description']}\n"
        f"Is Fraudulent: {row['is_fraudulent']}\n"
        f"Disputed: {row['disputed']}\n"
        f"Created: {row['created']}"
    )
    return Document(page_content=text, metadata={
        "payment_id": row["id"],
        "customer_id": row["customer_id"],
        "amount": row["amount"]
    })

# --- Main logic to embed and store in Chroma vector DB ---
def build_vectorstore():
    print("🔍 Loading payment records...")
    rows = load_payments()
    print(f"✅ Fetched {len(rows)} rows from DB")

    documents = [format_as_document(row) for row in rows]

    print("🔁 Embedding using Hugging Face (all-MiniLM-L6-v2)...")
    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("📦 Storing in Chroma vector store...")
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory=PERSIST_DIR
    )
    vectorstore.persist()
    print(f"✅ Vector store created with {len(documents)} documents at: {PERSIST_DIR}")

if __name__ == "__main__":
    build_vectorstore()
