from database.db import get_connection
from auth.password_utils import verify_password


def authenticate_user(username, password):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, username, password_hash, role, must_change_password, is_active
        FROM users WHERE username=?
    """, (username,))

    user = cursor.fetchone()
    conn.close()

    if not user:
        return None

    user_id, username, password_hash, role, must_change, active = user

    if active == 0:
        return "inactive"

    if verify_password(password, password_hash):
        return {
            "user_id": user_id,
            "username": username,
            "role": role,
            "must_change_password": must_change
        }

    return None