#!/usr/bin/env python3

from flask import (
    Flask,
    request,
    Response,
)

app = Flask(__name__)

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
