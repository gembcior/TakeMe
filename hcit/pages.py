from flask import Blueprint, redirect, render_template, url_for
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo
from wtforms.widgets import TextInput

from .database import User, db

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


class RegisterUserForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired(), Length(min=3, max=25)], widget=MyTextInput())
    last_name = StringField("Last Name", validators=[DataRequired(), Length(min=3, max=25)], widget=MyTextInput())
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=25)], widget=MyTextInput())
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=25)])
    confirm = PasswordField("Confirm password", validators=[DataRequired(), EqualTo("password", message="Passwords must match.")])
    submit = SubmitField("Sign up")


class LoginUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], widget=MyTextInput())
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")


class AddResourceForm(FlaskForm):
    name = StringField("Resource Name", validators=[DataRequired()])


@bp.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginUserForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template("login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterUserForm()
    if form.validate_on_submit():
        user = User( # noqa
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect("register")
    return render_template("register.html", form=form)


@bp.route("/add", methods=["GET", "POST"])
def add():
    form = AddResourceForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template("add.html", form=form)
