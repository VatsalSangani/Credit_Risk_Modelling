# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy dependencies and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code and model artifacts
COPY app ./app
COPY artifacts ./artifacts

# Expose both Streamlit (8501) and FastAPI (8000)
EXPOSE 8501
EXPOSE 8000

# Run both FastAPI and Streamlit apps
CMD exec sh -c "\
  uvicorn app.main:app --host 0.0.0.0 --port 8000 & \
  streamlit run app/app.py --server.port 8501 --server.address 0.0.0.0"

