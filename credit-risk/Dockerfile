# Use python 3.10 slim to keep size down
FROM python:3.10-slim

WORKDIR /app

# Install basic utilities and clean up immediately to save space
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your code and artifacts
COPY app ./app
COPY artifacts ./artifacts

# Copy the entrypoint script and make it executable
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Expose the necessary ports
EXPOSE 8000
EXPOSE 8501

# Use the script to start the app
ENTRYPOINT ["./entrypoint.sh"]
