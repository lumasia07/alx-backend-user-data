#!/usr/bin/env python3
"""Module for authorization"""
from flask import request
from typing import List, TypeVar


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
