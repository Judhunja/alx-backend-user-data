#!/usr/bin/env python3
""" This module contains a Flask app """

from auth import Auth
import flask
from flask import Flask, request, jsonify, make_response, redirect, url_for
app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def get():
    """Return json payload"""
    return flask.jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """ Endpoint to register a user """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """ Login a user """
    email = request.form.get("email")
    password = request.form.get("password")
    if not AUTH.valid_login(email, password):
        flask.abort(401)
    sess_id = AUTH.create_session(email)
    resp = make_response(jsonify({"email": email, "message": "logged in"}))
    resp.set_cookie("session_id", sess_id)
    return resp


@app.route('/sessions', methods=['DELETE'])
def logout():
    """ Logout a user """
    cookies = request.cookies
    session_id = cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        flask.abort(403)
    else:
        AUTH.destroy_session(user.id)
        return redirect(url_for('get'))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
