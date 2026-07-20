# modules/users/user_management.py

from database.db import get_connection
from auth.password_utils import hash_password

from auth.permissions import (
    can_view_user,
    can_create_user,
    can_edit_user,
    can_change_role,
    can_delete_user,
    can_reset_password
)

from datetime import datetime

from auth.password_policy import validate_password
from modules.audit.audit_logs import log_activity


# =====================================================
# GET ALL VISIBLE USERS
# =====================================================

def get_visible_users(current_user):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT 
            user_id,
            username,
            role,
            must_change_password
        FROM users
    """)


    users = cursor.fetchall()

    conn.close()


    visible_users = []


    for user in users:

        user_data = {
            "user_id": user[0],
            "username": user[1],
            "role": user[2],
            "must_change_password": user[3]
        }


        if can_view_user(
            current_user,
            user_data["role"]
        ):

            visible_users.append(user_data)


    return visible_users





# =====================================================
# CREATE USER
# =====================================================

def add_user(
        creator,
        username,
        password,
        role
):


    if not username or not password:

        raise Exception(
            "Username and password required."
        )

    valid, message = validate_password(password)


    if not valid:

        raise Exception(message)


    if role == "System Admin":

        raise Exception(
            "System Admin accounts cannot be created."
        )



    if not can_create_user(
        creator,
        role
    ):

        raise Exception(
            "You do not have permission to create this role."
        )



    conn = get_connection()
    cursor = conn.cursor()


    try:

        cursor.execute("""
            INSERT INTO users
            (
                username,
                password_hash,
                role,
                must_change_password,
                is_active,
                created_at
            )

            VALUES (?, ?, ?, ?, ?, ?)

        """,
        (
            username,
            hash_password(password),
            role,
            1,
            1,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        ))


        conn.commit()

        log_activity(
            module="USERS",
            action="CREATE",
            description="User created"
        )

    finally:

        conn.close()





# =====================================================
# GET USER BY ID
# =====================================================

def get_user_by_id(user_id):

    conn = get_connection()
    cursor = conn.cursor()


    cursor.execute("""
        SELECT
            user_id,
            username,
            role,
            must_change_password
        FROM users
        WHERE user_id=?
    """,
    (
        user_id,
    ))


    user = cursor.fetchone()

    conn.close()



    if not user:

        return None



    return {

        "user_id": user[0],
        "username": user[1],
        "role": user[2],
        "must_change_password": user[3]

    }





# =====================================================
# UPDATE USER
# =====================================================

def update_user(
        editor,
        user_id,
        username,
        role
):


    target_user = get_user_by_id(
        user_id
    )


    if not target_user:

        raise Exception(
            "User not found."
        )



    # Protect System Admin

    if target_user["role"] == "System Admin":

        raise Exception(
            "System Admin account cannot be edited."
        )



    if not can_edit_user(
        editor,
        target_user
    ):

        raise Exception(
            "You do not have permission to edit this user."
        )



    final_role = target_user["role"]
 
    original_role = target_user["role"]


    if can_change_role(
        editor,
        target_user,
        role
    ):

        final_role = role



    conn = get_connection()
    cursor = conn.cursor()


    try:

        cursor.execute("""
            UPDATE users

            SET username=?,
                role=?

            WHERE user_id=?

        """,
        (
            username,
            final_role,
            user_id
        ))


        conn.commit()

        if original_role != final_role:

            log_activity(
                module="USERS",
                action="ROLE_CHANGE",
                description="User role changed"
        )

        else:

            log_activity(
                module="USERS",
                action="UPDATE",
                description="User edited"
            )

    finally:

        conn.close()





# =====================================================
# DELETE USER
# =====================================================

def delete_user(
        deleter,
        user_id
):


    target_user = get_user_by_id(
        user_id
    )


    if not target_user:

        raise Exception(
            "User not found."
        )



    if target_user["role"] == "System Admin":

        raise Exception(
            "System Admin cannot be deleted."
        )



    if not can_delete_user(
        deleter,
        target_user
    ):

        raise Exception(
            "You do not have permission to delete this user."
        )



    conn = get_connection()
    cursor = conn.cursor()


    try:

        cursor.execute("""
            DELETE FROM users
            WHERE user_id=?

        """,
        (
            user_id,
        ))


        conn.commit()

        log_activity(
            module="USERS",
            action="DELETE",
            description="User deleted"
        )

    finally:

        conn.close()





# =====================================================
# RESET PASSWORD
# =====================================================

def reset_password(
        resetter,
        user_id,
        new_password
):


    if not new_password:

        raise Exception(
            "Password cannot be empty."
        )

    valid, message = validate_password(new_password)


    if not valid:

        raise Exception(message)


    target_user = get_user_by_id(
        user_id
    )


    if not target_user:

        raise Exception(
            "User not found."
        )



    if target_user["role"] == "System Admin":

        # allowed only if resetter is System Admin

        if resetter["role"] != "System Admin":

            raise Exception(
                "Only System Admin can reset System Admin password."
            )



    if not can_reset_password(
        resetter,
        target_user
    ):

        raise Exception(
            "You do not have permission to reset this password."
        )



    conn = get_connection()
    cursor = conn.cursor()


    try:

        cursor.execute("""
            UPDATE users

            SET password_hash=?,
                must_change_password=1

            WHERE user_id=?

        """,
        (
            hash_password(new_password),
            user_id
        ))


        conn.commit()

        log_activity(
            module="USERS",
            action="PASSWORD_RESET",
            description="Password reset"
        )

    finally:

        conn.close()