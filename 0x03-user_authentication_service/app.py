#!/usr/bin/env python3
"""This module contains a basic flask app"""

import flask
from flask import Flask, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def get():
    """Return jsonified payload"""
    return flask.jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'])
def users():
    """Send user data"""
    email = request.form['email']
    password = request.form['password']
    try:
        user = AUTH.register_user(email, password)
        return flask.jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return flask.jsonify({"message": "email already registered"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
