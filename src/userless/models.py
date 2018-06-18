#!/usr/bin/env python3

import copy
import os
import jinja2

from sqlalchemy.ext.declarative import (
    declarative_base,
    declared_attr,
)

from sqlalchemy import (
    Table,
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
)

from sqlalchemy.orm import (
    validates,
    relationship,
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
    SQLAlchemy,
    Model,
)

from validators import (
    email as validate_email,
    length as validate_length,
)

import requests


Base = declarative_base()


class NamedTableMixin(Model):
    """ Creates a table name automatically. """

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()


class ModelBase(NamedTableMixin):
    """ Named model that contains a primary key ID column. """

    id = Column(Integer, primary_key=True)


db = SQLAlchemy(model_class=ModelBase)

user_group_assoc = Table('user_group_assoc', db.Model.metadata,
                         Column('user_id', Integer, ForeignKey('user.id')),
                         Column('group_id', Integer, ForeignKey('group.id'))
                         )


class User(db.Model):

    email = Column(EmailType, unique=True, nullable=False)
    password = Column(PasswordType(
        schemes=[
            'pbkdf2_sha512',
        ],
    ), nullable=False)
    is_verified = Column(Boolean, nullable=False, default=False)
    state = Column(String)
    token = Column(String)

    groups = relationship('Group', secondary=user_group_assoc,
                          back_populates='users')

    @validates
    def validate_email(self, value):
        """ Validate a user's email address.

        :param value: Value of the user's email address.

        :return: `value` on success.

        :raises: ValueError if value is incorrect.
        """
        validate_email(value)
        return value

    def generic_send_email(self, escargo, escargo_server=('127.0.0.1', 5000)):
        """ Generically send an email to the user.

        :param escargo: `escargo` server data. The `sending.to` field should
        be omitted as this will be overridden by the user's email address.

        :param escarog_server: `(hostname, port)` of the server runing escargo.

        :return: response of sending the email.
        """
        escargo['sending']['to'] = self.email
        url = 'http://{}:{}/'.format(*escargo_server)
        return requests.post(url, json=escargo)

    def send_verification_email(self, escargo,
                                verification_url,
                                subject=None,
                                escargo_server=('127.0.0.1', 5000)):
        """ Send a verification email to the user.

        :param escargo: Escargo configuration

        :param verification_url: URL to use for verification.
        IMPORTANT: must contain the {token} placeholder.

        :param subject: Subject to specify.
        Default will be 'Verify Your Account'

        :param escargo_server: `(hostname, port)` of the running escargo
        server. Default will be (127.0.0.1, 5000)
        """
        from .paths import (HTML_EMAIL_USER_VERIFY, TEXT_EMAIL_USER_VERIFY)
        from .util import read_from
        from jinja2 import Template
        verify_text = read_from(TEXT_EMAIL_USER_VERIFY)
        verify_html = read_from(HTML_EMAIL_USER_VERIFY)
        # TODO: Add more available variables for the jinja2 template.
        escargo['sending'] = {
            'from': escargo['sending']['from'],
            'to': self.email,
            'subject': subject or 'Verify Your Account',
            'message': {
                'text_body': Template(verify_text).render(email=self.email),
                'html_body': Template(verify_html).render(email=self.email),
            }
        }
        return self.generic_send_email(escargo, escargo_server)

    def send_password_reset_email(self, escargo,
                                  reset_url,
                                  subject=None,
                                  escargo_server=('127.0.0.1', 5000)):
        """ Send a verification email to the user.

        :param escargo: Escargo configuration

        :param reset_url: URL to use for verification.
        IMPORTANT: must contain the {token} placeholder.

        :param subject: Subject to specify.
        Default will be 'Reset Your Password'

        :param escargo_server: `(hostname, port)` of the running escargo
        server. Default will be (127.0.0.1, 5000)
        """
        from .paths import (
            HTML_EMAIL_PASSWORD_RESET,
            TEXT_EMAIL_PASSWORD_RESET,
        )
        from .util import read_from
        from jinja2 import Template
        text = read_from(TEXT_EMAIL_PASSWORD_RESET)
        html = read_from(HTML_EMAIL_PASSWORD_RESET)
        # TODO: Add more available variables for the jinja2 template.
        escargo['sending'] = {
            'from': escargo['sending']['from'],
            'to': self.email,
            'subject': subject or 'Reset Your Password',
            'message': {
                'text_body': Template(text).render(
                    email=self.email,
                    url=reset_url
                ),
                'html_body': Template(html).render(
                    url=reset_url,
                    email=self.email
                ),
            }
        }
        return self.generic_send_email(escargo, escargo_server)


class Group(db.Model):

    name = Column(String, nullable=False, unique=True)

    users = relationship('User', secondary=user_group_assoc,
                         back_populates='groups')
