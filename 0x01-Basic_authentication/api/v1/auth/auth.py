#!/usr/bin/env python3
"""This module contains a class Auth"""


from flask import request
from typing import List, Optional, TypeVar


class Auth:
    # def __init__(self):
    #   """Initializes class Auth"""
    #  pass
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth"""
        return False

    def authorization_header(self, request=None) -> Optional[str]:
        """Authorization header"""
        return None

    def current_user(self, request=None) -> Optional[TypeVar('User')]:
        """Current user"""
        return None
