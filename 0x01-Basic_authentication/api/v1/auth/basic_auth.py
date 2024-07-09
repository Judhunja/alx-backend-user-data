#!/usr/bin/env python3
"""This module contains a class BasicAuth"""


from .auth import Auth


class BasicAuth(Auth):
    """Implements basic authentication features"""

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the base64 part of the authorization header
        for Basic Authentication"""
        if (
            authorization_header is None
            or not isinstance(authorization_header, str)
            or not authorization_header.startswith("Basic ")
        ):
            return None
        return authorization_header.lstrip("Basic ")
