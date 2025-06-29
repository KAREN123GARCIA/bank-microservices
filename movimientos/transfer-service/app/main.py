from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from datetime import datetime
from pymongo import MongoClient

app = FastAPI()

# Conexión a MongoDB
mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["bank"]
transactions = db["transactions"]

# Modelo de solicitud
class TransferRequest(BaseModel):
    source_account_id: int
    target_account_id: int
    amount: float

@app.post("/webhook/transfer")
def transfer_money(data: TransferRequest):
    # Verificar cuenta origen
    res_src = requests.get(f"http://get-account-service:8086/account/{data.source_account_id}")
    if res_src.status_code != 200:
        raise HTTPException(status_code=404, detail="Cuenta origen no encontrada")
    cuenta_origen = res_src.json()
    if cuenta_origen["state"] != "ACTIVE":
        raise HTTPException(status_code=400, detail="Cuenta origen inactiva")
    if float(cuenta_origen["balance"]) < data.amount:
        raise HTTPException(status_code=400, detail="Fondos insuficientes")

    # Verificar cuenta destino
    res_dst = requests.get(f"http://get-account-service:8086/account/{data.target_account_id}")
    if res_dst.status_code != 200:
        raise HTTPException(status_code=404, detail="Cuenta destino no encontrada")
    cuenta_destino = res_dst.json()
    if cuenta_destino["state"] != "ACTIVE":
        raise HTTPException(status_code=400, detail="Cuenta destino inactiva")

    # Calcular nuevos saldos
    nuevo_saldo_origen = float(cuenta_origen["balance"]) - data.amount
    nuevo_saldo_destino = float(cuenta_destino["balance"]) + data.amount

    # Actualizar cuenta origen
    res_update_src = requests.put(
        f"http://get-account-service:8086/account/{data.source_account_id}",
        json={"balance": nuevo_saldo_origen}
    )
    if res_update_src.status_code != 200:
        raise HTTPException(status_code=500, detail="Error actualizando cuenta origen")

    # Actualizar cuenta destino
    res_update_dst = requests.put(
        f"http://get-account-service:8086/account/{data.target_account_id}",
        json={"balance": nuevo_saldo_destino}
    )
    if res_update_dst.status_code != 200:
        raise HTTPException(status_code=500, detail="Error actualizando cuenta destino")

    # Registrar en MongoDB
    txn = {
        "type": "transfer",
        "source_account_id": data.source_account_id,
        "target_account_id": data.target_account_id,
        "amount": data.amount,
        "timestamp": datetime.utcnow(),
        "status": "COMPLETED"
    }
    transactions.insert_one(txn)

    return {
        "message": "Transferencia realizada con éxito",
        "transaction": {
            "source_account_id": data.source_account_id,
            "target_account_id": data.target_account_id,
            "amount": data.amount,
            "status": "COMPLETED"
        }
    }
