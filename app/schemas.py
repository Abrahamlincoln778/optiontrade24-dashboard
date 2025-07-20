from pydantic import BaseModel
from typing import Optional

# User Schemas
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class User(UserBase):
    id: int
    class Config:
        from_attributes = True

# Admin Schemas
class AdminBase(BaseModel):
    username: str
    email: str

class AdminCreate(AdminBase):
    password: str

class AdminUpdate(BaseModel):
    username: Optional[str] = None
    balance: Optional[float] = None
    daily_profit: Optional[float] = None

class Admin(AdminBase):
    id: int
    class Config:
        from_attributes = True

# Other Schemas
class ProfitResponse(BaseModel):
    username: str
    balance: float
    daily_profit: float