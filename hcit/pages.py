import json

from flask import Blueprint, Response
from flask import current_app as app
from flask import redirect, render_template, request
from flask_login import current_user, login_required, login_user, logout_user
from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
    ValidationError,
)
from wtforms.validators import DataRequired, EqualTo, Length
from wtforms.widgets import PasswordInput, TextInput

from hcit.crypto import bcrypt
from hcit.database import Resource, User, database

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
    name = StringField("Resource name", validators=[DataRequired()])
    notes = TextAreaField("Notes")
    resource_type = SelectField("Resource type", choices=[("fpga", "FPGA"), ("asic", "ASIC"), ("other", "Other")], default="other")
    submit = SubmitField("Add resource")


@bp.route("/")
def home():
    resources = Resource.query.all()
    return render_template("home.html", resources=resources)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect("/")
    form = LoginUserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            app.logger.info(f"User {user.username} logged in")
            return redirect("/")
        else:
            app.logger.warning("Invalid username and/or password")
    return render_template("login.html", form=form)


@bp.route("/resource", methods=["GET", "POST"])
@login_required
def resource():
    app.logger.warning("Resource POST")
    # data: dict = json.loads(request.data)
    data = request.json
    cmd = data.get("cmd")
    if cmd == "take":
        resource = Resource.query.filter_by(name=data["name"]).first()
        resource.taken = True
        database.session.commit()
    elif cmd == "release":
        resource = Resource.query.filter_by(name=data["name"]).first()
        resource.taken = False
        database.session.commit()
    return Response(status=204)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    app.logger.info("User logged out")
    return redirect("/")


@bp.route("/register", methods=["GET", "POST"])
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


@bp.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = AddResourceForm()
    if form.validate_on_submit():
        resource = Resource(
            name=form.name.data,
            resource_type=form.resource_type.data,
            notes=form.notes.data,
        )
        database.session.add(resource)
        database.session.commit()
        return redirect("/")
    return render_template("add.html", form=form)
