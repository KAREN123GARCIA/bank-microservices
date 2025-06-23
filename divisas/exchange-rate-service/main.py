from fastapi import FastAPI, Request, HTTPException
import asyncpg
from fastapi.responses import JSONResponse

app = FastAPI()

async def get_connection():
    return await asyncpg.connect(
        user='karen',
        password='2007',
        database='cuentas_db',
        host='postgres-login'
    )

@app.post("/webhook/exchange-rate")
async def exchange_rate(request: Request):
    data = await request.json()
    base = data.get("base", "USD")
    target = data.get("target", "EUR")

    conn = await get_connection()
    query = "SELECT rate FROM exchange_rates WHERE base_currency=$1 AND target_currency=$2"
    row = await conn.fetchrow(query, base, target)
    await conn.close()

    if row is None:
        raise HTTPException(status_code=404, detail="Tasa de cambio no encontrada")

    return JSONResponse(content={
        "base": base,
        "target": target,
        "rate": float(row["rate"])
    })
