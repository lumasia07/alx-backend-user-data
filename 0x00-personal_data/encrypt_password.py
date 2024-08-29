#!/usr/bin/env python3
"""Encrypt a paswword"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Return hashed password"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
