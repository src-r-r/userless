#!/usr/bin/env python3

from sqlalchemy.ext.declarative import (
    # declarative_base,
    declared_attr,
    )

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)

from sqlalchemy.orm import (
    validates,
)

from sqlalchemy_utils import (
    EmailType,
    PasswordType,
    # ChoiceType,
)

from flask import (
    Flask,
)
from flask_sqlalchemy import (
    SqlAlchemy,
)

from validators import (
    email as validate_email,
    length as validate_length,
)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)

class NamedTableMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class ModelBase(db.Base, NamedTableMixin):

    id = Column(Integer, primary_key=True)


class User(ModelBase):

    email = Column(EmailType, unique=True, nullable=False)
    password = Column(PasswordType, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    token = Column(String)

    @validates
    def email(self, value):
        validate_email(value)
        return value


class Group(ModelBase):

    name = Column(String, nullable=False, unique=True)
