from datetime import datetime

from flask import Flask
from sqlalchemy.exc import NoResultFound

from takeme.crypto import bcrypt
from takeme.database import User, database, migrate
from takeme.login import login_manager
from takeme.scheduler import scheduler
from takeme.ui import ui_bp


class AppConfig(object):
    BCRYPT_LOG_ROUNDS = 13
    CSRF_ENABLED = True
    DATABASE_URI = "sqlite:///db.sqlite"
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False
    WTF_CSRF_ENABLED = False


class ProductionConfig(object):
    BCRYPT_LOG_ROUNDS = 32
    CSRF_ENABLED = True
    DATABASE_URI = "sqlite:///db.sqlite"
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    TESTING = False
    WTF_CSRF_ENABLED = True


def dateformat(time: datetime, format: str):
    return time.strftime(format)


def fullname(username: str):
    try:
        user = database.session.query(User).filter_by(username=username).one()
    except NoResultFound:
        return "None"
    return f"{user.first_name} {user.last_name}"


def create_app() -> Flask:
    app = Flask(__name__, instance_relative_config=True)

    cfg = AppConfig()
    app.config.from_object(cfg)
    app.config.from_pyfile("application.cfg", silent=True)

    login_manager.init_app(app)
    bcrypt.init_app(app)
    database.init_app(app)
    migrate.init_app(app, db=database)
    scheduler.init_app(app)

    with app.app_context():
        database.create_all()

    app.register_blueprint(ui_bp, url_prefix="/")

    app.jinja_env.filters["dateformat"] = dateformat
    app.jinja_env.filters["fullname"] = fullname

    return app
