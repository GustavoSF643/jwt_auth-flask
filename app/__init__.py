from flask import Flask

from app.blueprints import user_blueprint
from app.configs import database, env_configs, migration, jwt


def create_app():
    app = Flask(__name__)

    env_configs.init_app(app)
    jwt.init_app(app)
    database.init_app(app)
    migration.init_app(app)

    app.register_blueprint(user_blueprint.bp_user)

    return app
