#!/usr/bin/env python3
"""This module contains a method _hash_password"""


import bcrypt
from db import DB, User
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
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password).decode('utf-8')
            user = self._db.add_user(email, hashed_password)
            self._db._session.commit()
            return user
