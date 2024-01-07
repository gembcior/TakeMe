from flask_jwt_extended import JWTManager
from flask_login import LoginManager

from takeme.database import User

login_manager = LoginManager()

login_manager.login_view = "ui.auth.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()


jwt = JWTManager()
