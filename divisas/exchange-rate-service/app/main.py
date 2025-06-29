from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

DB_HOST = os.getenv("DB_HOST", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "movimientos_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

class ExchangeRateEvent(BaseModel):
    currency_from: str
    currency_to: str
    rate: float

@app.post("/webhook/exchange-rate")
async def receive_exchange_rate(event: ExchangeRateEvent):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exchange_rates (
                id SERIAL PRIMARY KEY,
                currency_from VARCHAR(10),
                currency_to VARCHAR(10),
                rate NUMERIC,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        cursor.execute(
            "INSERT INTO exchange_rates (currency_from, currency_to, rate) VALUES (%s, %s, %s)",
            (event.currency_from.upper(), event.currency_to.upper(), event.rate)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return {"status": "ok", "message": "Exchange rate received"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
