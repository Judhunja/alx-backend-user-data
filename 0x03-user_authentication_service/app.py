#!/usr/bin/env python3
""" This module contains a Flask app """

from auth import Auth
import flask
from flask import Flask, request, jsonify
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
