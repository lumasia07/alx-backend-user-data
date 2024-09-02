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
        if path in excluded_paths:
            return False
        return True

    def authorization_header(self, request=None) -> str:
        """Returns None"""
        return None
    
    def current_user(self, request=None) -> User:
        """Returns None"""
        return None

    