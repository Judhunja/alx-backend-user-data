#!/usr/bin/env python3
"""Hashing password using bcrypt"""


import bcrypt


def hash_password(password: str) -> bytes:
    """Returns salted hashed password which is
        a byte string"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)
