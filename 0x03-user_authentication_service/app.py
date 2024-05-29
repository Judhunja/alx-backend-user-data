#!/usr/bin/env python3
"""This module contains a basic flask app"""

import flask
from flask import Flask


app = Flask(__name__)


@app.route("/")
def get():
    return flask.jsonify({"message": "Bienvenue"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
