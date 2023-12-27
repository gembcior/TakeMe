from flask import Blueprint, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import TextInput

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
    first_name = StringField("First Name", validators=[DataRequired()], widget=MyTextInput())
    last_name = StringField("Last Name", validators=[DataRequired()], widget=MyTextInput())
    username = StringField("Username", validators=[DataRequired()], widget=MyTextInput())
    password = PasswordField("Password", validators=[DataRequired()])


class LoginUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()], widget=MyTextInput())
    password = PasswordField("Password", validators=[DataRequired()])


class AddResourceForm(FlaskForm):
    name = StringField("Resource Name", validators=[DataRequired()])


@bp.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginUserForm()
    form.validate_on_submit()
    return render_template("login.html", form=form)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterUserForm()
    form.validate_on_submit()
    return render_template("register.html", form=form)


@bp.route("/add", methods=["GET", "POST"])
def add():
    form = AddResourceForm()
    form.validate_on_submit()
    return render_template("add.html", form=form)
