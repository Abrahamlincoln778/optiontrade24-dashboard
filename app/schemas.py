from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class ProfitResponse(BaseModel):
    username: str
    balance: float
    daily_profit: float


class AdminUpdate(BaseModel):
    username: str
    balance: Optional[float] = None
    daily_profit: Optional[float] = None
