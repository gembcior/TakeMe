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

from hcit.database import User, database


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
        user = database.session.query(User).filter_by(username=field.data).one()
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
