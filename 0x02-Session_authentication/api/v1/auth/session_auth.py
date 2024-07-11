#!/usr/bin/env python3
"""This module contains a class SessionAuth"""

from ..auth.auth import Auth
from uuid import uuid4
from ..views.users import User


class SessionAuth(Auth):
    """Session authentication mechanism"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user_id"""
        if (
            user_id is None
            or not isinstance(user_id, str)
        ):
            return None

        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return user ID based on a session ID"""
        if (
            session_id is None
            or not isinstance(session_id, str)
        ):
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """Returns a user instance based on cookie value"""
        cookie = self.session_cookie(request)
        userid = self.user_id_for_session_id(cookie)
        user = User.get(userid)
        return user
