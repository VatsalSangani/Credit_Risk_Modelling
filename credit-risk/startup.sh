#!/bin/bash
# Start FastAPI backend in background
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start Streamlit frontend (Azure serves on WEBSITES_PORT=8501)
streamlit run app/app.py --server.port 8501 --server.address 0.0.0.0 --server.headless true