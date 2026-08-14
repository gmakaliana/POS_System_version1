
"""
GeoMaka POS Expense Management

File:
modules/expenses/expense_management.py

Purpose:
Manage business expenses for GeoMaka POS.

Responsibilities:

- Retrieve all expenses.
- Retrieve an expense by ID.
- Add new expenses.
- Edit existing expenses.
- Delete expenses.
- Retrieve daily expenses.
- Retrieve monthly expenses.
- Record expense activities in the audit log.
- Use the currently logged-in user as the expense creator.
- Store expense dates in YYYY-MM-DD format.
- Store creation timestamps in YYYY-MM-DD HH:MM:SS format.
- Prevent audit failures from interrupting expense operations.

Company:
GeoMaka Technologies
"""

from datetime import datetime

from database.db import get_connection

from auth.session import get_session_user

from modules.audit.audit_logs import (
    log_activity
)


# ==========================================================
# DATE FORMAT
# ==========================================================

def _format_expense_date(value):
    """
    Converts an expense date to:

        YYYY-MM-DD

    Supports datetime objects and date strings.
    """

    if isinstance(
        value,
        datetime
    ):

        return value.strftime(
            "%Y-%m-%d"
        )


    value = str(value)


    # ------------------------------------------------------
    # If a complete datetime was supplied,
    # keep only the date portion.
    # ------------------------------------------------------

    if len(value) >= 10:

        return value[:10]


    return value


# ==========================================================
# DATETIME FORMAT
# ==========================================================

def _get_current_datetime():
    """
    Returns the current date/time as:

        YYYY-MM-DD HH:MM:SS
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# ==========================================================
# GET CURRENT USER ID
# ==========================================================

def _get_current_user_id():
    """
    Returns the user ID of the currently logged-in user.

    Returns:

        user_id:
            Current logged-in user ID.

        None:
            If no user is logged in.
    """

    user = get_session_user()


    if not user:

        return None


    return user.get(
        "user_id"
    )


# ==========================================================
# GET ALL EXPENSES
# ==========================================================

def get_all_expenses():
    """
    Retrieves all expenses.

    Returns:

        List of expense records ordered from
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
        # GET EXPENSES
        # ==================================================

        cursor.execute(
            """
            SELECT
                expense_id,
                expense_name,
                description,
                cost_amount,
                expense_date,
                created_at,
                entered_by

            FROM expenses

            ORDER BY
                expense_id DESC
            """
        )


        expenses = cursor.fetchall()


        return expenses


    except Exception:

        return []


    finally:

        # ==================================================
        # CLOSE CONNECTION
        # ==================================================

        if conn:

            try:

                conn.close()

            except Exception:

                pass


# ==========================================================
# GET EXPENSE BY ID
# ==========================================================

def get_expense_by_id(
    expense_id
):
    """
    Retrieves a single expense by expense ID.

    Parameters:

        expense_id:
            ID of the expense to retrieve.

    Returns:

        Expense record if found.

        None if the expense does not exist
        or the database operation fails.
    """

    conn = None


    try:

        # ==================================================
        # DATABASE CONNECTION
        # ==================================================

        conn = get_connection()

        cursor = conn.cursor()


        # ==================================================
        # GET EXPENSE
        # ==================================================

        cursor.execute(
            """
            SELECT
                expense_id,
                expense_name,
                description,
                cost_amount,
                expense_date,
                created_at,
                entered_by

            FROM expenses

            WHERE expense_id = ?

            """,

            (
                expense_id,
            )
        )


        return cursor.fetchone()


    except Exception:

        return None


    finally:

        # ==================================================
        # CLOSE CONNECTION
        # ==================================================

        if conn:

            try:

                conn.close()

            except Exception:

                pass


# ==========================================================
# ADD EXPENSE
# ==========================================================

def add_expense(
    expense_name,
    description,
    cost_amount
):
    """
    Adds a new expense.

    Parameters:

        expense_name:
            Name/type of the expense.

        description:
            Short description of the expense.

        cost_amount:
            Expense amount.

    Expense date and creation timestamp are generated
    automatically by the system.

    Returns:

        True:
            Expense added successfully.

        False:
            Expense could not be added.
    """

    conn = None


    try:

        # ==================================================
        # GET CURRENT USER
        # ==================================================

        user_id = _get_current_user_id()


        # ==================================================
        # VALIDATE USER
        # ==================================================

        if user_id is None:

            return False


        # ==================================================
        # FORMAT DATE/TIME
        # ==================================================

        expense_date = datetime.now().strftime(
            "%Y-%m-%d"
        )


        created_at = _get_current_datetime()


        # ==================================================
        # DATABASE CONNECTION
        # ==================================================

        conn = get_connection()

        cursor = conn.cursor()


        # ==================================================
        # INSERT EXPENSE
        # ==================================================

        cursor.execute(
            """
            INSERT INTO expenses
            (
                expense_name,
                description,
                cost_amount,
                expense_date,
                created_at,
                entered_by
            )

            VALUES (?, ?, ?, ?, ?, ?)

            """,

            (
                expense_name,
                description,
                cost_amount,
                expense_date,
                created_at,
                user_id
            )
        )


        # ==================================================
        # COMMIT
        # ==================================================

        conn.commit()


        # ==================================================
        # AUDIT LOG
        # ==================================================

        try:

            log_activity(
                module="EXPENSES",
                action="CREATE",
                description="Expense added"
            )

        except Exception:

            # --------------------------------------------------
            # Audit failure must not affect the completed
            # expense operation.
            # --------------------------------------------------

            pass


        return True


    except Exception:

        if conn:

            try:

                conn.rollback()

            except Exception:

                pass


        return False


    finally:

        # ==================================================
        # CLOSE CONNECTION
        # ==================================================

        if conn:

            try:

                conn.close()

            except Exception:

                pass


