import secrets
from dataclasses import dataclass

from app.configs.database import db
from app.exceptions.user_exc import InvalidKeysError, WrongPasswordError
from flask import current_app
from sqlalchemy import Column, Integer, String
from werkzeug.security import check_password_hash, generate_password_hash


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

    @property
    def password(self):
        raise AttributeError('Password cannot be accessed!')

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        if not check_password_hash(self.password_hash, password_to_compare):
            raise WrongPasswordError('Password is wrong.')

    def save(self):
        session = current_app.db.session
        session.add(self)
        session.commit()

    def update_user(self, data):
        try:
            UserModel(**data)
        except TypeError:
            keys = ('name', 'last_name', 'email', 'password')
            raise InvalidKeysError(f"Invalid Keys in body. Accepted Keys:{', '.join(keys)}")

        for key, value in data.items():
            setattr(self, key, value)
        
    def delete_user(self):
        session = current_app.db.session
        session.delete(self)
        session.commit()