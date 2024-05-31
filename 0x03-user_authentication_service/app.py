#!/usr/bin/env python3
"""This module contains a basic flask app"""

import flask
from flask import Flask, request, session, make_response
from auth import Auth
import uuid


app = Flask(__name__)
AUTH = Auth()
app.secret_key = b'\x996\xdb\xf5\xf0&\xbe[\xcev\xec\xe1\x95\x08KA'


@app.route("/")
def get():
    """Return jsonified payload"""
    return flask.jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """Send user data"""
    email = request.form['email']
    password = request.form['password']
    try:
        user = AUTH.register_user(email, password)
        return flask.jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return flask.jsonify({"message": "email already registered"})


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """Login a user"""
    email = request.form['email']
    password = request.form['password']

    if not AUTH.valid_login(email, password):
        flask.abort(401)

    user = AUTH._db.find_user_by(email=email)
    session_id = str(uuid.uuid4())
    user.session_id = session_id
    session["session_id"] = session_id
    resp = make_response(flask.jsonify(
        {"email": email, "message": "logged in"}))
    resp.set_cookie("session_id", session_id)
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
