#!/usr/bin/env python3
"""Module for Session auth"""
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Defines session auth"""
    def __init__(self):
        """Initialize user by session id"""
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create user session"""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return value of userID(key)"""
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)
