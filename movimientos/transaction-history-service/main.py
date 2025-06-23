from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from bson import ObjectId

app = FastAPI()

client = MongoClient("mongodb://mongodb:27017/")
db = client["bank"]
transactions = db["transactions"]

def serialize_transaction(txn):
    txn["_id"] = str(txn["_id"])
    return txn

@app.get("/webhook/transaction-history/{account_id}")
async def get_transaction_history(account_id: int):
    history_cursor = transactions.find({
        "$or": [
            {"account_id": account_id},
            {"source_account_id": account_id},
            {"target_account_id": account_id}
        ]
    })
    history = [serialize_transaction(t) for t in history_cursor]
    
    if not history:
        raise HTTPException(status_code=404, detail="No se encontraron transacciones para esta cuenta")
    
    return {"transactions": history}
