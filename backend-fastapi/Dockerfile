FROM python:3.11-slim

# Create non-root user
RUN useradd -m appuser
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Copy shared data (will be mounted in compose)
COPY ../shared-data /app/shared-data

# Copy .env.production as .env
COPY .env.production .env

USER appuser
EXPOSE 8000
ENV ENV=production
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 