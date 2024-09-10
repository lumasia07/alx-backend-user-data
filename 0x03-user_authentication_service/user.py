#!/usr/bin/env python3
"""Creates a user model"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """Defines User model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(250), nullable=False, unique=True)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=False)

    def __init__(self, email: str, hashed_password: str,
                 session_id: str = None, reset_token: str = None):
        """Instanitiates field values"""
        self.email = email
        self.hashed_password = hashed_password
        self.session_id = session_id
        self.reset_token = reset_token

    def __repr__(self):
        """String rep for User model"""
        return f"<User(id={self.id}, email={self.email})>"
