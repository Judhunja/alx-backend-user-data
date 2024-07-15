#!/usr/bin/env python3
""" This module contains a Flask app """

import flask
from flask import Flask
app = Flask(__name__)


@app.route('/', methods=['GET'])
def get():
    """Return json payload"""
    return flask.jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
