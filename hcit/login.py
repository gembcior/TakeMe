from flask_login import LoginManager

from hcit.database import User

login_manager = LoginManager()

login_manager.login_view = "pages.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
