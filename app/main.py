from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid

app = FastAPI()

# Allow frontend from any domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database (temporary)
users_db: Dict[str, Dict] = {}

# Models
class User(BaseModel):
    username: str
    email: str

class ProfitUpdate(BaseModel):
    username: str
    profit: float

@app.post("/register")
def register(user: User):
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="Username already exists")
    users_db[user.username] = {
        "email": user.email,
        "profit": 0.0,
        "joined": datetime.now().isoformat()
    }
    return {"message": "User registered successfully", "data": users_db[user.username]}

@app.get("/profit/{username}")
def get_profit(username: str):
    if username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return {
        "username": username,
        "profit": users_db[username]["profit"],
        "email": users_db[username]["email"],
        "joined": users_db[username]["joined"]
    }

@app.post("/admin/update-profit")
def update_profit(data: ProfitUpdate):
    if data.username not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    users_db[data.username]["profit"] += data.profit
    return {"message": f"Profit updated for {data.username}", "new_profit": users_db[data.username]["profit"]}
