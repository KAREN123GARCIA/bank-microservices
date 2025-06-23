from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

client = MongoClient("mongodb://mongodb:27017/")
db = client["bank"]
transactions = db["transactions"]

@app.get("/webhook/transaction/{transaction_id}")
async def get_transaction_by_id(transaction_id: str):
    try:
        transaction = transactions.find_one({"_id": ObjectId(transaction_id)}, {"_id": 0})
        if not transaction:
            raise HTTPException(status_code=404, detail="Transacción no encontrada")
        return {"transaction": transaction}
    except Exception as e:
        raise HTTPException(status_code=400, detail="ID inválido o error de consulta")
