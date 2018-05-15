#!/usr/bin/env python3

from flask import (
    Flask,
    request,
)

app = Flask(__init__)

@app.route('/register', methods=['POST', ])
def register():
    body = request.get_json()
