
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
- Display the exact username of the user who entered an expense.
- Use the currently logged-in user ID internally when creating expenses.
- Store expense dates in YYYY-MM-DD format.
- Store creation timestamps in YYYY-MM-DD HH:MM:SS format.
- Record expense activities in the audit log.
- Prevent audit failures from interrupting expense operations.

Important:

- expense_id remains stored and used internally.
- entered_by stores the user's ID in the expenses table.
- Expense retrieval joins the users table so the GUI receives
  the exact username instead of the user ID.
- This is a standalone POS using the local database.

Company:
GeoMaka Technologies
"""


from datetime import datetime


from database.db import (
    get_connection
)


from auth.session import (
    get_session_user
)


from modules.audit.audit_logs import (
    log_activity
)


# ==========================================================
# DATE FORMAT
# ==========================================================

def _format_expense_date(
    value
):
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


    value = str(
        value
    )


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

    The expense ID is included in the returned database record
    for internal operations such as editing and deleting.

    The entered_by field is resolved to the exact username
    from the users table.

    Returned structure:

        (
            expense_id,
            expense_name,
            description,
            cost_amount,
            expense_date,
            created_at,
            username
        )

    Returns:

        List of expense records ordered from newest to oldest.

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
        #
        # entered_by contains the user ID.
        #
        # JOIN users to retrieve the exact username.
        #
        # LEFT JOIN is used so an expense remains visible
        # even if its original user record no longer exists.
        #
        # ==================================================

        cursor.execute(
            """
            SELECT
                e.expense_id,
                e.expense_name,
                e.description,
                e.cost_amount,
                e.expense_date,
                e.created_at,
                u.username

            FROM expenses e

            LEFT JOIN users u
                ON e.entered_by = u.user_id

            ORDER BY
                e.expense_id DESC
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

    The returned entered_by field contains the exact
    username instead of the internal user ID.

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
                e.expense_id,
                e.expense_name,
                e.description,
                e.cost_amount,
                e.expense_date,
                e.created_at,
                u.username

            FROM expenses e

            LEFT JOIN users u
                ON e.entered_by = u.user_id

            WHERE e.expense_id = ?

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

    The currently logged-in user's ID is stored in
    the entered_by column.

    The username is resolved through the users table
    whenever the expense is retrieved.

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
            # Audit failure must never affect the completed
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

    The entered_by field contains the exact username.

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
                e.expense_id,
                e.expense_name,
                e.description,
                e.cost_amount,
                e.expense_date,
                e.created_at,
                u.username

            FROM expenses e

            LEFT JOIN users u
                ON e.entered_by = u.user_id

            WHERE e.expense_date = ?

            ORDER BY
                e.expense_id DESC

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

    The entered_by field contains the exact username.

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
                e.expense_id,
                e.expense_name,
                e.description,
                e.cost_amount,
                e.expense_date,
                e.created_at,
                u.username

            FROM expenses e

            LEFT JOIN users u
                ON e.entered_by = u.user_id

            WHERE substr(
                e.expense_date,
                1,
                7
            ) = ?

            ORDER BY
                e.expense_id DESC

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

