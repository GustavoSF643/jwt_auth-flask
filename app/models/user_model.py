import secrets
from dataclasses import dataclass

from app.configs.database import db
from app.configs.auth import auth
from app.exceptions.user_exc import WrongPasswordError
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
    api_key = Column(String(511), nullable=False)

    @property
    def password(self):
        raise AttributeError('Password cannot be accessed!')

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = generate_password_hash(password_to_hash)

    def verify_password(self, password_to_compare):
        if not check_password_hash(self.password_hash, password_to_compare):
            raise WrongPasswordError('Password is wrong.')

    @auth.verify_token
    def verify_token(token):
        user = UserModel.query.filter_by(api_key=token).first()
        if user:
            return user

    def save(self):
        session = current_app.db.session
        session.add(self)
        session.commit()

    def create_api_key(self):
        api_key = secrets.token_hex()
        self.api_key = api_key

    def update_user(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        
    def delete_user(self):
        session = current_app.db.session
        session.delete(self)
        session.commit()