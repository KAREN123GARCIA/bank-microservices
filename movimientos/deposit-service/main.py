from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from pymongo import MongoClient
import requests
from datetime import datetime

app = FastAPI()

client = MongoClient("mongodb://mongodb:27017/")
db = client["bank"]
transactions = db["transactions"]

class DepositRequest(BaseModel):
    user_id: int
    account_id: int
    amount: float

@app.post("/webhook/deposit")
async def make_deposit(data: DepositRequest, request: Request):
    try:
        # 1. Obtener datos de la cuenta desde microservicio PostgreSQL
        response = requests.get(f"http://get-account-service:8086/account/{data.account_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")

        account = response.json()
        if account["state"] != "ACTIVE":
            raise HTTPException(status_code=400, detail="Cuenta no está activa")

        # 2. Actualizar el saldo en PostgreSQL
        nuevo_saldo = float(account["balance"]) + data.amount
        update_response = requests.put(
            f"http://get-account-service:8086/account/{data.account_id}",
            json={"balance": nuevo_saldo}
        )
        if update_response.status_code != 200:
            raise HTTPException(status_code=500, detail="Error al actualizar el saldo en PostgreSQL")

        # 3. Registrar en MongoDB
        txn = {
            "type": "deposit",
            "user_id": data.user_id,
            "account_id": data.account_id,
            "amount": data.amount,
            "timestamp": datetime.utcnow(),
            "status": "COMPLETED"
        }
        result = transactions.insert_one(txn)
        txn["_id"] = str(result.inserted_id)

        return {"message": "Depósito registrado con éxito", "transaction": txn}

    except Exception as e:
        print("❌ Error:", e)
        raise HTTPException(status_code=500, detail=str(e))
