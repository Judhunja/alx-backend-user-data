#!/usr/bin/env python3
"""This module contains a method _hash_password"""


import bcrypt


def _hash_password(password: str) -> bytes:
    """Returns a salted hash of the input password"""
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password.encode(), salt)
