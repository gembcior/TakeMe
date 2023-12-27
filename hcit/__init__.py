from flask import Flask

from hcit import pages

from .database import User, db


class Config(object):
    TESTING = False
    SECRET_KEY = "192b9bdd22ab9ed4d12e236c78afcb9a393ec15f71bbf5dc987d54727823bcbf"


class ProductionConfig(Config):
    DATABASE_URI = "sqlite:///db.sqlite"


class DevelopmentConfig(Config):
    DATABASE_URI = "sqlite:///db.sqlite"
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite"


class TestingConfig(Config):
    DATABASE_URI = "sqlite:///db.sqlite"
    TESTING = True


def create_app():
    app = Flask(__name__)

    cfg = DevelopmentConfig()
    app.config.from_object(cfg)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(pages.bp)
    return app
