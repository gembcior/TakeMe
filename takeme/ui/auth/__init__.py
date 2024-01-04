from flask import Blueprint
from flask import current_app as app
from flask import redirect, render_template
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy.exc import NoResultFound

from takeme.crypto import bcrypt
from takeme.database import User, database
from takeme.form import LoginUserForm, RegisterUserForm

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginUserForm()
    if form.validate_on_submit():
        try:
            user = database.session.query(User).filter_by(username=form.username.data).one()
        except NoResultFound:
            form.username.errors.append("Invalid username")
        else:
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                app.logger.info(f"User {user.username} logged in")
                return redirect("/")
            else:
                app.logger.warning("Invalid username and/or password")
                form.password.errors.append("Invalid password")
    return render_template("login.html", form=form)


@auth_bp.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    app.logger.info("User logged out")
    return redirect("/")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect("/")
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
        )
        database.session.add(user)
        database.session.commit()
        app.logger.info(f"New user {user.username} registered")
        return redirect("login")
    return render_template("register.html", form=form)
