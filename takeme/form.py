from flask_wtf import FlaskForm
from sqlalchemy.exc import NoResultFound
from wtforms import (
    BooleanField,
    Field,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
    ValidationError,
)
from wtforms.validators import EqualTo, InputRequired, Length
from wtforms.widgets import PasswordInput, TextInput

from takeme.database import Resource, User, database


class BootstrapTextInput(TextInput):
    def __init__(self, error_class="is-invalid"):
        super(BootstrapTextInput, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop("class", "") or kwargs.pop("class_", "")
            kwargs["class"] = "%s %s" % (self.error_class, c)
        return super(BootstrapTextInput, self).__call__(field, **kwargs)


class BootstrapPasswordInput(PasswordInput):
    def __init__(self, error_class="is-invalid"):
        super(BootstrapPasswordInput, self).__init__()
        self.error_class = error_class

    def __call__(self, field, **kwargs):
        if field.errors:
            c = kwargs.pop("class", "") or kwargs.pop("class_", "")
            kwargs["class"] = "%s %s" % (self.error_class, c)
        return super(BootstrapPasswordInput, self).__call__(field, **kwargs)


class UniqueUserValidator:
    def __init__(self, message=None):
        if message is None:
            message = "User already exists"
        self.message = message

    def __call__(self, form, field):
        try:
            username = field.data.strip()
            user = database.session.query(User).filter_by(username=username).one()
        except NoResultFound:
            return
        if user:
            raise ValidationError(self.message)


class UniqueResourceName:
    def __init__(self, message=None):
        if message is None:
            message = "Resource already exists"
        self.message = message

    def __call__(self, form, field):
        try:
            name = field.data.strip()
            resource = database.session.query(Resource).filter_by(name=name).one()
        except NoResultFound:
            return
        if resource:
            raise ValidationError(self.message)


class ValidString:
    def __call__(self, form, field):
        value: str = field.data
        if not value.isprintable():
            raise ValidationError("Only printable characters")
        if not value.isascii():
            raise ValidationError("Only ASCII characters")


class StrippedNameField(StringField):
    widget = BootstrapTextInput()

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].strip()

    def process_data(self, value):
        if value:
            self.data = value.strip()
        else:
            self.data = ""


class RegisterUserForm(FlaskForm):
    first_name = StrippedNameField("First Name", validators=[InputRequired(), Length(min=3, max=25), ValidString()])
    last_name = StrippedNameField("Last Name", validators=[InputRequired(), Length(min=3, max=25), ValidString()])
    username = StrippedNameField("Username", validators=[InputRequired(), Length(min=3, max=25), UniqueUserValidator(), ValidString()])
    password = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=25), ValidString()], widget=BootstrapPasswordInput())
    confirm = PasswordField(
        "Confirm password", validators=[InputRequired(), EqualTo("password", message="Passwords must match"), ValidString()], widget=BootstrapPasswordInput()
    )
    submit = SubmitField("Sign up")


class LoginUserForm(FlaskForm):
    username = StrippedNameField("Username", validators=[InputRequired(), ValidString()])
    password = PasswordField("Password", validators=[InputRequired(), ValidString()], widget=BootstrapPasswordInput())
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")


class AddResourceForm(FlaskForm):
    name = StrippedNameField("Resource name", validators=[InputRequired(), UniqueResourceName(), ValidString(), Length(min=3, max=25)])
    notes = TextAreaField("Notes")
    resource_type = SelectField("Resource type", choices=[("fpga", "FPGA"), ("asic", "ASIC"), ("other", "Other")], default="other")
    submit = SubmitField("Add resource")


class SettingsForm(FlaskForm):
    auto_release = BooleanField("Auto release")
    auto_release_time = TimeField("Auto release at", validators=[InputRequired()])
    submit = SubmitField("Save")


class ResourceUpdateForm(FlaskForm):
    name = StrippedNameField("Resource name", validators=[InputRequired(), ValidString(), Length(min=3, max=25)])
    notes = TextAreaField("Notes")
    resource_type = SelectField("Resource type", choices=[("fpga", "FPGA"), ("asic", "ASIC"), ("other", "Other")], default="other")
    submit = SubmitField("Update")
