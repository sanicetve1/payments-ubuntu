# config.py

# Absolute path to your Stripe DB file
import os
from dotenv import load_dotenv
load_dotenv()
RAG_VECTOR_PATH = os.getenv("RAG_VECTOR_PATH")

DB_PATH = "/app/stripe/stripe_test.db"
