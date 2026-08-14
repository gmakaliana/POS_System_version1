"""
GeoMaka POS Audit Log Management

File:
modules/audit/audit_log.py

Purpose:
Manage audit log records for GeoMaka POS.

Responsibilities:

- Record user activities.
- Record system activities.
- Retrieve audit logs.
- Support audit log reporting/export.
- Prevent audit logging failures from interrupting
  the main POS operation.
- Store audit timestamps in YYYY-MM-DD HH:MM:SS format.
- Preserve short audit descriptions supplied by modules.

Company:
GeoMaka Technologies
"""

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
    Saves an activity into the audit_logs table.

    Parameters:

        module:
            Module where the activity occurred.

        action:
            Action performed.

        description:
            Short description of the activity.

    Example:

        log_activity(
            "PRODUCTS",
            "UPDATE",
            "Product edited"
        )

    Returns:

        True:
            Audit log saved successfully.

        False:
            Audit log could not be saved.

    IMPORTANT:

        This function does not modify the description.

        The calling module is responsible for providing
        a short audit description.
    """

    # ======================================================
    # GET CURRENT SESSION USER
    # ======================================================

    user = get_session_user()


    if user:

        user_id = user["user_id"]

        username = user["username"]

        role = user["role"]


    else:

        # --------------------------------------------------
        # SYSTEM EVENT
        # --------------------------------------------------

        user_id = None

        username = "SYSTEM"

        role = "SYSTEM"


    # ======================================================
    # LOG DATE AND TIME
    # ======================================================
    #
    # Required format:
    #
    # YYYY-MM-DD HH:MM:SS
    #
    # Example:
    #
    # 2026-08-13 14:27:29
    #
    # ======================================================

    log_datetime = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    conn = None


    try:

        # ==================================================
        # DATABASE CONNECTION
        # ==================================================

        conn = get_connection()

        cursor = conn.cursor()


        # ==================================================
        # INSERT AUDIT LOG
        # ==================================================

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


        # ==================================================
        # COMMIT AUDIT LOG
        # ==================================================

        conn.commit()


        return True


    except Exception:

        # ==================================================
        # AUDIT FAILURE
        # ==================================================
        #
        # Audit logging must NEVER cause the main POS
        # operation to fail.
        #
        # Example:
        #
        # Sale completed
        #       ↓
        # Audit log fails
        #       ↓
        # Sale remains completed
        #
        # ==================================================

        if conn:

            try:

                conn.rollback()

            except Exception:

                pass


        return False


    finally:

        # ==================================================
        # CLOSE DATABASE CONNECTION
        # ==================================================

        if conn:

            try:

                conn.close()

            except Exception:

                pass


# ==========================================================
# GET ALL AUDIT LOGS
# ==========================================================

def get_all_audit_logs():
    """
    Retrieves all audit logs.

    Returns:

        List of audit log records ordered from
        newest to oldest.

    If the database operation fails,
    an empty list is returned.
    """

    conn = None


    try:

        # ==================================================
        # DATABASE CONNECTION
        # ==================================================

        conn = get_connection()

        cursor = conn.cursor()


        # ==================================================
        # GET AUDIT LOGS
        # ==================================================

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


        return logs


    except Exception:

        return []


    finally:

        # ==================================================
        # CLOSE DATABASE CONNECTION
        # ==================================================

        if conn:

            try:

                conn.close()

            except Exception:

                pass