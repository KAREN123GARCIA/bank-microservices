FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir fastapi uvicorn pymongo requests

EXPOSE 8094

CMD ["python", "main.py"]
