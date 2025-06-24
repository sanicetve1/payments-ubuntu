# Dockerfile for unified FastAPI (Uvicorn) + Streamlit + RAG app
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libopenblas-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app
RUN chmod +x start.sh

# Upgrade pip and install requirements
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Set environment vars (for Streamlit)
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Expose ports for FastAPI and Streamlit
EXPOSE 8000 8501

# Run both FastAPI and Streamlit via shell script
CMD ["bash", "-c", "./start.sh"]


