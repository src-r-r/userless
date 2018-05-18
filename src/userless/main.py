#!/usr/bin/env python3

from queue import (
    Queue
)

from flask import (
    Flask,
    request,
    Response,
)

from flask.ext.restless import (
    APIManager,
)
from flask.ext.sqlalchemy import (
    SQLAlchemy,
)

from userless.models import (
    app,
    db,
)

@app.route('/')
def index():
    """ Test path
    """
    return Response('hello, world!')


@app.route('/register', methods=['POST', ])
def register():
    """ Register a new user.

    ...

    request:
        - method: POST
          body:
            format: json
            contents:
                email: email address associated with account.
                password: password for account
    response:
        success:
            - response_code: 202
              reason: user has been created.

    """
    body = request.get_json()
    email = body['email']
    password = body['password']
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()


@app.route('/verify', method=['POST', ])


@app.route('/login/', method=['POST', ])
def login():
    email = request.data['email']
    password = request.data['password']
