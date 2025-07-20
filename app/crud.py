from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hashing password
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Create a new user
def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = hash_password(user.password)
    db_user = models.User(email=user.email, password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Authenticate user
def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password):
        return None
    return user

# Create an admin user (manually in script or seeded)
def create_admin(db: Session, admin: schemas.AdminCreate):
    hashed_pw = hash_password(admin.password)
    db_admin = models.Admin(email=admin.email, password=hashed_pw)
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin

# Authenticate admin
def authenticate_admin(db: Session, email: str, password: str):
    admin = db.query(models.Admin).filter(models.Admin.email == email).first()
    if not admin or not verify_password(password, admin.password):
        return None
    return admin

# Get user by ID
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Update user profit
def update_profit(db: Session, user_id: int, profit: float):
    user = get_user(db, user_id)
    if user:
        user.profit = profit
        db.commit()
        db.refresh(user)
    return user

# Get all users (for admin dashboard)
def get_all_users(db: Session):
    return db.query(models.User).all()

# Create a contact message
def create_contact_message(db: Session, message: schemas.ContactCreate):
    db_message = models.ContactMessage(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message
