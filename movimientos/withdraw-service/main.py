from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from datetime import datetime
from pymongo import MongoClient

app = FastAPI()

mongo_client = MongoClient("mongodb://mongodb:27017/")
db = mongo_client["bank"]
transactions = db["transactions"]

class WithdrawRequest(BaseModel):
    account_id: int
    amount: float

@app.post("/webhook/withdraw")
def withdraw_money(data: WithdrawRequest):
    res = requests.get(f"http://get-account-service:8086/account/{data.account_id}")
    if res.status_code != 200:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")

    cuenta = res.json()
    if cuenta["state"] != "ACTIVE":
        raise HTTPException(status_code=400, detail="Cuenta inactiva")
    if float(cuenta["balance"]) < data.amount:
        raise HTTPException(status_code=400, detail="Fondos insuficientes")

    nuevo_saldo = float(cuenta["balance"]) - data.amount
    res_update = requests.put(f"http://get-account-service:8086/account/{data.account_id}",
                              json={"balance": nuevo_saldo})
    if res_update.status_code != 200:
        raise HTTPException(status_code=500, detail="Error al actualizar el saldo")

    txn = {
        "type": "withdrawal",
        "account_id": data.account_id,
        "amount": data.amount,
        "timestamp": datetime.utcnow(),
        "status": "COMPLETED"
    }
    transactions.insert_one(txn)

    return {
        "message": "Retiro realizado con éxito",
        "transaction": txn
    }
# 👇 Agrega esto al final de tu main.py si no usas imagen tiangolo
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8094, reload=True)