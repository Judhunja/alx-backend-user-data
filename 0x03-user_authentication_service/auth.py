#!/usr/bin/env python3
""" This module contains a method _hash_password"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """hash password"""
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(password.encode(), salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Registers a new user"""
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f'User {email} already exists')
        except NoResultFound:
            hashed_pw = _hash_password(password)
            user = self._db.add_user(email, hashed_pw)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ Check if password matches in login """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
            else:
                return False
        except NoResultFound:
            return False
