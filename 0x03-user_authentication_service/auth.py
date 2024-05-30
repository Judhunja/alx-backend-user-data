#!/usr/bin/env python3
"""This module contains a method _hash_password"""


import bcrypt
from db import DB, User, NoResultFound
import uuid


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
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if user password is correct"""
        try:
            user = self._db.find_user_by(email=email)
            if user is None:
                return False
            return bcrypt.checkpw(password.encode(),
                                  user.hashed_password.encode())
        except Exception:
            return False

    def _generate_uuid(self) -> str:
        """Returns string representation of a new UUID"""
        return str(uuid.uuid4())
