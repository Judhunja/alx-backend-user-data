#!/usr/bin/env python3
"""This module contains a class Auth"""


from flask import request


class Auth:
    def __init__(self):
        """Initializes class Auth"""
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """"""
        return False

    def authorization_header(self, request=None) -> str:
        """"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """"""
        return None
