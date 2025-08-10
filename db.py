from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from datetime import datetime

BASE = declarative_base()
DB_PATH = os.path.join(os.path.dirname(__file__), "ebs_demo.db")
ENGINE = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=ENGINE)

class User(BASE):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="viewer")
    created_at = Column(DateTime, default=datetime.utcnow)

class Audit(BASE):
    __tablename__ = "audit"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    action = Column(String, nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

def init_db():
    if not os.path.exists(DB_PATH):
        BASE.metadata.create_all(bind=ENGINE)

def get_session():
    return SessionLocal()

def create_sample_data():
    session = get_session()
    if session.query(User).count() == 0:
        import hashlib
        admin = User(username="admin", email="admin@example.com", password_hash=hashlib.sha256("admin".encode()).hexdigest(), role="admin")
        finance = User(username="finance_user", email="finance@example.com", password_hash=hashlib.sha256("12345".encode()).hexdigest(), role="finance")
        viewer = User(username="viewer", email="viewer@example.com", password_hash=hashlib.sha256("123".encode()).hexdigest(), role="viewer")
        session.add_all([admin, finance, viewer])
        session.commit()
    session.close()
