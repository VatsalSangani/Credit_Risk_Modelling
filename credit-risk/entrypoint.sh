#!/bin/bash
set -e

# 1. Start FastAPI in the background
# We log output to a file so we can debug it later if needed
echo "Starting FastAPI..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 > /var/log/fastapi.log 2>&1 &

# 2. Start Streamlit in the foreground
# Streamlit needs to stay running to keep the container alive
echo "Starting Streamlit..."
streamlit run app/app.py --server.port 8501 --server.address 0.0.0.0
