# GeoMaka POS Expense Edit Window


"""
GeoMaka POS Expense Edit Window

File:
gui/expense_edit_window.py

Purpose:
Provide the GUI for editing an existing expense.

Responsibilities:

- Display the selected expense.
- Allow authorized users to edit expense information.
- Validate expense input.
- Update the expense through the expense management module.
- Refresh the Expense Management window after saving.
- Keep the Expense Management window visible.
- Prevent interaction with the Expense Management window
  until this window is closed.
- Display success and error messages.
- Close the edit window safely.

Important:

- The parent Expense Management window is NOT hidden.
- The parent Expense Management window remains visible
  while this window is displayed.
- The Edit Expense window is modal relative to the
  Expense Management window.
- The Expense Management window cannot be interacted
  with until the Edit Expense window is closed.
- The on_saved callback is called after a successful
  expense update.
- Expense ID is used internally only.
- Expense ID is never displayed.

Company:
GeoMaka Technologies
"""

import tkinter as tk

from tkinter import (
    messagebox
)


# ==========================================================
# EXPENSE MANAGEMENT
# ==========================================================

from modules.expenses.expense_management import (
    update_expense
)


# ==========================================================
# CENTER WINDOW
# ==========================================================

def center_window(
    window,
    width,
    height
):
    """
    Centers a Tkinter window on the screen.
    """

    screen_width = (
        window.winfo_screenwidth()
    )

    screen_height = (
        window.winfo_screenheight()
    )

    x = (
        screen_width // 2
        -
        width // 2
    )

    y = (
        screen_height // 2
        -
        height // 2
    )

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )


# ==========================================================
# GET EXPENSE VALUE
# ==========================================================

def _get_expense_value(
    expense,
    key,
    index
):
    """
    Safely retrieves an expense field.

    Supports:

    1. Dictionary-style records.
    2. SQLite tuple/list records.

    Current tuple structure:

        (
            expense_id,
            expense_name,
            description,
            cost_amount,
            expense_date,
            created_at,
            username
        )

    Expense ID is used internally only.
    """

    # ------------------------------------------------------
    # Dictionary / SQLite Row
    # ------------------------------------------------------

    try:

        return expense[key]

    except (
        TypeError,
        KeyError,
        IndexError
    ):

        pass


    # ------------------------------------------------------
    # Tuple / List
    # ------------------------------------------------------

    try:

        return expense[index]

    except (
        TypeError,
        IndexError
    ):

        return ""


# ==========================================================
# EDIT EXPENSE WINDOW
# ==========================================================

