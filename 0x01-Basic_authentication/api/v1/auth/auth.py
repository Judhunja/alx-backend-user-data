#!/usr/bin/env python3
"""This module contains a class Auth"""


from flask import request
from typing import List, TypeVar


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Check if path requires authentication"""
        if path is None:
            return True
        if len(excluded_paths) == 0 or excluded_paths is None:
            return True
        path = path.rstrip("/")
        rstrip_paths = [path.rstrip("/") for path in excluded_paths]
        if path in rstrip_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        return None

    def current_user(self, request=None) -> TypeVar("User"):
        """Current user"""
        return None
