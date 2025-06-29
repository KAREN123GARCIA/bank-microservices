from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from datetime import datetime
from collections import defaultdict

app = FastAPI()

client = MongoClient("mongodb://mongodb:27017/")
db = client["bank"]
transactions = db["transactions"]

@app.get("/webhook/alerts/{account_id}")
async def detect_anomalies(account_id: int):
    txns = list(transactions.find(
        { "$or": [ {"account_id": account_id}, {"source_account_id": account_id} ] }
    ))

    if not txns:
        raise HTTPException(status_code=404, detail="No hay transacciones para esta cuenta")

    anomalías = []

    conteo_por_día = defaultdict(list)

    for txn in txns:
        fecha = txn["timestamp"].date()
        monto = txn["amount"]

        # Regla 1: Monto muy alto
        if monto > 10000:
            anomalías.append({
                "tipo": txn.get("type"),
                "monto": monto,
                "fecha": txn["timestamp"],
                "razón": "Monto mayor a $10,000"
            })

        # Agrupar para regla 2
        conteo_por_día[fecha].append(monto)

    # Regla 2: Muchas transacciones grandes en un día
    for fecha, montos in conteo_por_día.items():
        grandes = [m for m in montos if m > 2000]
        if len(grandes) >= 3:
            anomalías.append({
                "fecha": fecha,
                "total_grandes": len(grandes),
                "razón": "Más de 3 transacciones grandes en un día"
            })

    return {"alertas": anomalías}

# 🔥 Esto es esencial para que el contenedor arranque correctamente
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8093)
