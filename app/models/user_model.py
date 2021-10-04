from dataclasses import dataclass
from app.configs.database import db
from sqlalchemy import Column, Integer, String


@dataclass
class UserModel(db.Model):
    name: str
    last_name: str
    email: str

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(127), nullable=False)
    last_name = Column(String(511), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(511), nullable=False)
    api_key = Column(String(511), nullable=False)
