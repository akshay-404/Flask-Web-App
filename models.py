from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text
from passlib.hash import argon2

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    kvs = relationship("UserKV", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password: str):
        self.password_hash = argon2.hash(password)

    def check_password(self, password: str) -> bool:
        try:
            return argon2.verify(password, self.password_hash)
        except Exception:
            return False

class UserKV(Base):
    __tablename__ = "user_kv"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    k = Column(String(128), nullable=False)
    v_hash = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="kvs")
