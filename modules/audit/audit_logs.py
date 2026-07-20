from datetime import datetime

from database.db import get_connection
from auth.session import get_session_user



# ==========================================================
# ADD AUDIT LOG
# ==========================================================

def log_activity(
        module,
        action,
        description
):

    """
    Saves an activity into audit_logs table.

    Example:
    log_activity(
        "Products",
        "EDIT",
        "Edited product Coca-Cola 2L"
    )
    """

    user = get_session_user()


    if user:

        user_id = user["user_id"]
        username = user["username"]
        role = user["role"]

    else:

        # For system events where no user exists

        user_id = None
        username = "SYSTEM"
        role = "SYSTEM"



    log_datetime = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        INSERT INTO audit_logs
        (
            user_id,
            username,
            role,
            module,
            action,
            description,
            log_datetime
        )

        VALUES (?, ?, ?, ?, ?, ?, ?)

        """,

        (
            user_id,
            username,
            role,
            module,
            action,
            description,
            log_datetime
        )

    )


    conn.commit()

    conn.close()





# ==========================================================
# GET ALL AUDIT LOGS
# ==========================================================

def get_all_audit_logs():


    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT
            audit_id,
            log_datetime,
            username,
            role,
            module,
            action,
            description

        FROM audit_logs

        ORDER BY audit_id DESC

        """
    )


    logs = cursor.fetchall()


    conn.close()


    return logs 