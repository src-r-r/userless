#!/usr/bin/env python3

from sqlalchemy.ext.declarative import (
    declarative_base,
    declared_attr,
    )

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
)

from sqlalchemy_utils import (
    EmailType,
    PasswordType,
    # ChoiceType,
)

Base = declarative_base()


class NamedTableMixin(object):

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class ModelBase(Base, NamedTableMixin):

    id = Column(Integer, primary_key=True)


class User(ModelBase):

    email = Column(EmailType, unique=True, nullable=False)
    password = Column(PasswordType, nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    token = Column(String)


class Group(ModelBase):

    name = Column(String, nullable=False, unique=True)