# ==========================================================
# UPDATE EXPENSE
# ==========================================================

def update_expense(
    expense_id,
    expense_name,
    description,
    cost_amount
):
    """
    Updates an existing expense.

    The original expense date, created_at timestamp,
    and entered_by user are preserved.

    Returns:

        True:
            Expense updated successfully.

        False:
            Expense could not be updated.
    """

    conn = None


    try:

        # ==================================================
        # VALIDATE EXPENSE
        # ==================================================

        if get_expense_by_id(
            expense_id
        ) is None:

            return False


        # ==================================================
        # DATABASE CONNECTION
        # ==================================================

        conn = get_connection()

        cursor = conn.cursor()


        # ==================================================
        # UPDATE EXPENSE
        # ==================================================

        cursor.execute(
            """
            UPDATE expenses

            SET
                expense_name = ?,
                description = ?,
                cost_amount = ?

            WHERE expense_id = ?

            """,

            (
                expense_name,
                description,
                cost_amount,
                expense_id
            )
        )


        # ==================================================
        # COMMIT
        # ==================================================

        conn.commit()


        # ==================================================
        # AUDIT LOG
        # ==================================================

        try:

            log_activity(
                module="EXPENSES",
                action="UPDATE",
                description="Expense edited"
            )

        except Exception:

            pass


        return True


    except Exception:

        if conn:

            try:

                conn.rollback()

            except Exception:

                pass


        return False


    finally:

        # ==================================================
        # CLOSE CONNECTION
        # ==================================================

        if conn:

            try:

                conn.close()

            except Exception:

                pass


# ==========================================================
# DELETE EXPENSE
# ==========================================================

def delete_expense(
    expense_id
):
    """
    Deletes an expense.

    Parameters:

        expense_id:
            ID of the expense to delete.

    Returns:

        True:
            Expense deleted successfully.

        False:
            Expense could not be deleted.
    """

    conn = None


    try:

        # ==================================================
        # VALIDATE EXPENSE
        # ==================================================

        if get_expense_by_id(
            expense_id
        ) is None:

            return False


        # ==================================================
        # DATABASE CONNECTION
        # ==================================================

        conn = get_connection()

        cursor = conn.cursor()


        # ==================================================
        # DELETE EXPENSE
        # ==================================================

        cursor.execute(
            """
            DELETE FROM expenses

            WHERE expense_id = ?

            """,

            (
                expense_id,
            )
        )


        # ==================================================
        # COMMIT
        # ==================================================

        conn.commit()


        # ==================================================
        # AUDIT LOG
        # ==================================================

        try:

            log_activity(
                module="EXPENSES",
                action="DELETE",
                description="Expense deleted"
            )

        except Exception:

            pass


        return True


    except Exception:

        if conn:

            try:

                conn.rollback()

            except Exception:

                pass


        return False


    finally:

        # ==================================================
        # CLOSE CONNECTION
        # ==================================================

        if conn:

            try:

                conn.close()

            except Exception:

                pass


# ==========================================================
# GET DAILY EXPENSES
# ==========================================================

def get_daily_expenses(
    expense_date
):
    """
    Retrieves all expenses for a specific date.

    Parameters:

        expense_date:
            Date in YYYY-MM-DD format.

    Returns:

        List of expenses for the specified date.
    """

    conn = None


    try:

        expense_date = _format_expense_date(
            expense_date
        )


        # ==================================================
        # DATABASE CONNECTION
        # ==================================================

        conn = get_connection()

        cursor = conn.cursor()


        # ==================================================
        # GET DAILY EXPENSES
        # ==================================================

        cursor.execute(
            """
            SELECT
                expense_id,
                expense_name,
                description,
                cost_amount,
                expense_date,
                created_at,
                entered_by

            FROM expenses

            WHERE expense_date = ?

            ORDER BY
                expense_id DESC

            """,

            (
                expense_date,
            )
        )


        return cursor.fetchall()


    except Exception:

        return []


    finally:

        # ==================================================
        # CLOSE CONNECTION
        # ==================================================

        if conn:

            try:

                conn.close()

            except Exception:

                pass


# ==========================================================
# GET MONTHLY EXPENSES
# ==========================================================

def get_monthly_expenses(
    month
):
    """
    Retrieves all expenses for a specified month.

    Parameters:

        month:
            Month in YYYY-MM format.

    Returns:

        List of expenses for the specified month.
    """

    conn = None


    try:

        month = str(
            month
        )[:7]


        # ==================================================
        # DATABASE CONNECTION
        # ==================================================

        conn = get_connection()

        cursor = conn.cursor()


        # ==================================================
        # GET MONTHLY EXPENSES
        # ==================================================

        cursor.execute(
            """
            SELECT
                expense_id,
                expense_name,
                description,
                cost_amount,
                expense_date,
                created_at,
                entered_by

            FROM expenses

            WHERE substr(
                expense_date,
                1,
                7
            ) = ?

            ORDER BY
                expense_id DESC

            """,

            (
                month,
            )
        )


        return cursor.fetchall()


    except Exception:

        return []


    finally:

        # ==================================================
        # CLOSE CONNECTION
        # ==================================================

        if conn:

            try:

                conn.close()

            except Exception:

                pass
