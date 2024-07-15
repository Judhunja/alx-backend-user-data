#!/usr/bin/env python3
""" This module contains a method _hash_password"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """hash password"""
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password.encode(), salt)
