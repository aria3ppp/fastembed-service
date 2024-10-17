FROM python:3.12-slim

WORKDIR /app

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

# Set environment variables with default values
ENV FASTAPI_HOST=0.0.0.0
ENV FASTAPI_PORT=8000

# Expose the port the app runs on
EXPOSE $FASTAPI_PORT

# Command to run the application
CMD ["python", "main.py"]