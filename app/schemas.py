from pydantic import BaseModel, EmailStr
from typing import Optional

# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr

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
    email: EmailStr

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

# Contact Form Schemas
class ContactBase(BaseModel):
    name: str
    email: EmailStr
    subject: str

class ContactCreate(ContactBase):
    message: str

# Profit/Financial Schemas
class ProfitResponse(BaseModel):
    username: str
    balance: float
    daily_profit: float