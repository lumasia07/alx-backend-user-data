import requests

BASE_URL = "http://localhost:5000"

def register_user(email: str, password: str) -> None:
    """ Register a new user. """
    payload = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.json() == {"email": email, "message": "user created"}, f"Unexpected response payload: {response.json()}"

def log_in_wrong_password(email: str, password: str) -> None:
    """ Try to log in with an incorrect password. """
    payload = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", json=payload)
    assert response.status_code == 401, f"Expected status code 401, got {response.status_code}"

def log_in(email: str, password: str) -> str:
    """ Log in and return the session ID. """
    payload = {"email": email, "password": password}
    response = requests.post(f"{BASE_URL}/sessions", json=payload)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    session_id = response.cookies.get("session_id")
    assert session_id, "No session ID found"
    return session_id

def profile_unlogged() -> None:
    """ Access profile without being logged in. """
    response = requests.get(f"{BASE_URL}/profile")
    assert response.status_code == 403, f"Expected status code 403, got {response.status_code}"

def profile_logged(session_id: str) -> None:
    """ Access profile while logged in. """
    cookies = {"session_id": session_id}
    response = requests.get(f"{BASE_URL}/profile", cookies=cookies)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

def log_out(session_id: str) -> None:
    """ Log out of the session. """
    cookies = {"session_id": session_id}
    response = requests.delete(f"{BASE_URL}/sessions", cookies=cookies)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

def reset_password_token(email: str) -> str:
    """ Request a password reset token. """
    payload = {"email": email}
    response = requests.post(f"{BASE_URL}/reset_password", json=payload)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    reset_token = response.json().get("reset_token")
    assert reset_token, "No reset token found"
    return reset_token

def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Update password using reset token. """
    payload = {"email": email, "reset_token": reset_token, "new_password": new_password}
    response = requests.put(f"{BASE_URL}/reset_password", json=payload)
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    assert response.json() == {"email": email, "message": "Password updated"}, f"Unexpected response payload: {response.json()}"

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
