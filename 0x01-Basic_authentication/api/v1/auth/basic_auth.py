#!/usr/bin/env python3
"""This module contains a class BasicAuth"""


from .auth import Auth
import base64


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

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """Decoding the base64 part of the authorization header"""
        if (
            base64_authorization_header is None
            or not isinstance(base64_authorization_header, str)
        ):
            return None

        try:
            return base64.b64decode(
                base64_authorization_header).decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        """Return user email and password from the Base64 decoded value"""
        if (
            decoded_base64_authorization_header is None
            or not isinstance(decoded_base64_authorization_header, str)
            or ":" not in decoded_base64_authorization_header
        ):
            return (None, None)
        email, pwd = decoded_base64_authorization_header.split(":")
        return (email, pwd)

    """def user_object_from_credentials(
            self,
            user_email: str, user_pwd: str
        ) -> TypeVar('User'):"""
