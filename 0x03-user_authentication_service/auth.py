#!/usr/bin/env python3
"""Password hashing"""
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """
    def _hash_password(self, password: str) -> bytes:
        """Function to hash password"""

        salt = bcrypt.gensalt()

        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed

    def __init__(self):
        """Instatiate class auth call from DB"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register user in DB"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed = self._hash_password(password)
            new_user = self._db.add_user(email=email, hashed_password=hashed)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login"""
        try:
            user = self._db.find_user_by(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except Exception:
            return False

    def _generate_uuid(self) -> str:
        """Generates a new ID and returns str representation"""
        return str(uuid.uuid4())
    
    def create_session(self, email: str) -> str:
        """Returns session ID"""
        try:
            user: User = self._db.find_user_by(email=email)
        except NoResultFound:
            raise NoResultFound("No user found with provided credentials")
        
        session_id: str = self._generate_uuid()

        self._db.update_user(user.id, session_id=session_id)

        return session_id
