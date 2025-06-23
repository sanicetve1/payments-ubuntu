# rag_mode.py

# Toggle to enable full RAG (send context to GPT) or secure RAG (do not send data to GPT)
# This sets the environment variable dynamically for your agent script

import os

def set_rag_mode(full: bool = False):
    if full:
        os.environ["USE_FULL_RAG"] = "true"
        print("✅ Full RAG mode enabled: data will be sent to GPT.")
    else:
        os.environ["USE_FULL_RAG"] = "false"
        print("🔒 Secure RAG mode enabled: no data will be sent to GPT.")
