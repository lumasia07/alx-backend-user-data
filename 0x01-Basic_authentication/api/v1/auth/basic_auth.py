#!/usr/bin/env python3
"""Module Basic Auth that inherits from Auth"""
import base64
from api.v1.auth.auth import Auth
from typing import TypeVar
from models.user import User


User_1 = TypeVar('User')
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
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """Decodes base64 Auth header"""
        if base64_authorization_header is None:
            return None
        
        if not isinstance(base64_authorization_header, str):
            return None
        
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        
        except (base64.binascii.Error, UnicodeDecodeError):
            return None
        

    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """Extract user credentials"""
        if decoded_base64_authorization_header is None:
            return(None, None)
        
        if not isinstance(decoded_base64_authorization_header, str):
            return(None, None)
        
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        
        email, pwd = decoded_base64_authorization_header.split(':', 1)
        return email, pwd


    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> User:
        """Returns user based on email and password."""
        if not isinstance(user_email, str) or user_email is None:
            return None

        if not isinstance(user_pwd, str) or user_pwd is None:
            return None

        user = User.search({'email': user_email})

        if not user:
            return None

        user = user[0]
    
        if not user.is_valid_password(user_pwd):
            return None
    
        return user


    def current_user(self, request=None) -> User_1:
        """Retrieves the User instance for a request."""
        if request is None:
            return None
        
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return None

        base64_auth_header = self.extract_base64_authorization_header(auth_header)
        if base64_auth_header is None:
            return None

        decoded_auth = self.decode_base64_authorization_header(base64_auth_header)
        if decoded_auth is None:
            return None

        user_email, user_pwd = self.extract_user_credentials(decoded_auth)
        if user_email is None or user_pwd is None:
            return None

        user = self.user_object_from_credentials(user_email, user_pwd)
        return user

