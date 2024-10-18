FROM python:3.12-slim

WORKDIR /app

# Define build arguments for model selection
ARG TEXT_EMBEDDING_MODEL="BAAI/bge-small-en-v1.5"
ARG IMAGE_EMBEDDING_MODEL="Qdrant/clip-ViT-B-32-vision"

# Set environment variables from build arguments
ENV TEXT_EMBEDDING_MODEL=$TEXT_EMBEDDING_MODEL
ENV IMAGE_EMBEDDING_MODEL=$IMAGE_EMBEDDING_MODEL

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the model download script
COPY download_models.py .

# Run the model download script
RUN python download_models.py

# Copy the FastAPI application
COPY . .

# Set environment variables with default values for FastAPI
ENV FASTAPI_HOST=0.0.0.0
ENV FASTAPI_PORT=8000

# Expose the port the app runs on
EXPOSE $FASTAPI_PORT

# Command to run the application
CMD ["python", "main.py"]
