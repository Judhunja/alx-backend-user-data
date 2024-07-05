#!/usr/bin/env python3
"""Hashing password using bcrypt"""


import bcrypt


def hash_password(password: str) -> bytes:
    """Returns salted hashed password which is
        a byte string"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks whether a password is valid"""
    # check the password to be tested against the hashed
    return bcrypt.checkpw(password.encode(), hashed_password)
