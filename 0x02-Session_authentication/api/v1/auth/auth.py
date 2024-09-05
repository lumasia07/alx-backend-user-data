#!/usr/bin/env python3
"""Module for authorization"""
from flask import request
from typing import List, TypeVar
import os


User = TypeVar('User')


class Auth:
    """Defines a class Auth"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Defines routes that dont need authentication"""
        if path is None:
            return True
        if not excluded_paths:
            return True
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*'):
                if path.startswith(excluded_path[:-1]):
                    return False

            elif path == excluded_path:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns value of header request"""
        if request is None:
            return None

        auth_header = request.headers.get('Authorization')
        if auth_header is None:
            return None

        return auth_header

    def current_user(self, request=None) -> User:
        """Returns None"""
        return None

    def session_cookie(self, request=None):
        """Return value of cookie"""
        if request is None:
            return None

        session_name = os.getenv('SESSION_NAME')

        if session_name is None:
            return None

        return request.cookies.get(session_name)
