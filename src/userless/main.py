#!/usr/bin/env python3

from flask import (
    Flask,
    request,
    Response,
)

# from flask_restful import (
#     Resource,
#     Api,
# )
from flask.ext.restless import (
    APIManager,
)
from flask.ext.sqlalchemy import (
    SQLAlchemy,
)

from validators import (
    email as validate_email,
)

app = Flask(__name__)

# restLESS API
db = SQLAlchemy(app)

# restFUL api
# api = Api(app)


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
    validate_email.email(email)
    db.session
