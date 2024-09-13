#!/usr/bin/env python3
"""Password hashing and authentication management"""

from typing import Optional
import bcrypt
import uuid
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hash a password with bcrypt and return the hashed bytes.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted and hashed password.
    """
    password_bytes = password.encode('utf-8')

    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed_password


class Auth():
    """Auth class to interact with the authentication database."""

    def __init__(self):
        """Initialize the Auth class with a database instance."""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the given email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            User: The created User object.

        Raises:
            ValueError: If a user with the given email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed = self._hash_password(password)
            new_user = self._db.add_user(email=email, hashed_password=hashed)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login by checking the email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login is valid, otherwise False.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password)
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """Generates a new UUID and returns its string representation.

        Returns:
            str: The string representation of the UUID.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Creates a new session for the user with the given email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID.

        Raises:
            NoResultFound: If no user is found with the provided email.
        """
        try:
            user: User = self._db.find_user_by(email=email)
        except NoResultFound:
            raise NoResultFound("No user found with provided credentials")

        session_id: str = self._generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self,
                                 session_id: Optional[str]) -> Optional[User]:
        """Retrieves the User object corresponding to the session ID.

        Args:
            session_id (Optional[str]): The session ID.

        Returns:
            Optional[User]: The User object if found, otherwise None.
        """
        if session_id is None:
            return None

        try:
            return self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys the session for the user with the given user ID.

        Args:
            user_id (int): The ID of the user.

        Returns:
            None
        """
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generates and returns a reset password token for the user.

        Args:
            email (str): The email of the user.

        Returns:
            str: The reset token.

        Raises:
            ValueError: If no user is found with the given email.
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError(f"No user found with email: {email}")

        reset_token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Updates the user's password using the reset token.

        Args:
            reset_token (str): The reset token.
            password (str): The new password.

        Returns:
            None

        Raises:
            ValueError: If the reset token is invalid.
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        hashed_password = self._hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
