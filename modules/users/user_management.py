from database.db import get_connection
from auth.password_utils import hash_password
from datetime import datetime


def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id, username, role, must_change_password
        FROM users
    """)

    users = cursor.fetchall()
    conn.close()
    return users


def add_user(username, password, role):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO users (username, password_hash, role, must_change_password, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        hash_password(password),
        role,
        1,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


def update_user(user_id, username, role):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET username=?, role=?
        WHERE user_id=?
    """, (username, role, user_id))

    conn.commit()
    conn.close()


def delete_user(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    # ------------------------------------
    # PROTECT DEFAULT ADMIN
    # ------------------------------------
    cursor.execute("SELECT username FROM users WHERE user_id=?", (user_id,))
    user = cursor.fetchone()

    if user and user[0] == "admin":
        conn.close()
        raise Exception("Default admin account cannot be deleted.")

    cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))

    conn.commit()
    conn.close()