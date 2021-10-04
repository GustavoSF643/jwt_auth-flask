from os import environ

from dotenv import load_dotenv
from flask import Flask

load_dotenv()


def init_app(app: Flask):
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = bool(environ.get('SQLALCHEMY_TRACK_MODIFICATIONS'))
    app.config['JSON_SORT_KEYS'] = environ.get('JSON_SORT_KEYS')