from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email, name=user.name, balance=0.0, profit=0.0)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_profit(db: Session, user_id: int, amount: float):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.profit += amount
        db_user.balance += amount
        db.commit()
        db.refresh(db_user)
    return db_user

def reset_user_profit(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if db_user:
        db_user.profit = 0.0
        db.commit()
        db.refresh(db_user)
    return db_user
