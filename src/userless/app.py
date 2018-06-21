#!/usr/bin/env python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager


from userless.exc import (
    UserlessException,
)

from userless.extension import (
    celery,
    db
)


class UserlessApp(Flask):

    def __init__(self, *args, **kwargs):
        super(UserlessApp, self).__init__(*args, **kwargs)
        self.api_manager = None
        self.db = None


def create_app(config_filename):
    # import flask.ext.restless

    app = UserlessApp(__name__)
    app.config.from_pyfile(config_filename)

    from userless.models import (
        db, User, Group,
    )

    from userless.bootstrap import check

    if not check():
        raise OSError('✘ Pre-Flight Check Failed; Check console for output.')

    db.init_app(app)
    celery.init_app(app)

    manager = APIManager(app, flask_sqlalchemy_db=db)

    with app.app_context():
        db.create_all()
        manager.create_api(User, methods=['GET', 'PUT', 'POST', 'DELETE'])
        manager.create_api(Group, methods=['GET', 'PUT', 'POST', 'DELETE'])

    app.db = db
    app.api_manager = manager

    return app

# Copied from "Flask Celery pattern" (https://lstu.fr/dqLZcUur)
