from pydantic import BaseModel, EmailStr
from typing import Optional

# User Schemas
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    profit: Optional[float] = None
    class Config:
        from_attributes = True

# Admin Schemas
class AdminBase(BaseModel):
    email: EmailStr

class AdminCreate(AdminBase):
    password: str

# Contact Form Schema
class ContactCreate(BaseModel):
    name: str
    email: EmailStr
    subject: str
    message: str