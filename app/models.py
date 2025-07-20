from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import bcrypt

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Optional relationship if you track support messages etc
    # support_messages = relationship("SupportMessage", back_populates="user")

    def verify_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode(), self.hashed_password.encode())

    @staticmethod
    def hash_password(plain_password: str) -> str:
        hashed = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())
        return hashed.decode()

# You can add more models like SupportMessage, Transactions, etc. if needed