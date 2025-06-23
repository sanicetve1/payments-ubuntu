#!/bin/bash

echo "🚀 Starting FastAPI backend on port 8000..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

echo "🎨 Launching Streamlit UI on port 8501..."
streamlit run ui/AgentUI.py

