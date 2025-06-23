# load_pdfs_once.py
from rag_loader import build_vector_store_from_pdfs

# Path where your PDFs are stored
pdf_path = "C:/Users/San/Desktop/Projects/Payments/Legal-documents"

# Build vector store
build_vector_store_from_pdfs(pdf_path)
