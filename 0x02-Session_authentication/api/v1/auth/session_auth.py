#!/usr/bin/env python3
"""Module for Session auth"""
import os
import uuid
from flask import abort, jsonify, request
from api.v1.auth.auth import Auth
from models.user import User
from api.v1.views import app_views


class SessionAuth(Auth):
    """Defines session auth"""
    def __init__(self):
        """Initialize user by session id"""
        self.user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Create user session"""
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())

        self.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return value of userID(key)"""
        if session_id is None or not isinstance(session_id, str):
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Return user based on session cookie"""
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        if user_id:
            return User.get(user_id)
        return None

@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """Handles the login route for session authentication."""
    
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    users = User.search({'email': email})

    if not users or len(users) == 0:
        return jsonify({"error": "no user found for this email"}), 404

    user = users[0]
    
    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 40
    from api.v1.app import auth
    
    session_id = auth.create_session(user.id)

    if not session_id:
        return abort(500, description="Session creation failed")

    session_name = os.getenv('SESSION_NAME')

    user_data = user.to_json()
    response = jsonify(user_data)

    response.set_cookie(session_name, session_id)

    return response