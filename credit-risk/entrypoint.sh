#!/bin/bash
set -e

echo "Starting FastAPI on port 8000..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

echo "Starting Streamlit on port ${PORT:-8501}..."
streamlit run app/app.py \
  --server.port ${PORT:-8501} \
  --server.address 0.0.0.0 \
  --server.headless true \
  --server.enableCORS false