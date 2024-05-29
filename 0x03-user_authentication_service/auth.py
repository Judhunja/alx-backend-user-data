#!/usr/bin/env python3
"""This module contains a method _hash_password"""


import bcrypt
from db import DB
from db import User
from sqlalchemy.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """Returns a salted hash of the input password"""
        salt = bcrypt.gensalt()

        return bcrypt.hashpw(password.encode(), salt)

    def register_user(self, email: str, password: str) -> User:
        """Authenticates a user"""
        try:
            user_exists = self._db.find_user_by(email=email)
            if user_exists:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            password = self._hash_password(password).decode()
            user = self._db.add_user(email, password)
            return user
