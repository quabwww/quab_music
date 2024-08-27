FROM python:3.11-slim
RUN apt-get update && apt-get install -y ffmpeg gcc
WORKDIR /app
COPY . .
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /app
CMD ls -la && cat /app/main.py && echo "Starting Uvicorn..." && uvicorn main:app --host 0.0.0.0 --port 8000
