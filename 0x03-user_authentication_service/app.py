#!/usr/bin/env python3
""" This module contains a Flask app """

from sqlalchemy.orm.exc import NoResultFound
from auth import Auth
import flask
from flask import Flask, request, jsonify, make_response, redirect, url_for
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def get():
    """Return json payload"""
    return flask.jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def users():
    """ Endpoint to register a user """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({"email": email, "message": "user created"})


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ Login a user """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        flask.abort(401)
    user = AUTH._db.find_user_by(email=email)
    sess_id = AUTH.create_session(email)
    user.session_id = sess_id
    resp = make_response(jsonify({"email": email, "message": "logged in"}))
    resp.set_cookie("session_id", sess_id)
    return resp


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ Logout a user """
    cookies = request.cookies
    session_id = cookies["session_id"]
    try:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect(url_for('get'))
    except Exception:
        return redirect(url_for('get'))


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile():
    """ Find user profile """
    cookies = request.cookies
    session_id = cookies["session_id"]
    try:
        user = AUTH.get_user_from_session_id(session_id)
    except Exception:
        flask.abort(403)
    if user:
        return jsonify({"email": user.email}), 200
    else:
        flask.abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """ Reset password endpoint """
    email = request.form.get("email")
    try:
        AUTH._db.find_user_by(email=email)
    except NoResultFound:
        flask.abort(403)
    token = AUTH.get_reset_password_token(email)
    return jsonify({"email": email, "reset_token": token})


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """ Update password endpoint """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    try:
        AUTH.update_password(reset_token, new_password)
    except ValueError:
        flask.abort(403)

    return jsonify({"email": email, "message": "Password updated"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
