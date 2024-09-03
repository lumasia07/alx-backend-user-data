#!/usr/bin/env python3
"""Module Basic Auth that inherits from Auth"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """inherits from Base Class Auth"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extracts base64 Auth header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        
        return authorization_header[len("Basic "):]