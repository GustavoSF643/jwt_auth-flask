from flask import Flask
from flask_migrate import Migrate


def init_app(app: Flask):
    from app.models import user_model

    Migrate(app, app.db)