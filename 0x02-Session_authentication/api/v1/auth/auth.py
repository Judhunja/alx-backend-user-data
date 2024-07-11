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
        if excluded_paths is None:
            return True
        elif len(excluded_paths) == 0:
            return True
        rstrip_path = path.rstrip("/")
        rstrip_paths = [p.rstrip("/") for p in excluded_paths]

        if rstrip_path in rstrip_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request is None:
            return None
        headers = request.headers
        if "Authorization" not in headers.keys():
            return None
        return headers["Authorization"]

    def current_user(self, request=None) -> TypeVar("User"):
        """Current user"""
        return None
