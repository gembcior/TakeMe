from datetime import datetime

from flask_login import UserMixin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from hcit.crypto import bcrypt

database = SQLAlchemy()
migrate = Migrate()


class User(UserMixin, database.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[bytes] = mapped_column(String, nullable=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    created: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    def __init__(self, username, first_name, last_name, password, is_admin=False):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = bcrypt.generate_password_hash(password)
        self.is_admin = is_admin
        self.created = datetime.now()


class Resource(database.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    taken: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    taken_by: Mapped[str | None] = mapped_column(String, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    resource_type: Mapped[str] = mapped_column(String, nullable=False)
    taken_on: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    notes: Mapped[str] = mapped_column(Text, nullable=True)

    def __init__(self, name, resource_type, notes):
        self.name = name
        self.resource_type = resource_type
        self.notes = notes