def open_expense_edit_window(
    parent,
    expense,
    on_saved=None
):
    """
    Opens the Edit Expense window.

    Parameters:

        parent:
            Parent Expense Management window.

        expense:
            Existing expense record.

        on_saved:
            Optional callback executed after a successful
            expense update.

    Returns:

        Tkinter Toplevel window.

    Important:

        The parent Expense Management window remains
        visible while this window is displayed.

        The parent cannot be interacted with until
        this Edit Expense window is closed.
    """

    # ======================================================
    # VALIDATE PARENT
    # ======================================================

    if (
        parent is None
        or
        not parent.winfo_exists()
    ):

        return None


    # ======================================================
    # VALIDATE EXPENSE
    # ======================================================

    if not expense:

        messagebox.showerror(
            "Edit Expense",
            "No expense was selected.",
            parent=parent
        )

        return None


    # ======================================================
    # GET EXPENSE ID
    # ======================================================

    expense_id = _get_expense_value(
        expense,
        "expense_id",
        0
    )


    if not expense_id:

        messagebox.showerror(
            "Edit Expense",
            "The selected expense has no valid ID.",
            parent=parent
        )

        return None


    # ======================================================
    # GET EXISTING VALUES
    # ======================================================

    expense_name = _get_expense_value(
        expense,
        "expense_name",
        1
    )

    description = _get_expense_value(
        expense,
        "description",
        2
    )

    cost_amount = _get_expense_value(
        expense,
        "cost_amount",
        3
    )


    # ======================================================
    # CREATE EDIT WINDOW
    # ======================================================
    #
    # IMPORTANT:
    #
    # The parent Expense Management window is NOT
    # withdrawn.
    #
    # ======================================================

    root = tk.Toplevel(
        parent
    )


    root.title(
        "EDIT EXPENSE"
    )


    root.resizable(
        False,
        False
    )


    center_window(
        root,
        500,
        260
    )


    # ======================================================
    # KEEP EDIT WINDOW ASSOCIATED WITH PARENT
    # ======================================================

    root.transient(
        parent
    )


    # ======================================================
    # MAKE EDIT WINDOW MODAL
    # ======================================================
    #
    # The Expense Management window remains visible,
    # but the user cannot interact with it while the
    # Edit Expense window is open.
    #
    # The user must close this window first.
    #
    # ======================================================

    root.grab_set()


    # ======================================================
    # CLOSE WINDOW
    # ======================================================

    def close_window():

        # --------------------------------------------------
        # Release modal grab safely.
        # --------------------------------------------------

        try:

            if root.grab_current() == root:

                root.grab_release()

        except Exception:

            pass


        # --------------------------------------------------
        # Destroy only the Edit Expense window.
        # --------------------------------------------------

        if root.winfo_exists():

            root.destroy()


        # --------------------------------------------------
        # Return focus to Expense Management.
        # --------------------------------------------------

        try:

            if parent.winfo_exists():

                parent.lift()

                parent.focus_set()

        except Exception:

            pass


    # ======================================================
    # TITLE
    # ======================================================

    tk.Label(
        root,
        text="EDIT EXPENSE",
        font=(
            "Arial",
            16,
            "bold"
        )
    ).pack(
        pady=15
    )


    # ======================================================
    # FORM FRAME
    # ======================================================

    form_frame = tk.Frame(
        root
    )


    form_frame.pack(
        padx=20,
        pady=5
    )


    # ======================================================
    # EXPENSE NAME
    # ======================================================

    tk.Label(
        form_frame,
        text="Expense Name:"
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=5,
        pady=8
    )


    name_entry = tk.Entry(
        form_frame,
        width=35
    )


    name_entry.grid(
        row=0,
        column=1,
        padx=5,
        pady=8
    )


    name_entry.insert(
        0,
        str(
            expense_name
            if expense_name is not None
            else ""
        )
    )


    # ======================================================
    # DESCRIPTION
    # ======================================================

    tk.Label(
        form_frame,
        text="Description:"
    ).grid(
        row=1,
        column=0,
        sticky="w",
        padx=5,
        pady=8
    )


    description_entry = tk.Entry(
        form_frame,
        width=35
    )


    description_entry.grid(
        row=1,
        column=1,
        padx=5,
        pady=8
    )


    description_entry.insert(
        0,
        str(
            description
            if description is not None
            else ""
        )
    )


    # ======================================================
    # COST AMOUNT
    # ======================================================

    tk.Label(
        form_frame,
        text="Cost Amount (M):"
    ).grid(
        row=2,
        column=0,
        sticky="w",
        padx=5,
        pady=8
    )


    amount_entry = tk.Entry(
        form_frame,
        width=35
    )


    amount_entry.grid(
        row=2,
        column=1,
        padx=5,
        pady=8
    )


    # ------------------------------------------------------
    # Format existing amount safely.
    # ------------------------------------------------------

    try:

        formatted_amount = (
            f"{float(cost_amount):.2f}"
        )

    except (
        TypeError,
        ValueError
    ):

        formatted_amount = str(
            cost_amount
            if cost_amount is not None
            else ""
        )


    amount_entry.insert(
        0,
        formatted_amount
    )


    # ======================================================
    # UPDATE EXPENSE
    # ======================================================

    def save_changes():

        # --------------------------------------------------
        # GET INPUT
        # --------------------------------------------------

        new_name = (
            name_entry
            .get()
            .strip()
        )


        new_description = (
            description_entry
            .get()
            .strip()
        )


        new_amount = (
            amount_entry
            .get()
            .strip()
        )


        # --------------------------------------------------
        # VALIDATE NAME
        # --------------------------------------------------

        if not new_name:

            messagebox.showwarning(
                "Invalid Expense",
                "Please enter an expense name.",
                parent=root
            )

            name_entry.focus_set()

            return


        # --------------------------------------------------
        # VALIDATE DESCRIPTION
        # --------------------------------------------------

        if not new_description:

            messagebox.showwarning(
                "Invalid Expense",
                "Please enter the expense description.",
                parent=root
            )

            description_entry.focus_set()

            return


        # --------------------------------------------------
        # VALIDATE AMOUNT
        # --------------------------------------------------

        if not new_amount:

            messagebox.showwarning(
                "Invalid Amount",
                "Please enter the expense amount.",
                parent=root
            )

            amount_entry.focus_set()

            return


        # --------------------------------------------------
        # CONVERT AMOUNT
        # --------------------------------------------------

        try:

            amount = float(
                new_amount
            )

        except (
            TypeError,
            ValueError
        ):

            messagebox.showwarning(
                "Invalid Amount",
                "Cost amount must be a valid number.",
                parent=root
            )

            amount_entry.focus_set()

            return


        # --------------------------------------------------
        # PREVENT ZERO / NEGATIVE EXPENSE
        # --------------------------------------------------

        if amount <= 0:

            messagebox.showwarning(
                "Invalid Amount",
                "Cost amount must be greater than zero.",
                parent=root
            )

            amount_entry.focus_set()

            return


        # --------------------------------------------------
        # ROUND AMOUNT
        # --------------------------------------------------

        amount = round(
            amount,
            2
        )


        # ==================================================
        # UPDATE DATABASE
        # ==================================================

        try:

            result = update_expense(

                expense_id,

                new_name,

                new_description,

                amount

            )

        except Exception as error:

            messagebox.showerror(
                "Update Expense Error",
                (
                    "The expense could not be updated.\n\n"
                    f"Error:\n{error}"
                ),
                parent=root
            )

            return


        # ==================================================
        # CHECK UPDATE RESULT
        # ==================================================

        if result is False:

            messagebox.showerror(
                "Update Expense",
                "The expense could not be updated.",
                parent=root
            )

            return


        # ==================================================
        # REFRESH PARENT
        # ==================================================
        #
        # Refresh the Expense Management Treeview while
        # keeping the management window open.
        #
        # ==================================================

        if callable(
            on_saved
        ):

            try:

                on_saved()

            except Exception as error:

                messagebox.showerror(
                    "Refresh Error",
                    (
                        "The expense was updated successfully, "
                        "but the expense list could not be "
                        "refreshed.\n\n"
                        f"Error:\n{error}"
                    ),
                    parent=root
                )


        # ==================================================
        # SUCCESS
        # ==================================================

        messagebox.showinfo(
            "Expense Updated",
            "Expense updated successfully.",
            parent=root
        )


        # ==================================================
        # CLOSE EDIT WINDOW ONLY
        # ==================================================
        #
        # Expense Management remains open.
        #
        # ==================================================

        close_window()


    # ======================================================
    # BUTTON FRAME
    # ======================================================

    button_frame = tk.Frame(
        root
    )


    button_frame.pack(
        pady=20
    )


    # ======================================================
    # UPDATE BUTTON
    # ======================================================

    tk.Button(
        button_frame,
        text="Update",
        width=14,
        bg="#27ae60",
        fg="white",
        command=save_changes
    ).pack(
        side="left",
        padx=5
    )


    # ======================================================
    # CANCEL BUTTON
    # ======================================================

    tk.Button(
        button_frame,
        text="Cancel",
        width=14,
        bg="#7f8c8d",
        fg="white",
        command=close_window
    ).pack(
        side="left",
        padx=5
    )


    # ======================================================
    # WINDOW CLOSE EVENT
    # ======================================================

    root.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )


    # ======================================================
    # ENTER = UPDATE
    # ======================================================

    root.bind(
        "<Return>",
        lambda event: save_changes()
    )


    # ======================================================
    # INITIAL FOCUS
    # ======================================================

    name_entry.focus_set()


    # ======================================================
    # KEEP WINDOW ABOVE PARENT
    # ======================================================

    root.lift()


    return root

