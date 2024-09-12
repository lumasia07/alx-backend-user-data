#!/usr/bin/env python3
"""Password hashing"""
import bcrypt

"""Defines a class DB"""
def _hash_password(password: str) -> bytes:
    """Function to hash password"""

    salt = bcrypt.gensalt()

    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
