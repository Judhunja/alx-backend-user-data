#!/usr/bin/env python3
"""This module contains a basic flask app"""

import flask
from flask import Flask, request, session, make_response, redirect, url_for
from auth import Auth, NoResultFound
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


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """Logout a user"""
    session_id = request.cookies.get('session_id')
    if session_id:
        try:
            user = AUTH.get_user_from_session_id(session_id)
            AUTH.destroy_session(user.id)
            return redirect(url_for('get'))
        except NoResultFound:
            flask.abort(403)
    else:
        flask.abort(403)


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    """Get user email in a json payload"""
    session_id = request.cookies.get('session_id')
    if session_id:
        try:
            user = AUTH.get_user_from_session_id(session_id)
            if user:
                return make_response(flask.jsonify({"email": user.email}), 200)
            flask.abort(403)
        except NoResultFound:
            flask.abort(403)
    else:
        flask.abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
