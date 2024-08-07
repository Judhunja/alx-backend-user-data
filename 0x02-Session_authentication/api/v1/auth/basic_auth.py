#!/usr/bin/env python3
"""This module contains a class BasicAuth"""


from .auth import Auth
import base64
from models.base import Base
from models.user import User
from typing import TypeVar


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

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str
    ) -> TypeVar('User'):
        """Creating a user object from user email and password"""
        if (
            user_email is None
            or not isinstance(user_email, str)
            or user_pwd is None
            or not isinstance(user_pwd, str)
        ):
            return None

        try:
            usr_list = User.search({"email": user_email})
        except KeyError:
            return None
        if not usr_list:
            return None
        # get the first User object from List of objects returned by search
        usr = usr_list[0]
        if not usr.is_valid_password(user_pwd):
            return None
        return usr

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth.current_user and retrieves the User instance
        for a request"""
        header = self.authorization_header(request)
        base64cred = self.extract_base64_authorization_header(header)
        decodedbase64cred = self.decode_base64_authorization_header(base64cred)
        email, pwd = self.extract_user_credentials(decodedbase64cred)
        usr = self.user_object_from_credentials(email, pwd)
        return usr
