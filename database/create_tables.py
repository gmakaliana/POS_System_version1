from database.db import get_connection
from auth.password_utils import hash_password
from datetime import datetime


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password_hash TEXT,
        role TEXT,
        must_change_password INTEGER DEFAULT 1,
        is_active INTEGER DEFAULT 1,
        created_at TEXT
    )
    """)

    conn.commit()

    # Create default admin
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("""
        INSERT INTO users (username, password_hash, role, must_change_password, created_at)
        VALUES (?, ?, ?, ?, ?)
        """, (
            "admin",
            hash_password("admin123"),
            "Admin",
            1,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        conn.commit()

    conn.close()