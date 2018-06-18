#!/usr/bin/env python3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager

class UserlessApp(Flask):

    def __init__(self, *args, **kwargs):
        super(UserlessApp, self).__init__(*args, **kwargs)
        self.api_manager = None

    def _start_queues(self):
        for q in QUEUES.items():
            q.run()

    def _stop_queues(self):
        for q in QUEUES.items():
            q.join()
            q.stop()

    def request_account_verification(self, user):
        return QUEUES['password_reset'].add_user(user)

    def request_password_reset(self, user):
        return QUEUES['account_verification'].add_user(user)


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
    manager = APIManager(app, flask_sqlalchemy_db=db)

    with app.app_context():
        db.create_all()
        manager.create_api(User, methods=['GET', 'PUT', 'POST', 'DELETE'])
        manager.create_api(Group, methods=['GET', 'PUT', 'POST', 'DELETE'])

    return app
