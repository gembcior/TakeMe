from flask import Blueprint, flash, redirect, render_template
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import PasswordInput, TextInput

from hcit.crypto import bcrypt
from hcit.database import User, database

bp = Blueprint("pages", __name__)


class MyTextInput(TextInput):
    def __init__(self, error_class="is-invalid"):
        super(MyTextInput, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop("class", "") or kwargs.pop("class_", "")
            kwargs["class"] = "%s %s" % (self.error_class, c)
        return super(MyTextInput, self).__call__(field, **kwargs)


class MyPasswordInput(PasswordInput):
    def __init__(self, error_class="is-invalid"):
        super(MyPasswordInput, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop("class", "") or kwargs.pop("class_", "")
            kwargs["class"] = "%s %s" % (self.error_class, c)
        return super(MyPasswordInput, self).__call__(field, **kwargs)


class UniqueUserValidator:
    def __init__(self, message=None):
        if message is None:
            message = "User already exists"
        self.message = message

    def __call__(self, form, field):
        user = User.query.filter_by(username=field.data).first()
        if user:
            raise ValidationError(self.message)


class RegisterUserForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=3, max=25)], widget=MyTextInput())
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=3, max=25)], widget=MyTextInput())
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25), UniqueUserValidator()], widget=MyTextInput())
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=25)], widget=MyPasswordInput())
    confirm = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password", message="Passwords must match")], widget=MyPasswordInput())
    submit = SubmitField("Sign up")


class LoginUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], widget=MyTextInput())
    password = PasswordField("Password", validators=[DataRequired()], widget=MyPasswordInput())
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")


class AddResourceForm(FlaskForm):
    name = StringField("Resource Name", validators=[DataRequired()])


@bp.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("You are already logged in.", "info")
        return redirect("/")
    form = LoginUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        else:
            flash("Invalid username and/or password.", "danger")
    return render_template("login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect("/")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        flash("You are already registered.", "info")
        return redirect("/")
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = User(  # noqa
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
        )
        database.session.add(user)
        database.session.commit()
        flash("Register success. You can now sign in!", "success")
        return redirect("login")
    return render_template("register.html", form=form)


@bp.route("/add", methods=["GET", "POST"])
def add():
    form = AddResourceForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template("add.html", form=form)
