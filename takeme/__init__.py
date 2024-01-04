from flask import Flask

from takeme.api import api_bp
from takeme.crypto import bcrypt
from takeme.database import database, migrate
from takeme.login import jwt, login_manager
from takeme.ui import ui_bp


class Config(object):
    TESTING = False
    DEBUG = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BCRYPT_LOG_ROUNDS = 13
    WTF_CSRF_ENABLED = True
    SECRET_KEY = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_SECRET_KEY = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"
    JWT_COOKIE_SECURE = False


class ProductionConfig(Config):
    DATABASE_URI = "sqlite:///db.sqlite"


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    WTF_CSRF_ENABLED = False
    DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 1
    WTF_CSRF_ENABLED = False
    DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_DATABASE_URI = "sqlite:///testdb.sqlite"


def create_app() -> Flask:
    app = Flask(__name__)

    cfg = DevelopmentConfig()
    app.config.from_object(cfg)

    jwt.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    database.init_app(app)
    migrate.init_app(app, db=database)

    with app.app_context():
        database.create_all()

    app.register_blueprint(ui_bp, url_prefix="/")
    app.register_blueprint(api_bp, url_prefix="/api")

    return app