FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install fastapi uvicorn pymongo

EXPOSE 8093

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8093"]
