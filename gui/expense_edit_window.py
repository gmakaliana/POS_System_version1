
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
- Display success and error messages.
- Close the window safely.

Company:
GeoMaka Technologies
"""

import tkinter as tk
from tkinter import messagebox

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
# FORMAT EXPENSE VALUE
# ==========================================================

def _get_expense_value(
    expense,
    key,
    index
):
    """
    Safely retrieves an expense field.

    Supports:

    1. Dictionary-style records
    2. SQLite tuple/list records
    """

    try:

        return expense[key]

    except (
        TypeError,
        KeyError,
        IndexError
    ):

        pass

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
    expense
):
    """
    Opens the Edit Expense window.

    Parameters:

        parent:
            Parent Tkinter window.

        expense:
            Existing expense record.

    Returns:

        Tkinter Toplevel window.
    """

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
    # HIDE PARENT
    # ======================================================

    if (
        parent
        and
        parent.winfo_exists()
    ):

        parent.withdraw()


    # ======================================================
    # CREATE WINDOW
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
        360
    )


    # ======================================================
    # CLOSE WINDOW
    # ======================================================

    def close_window():

        root.destroy()

        if (
            parent
            and
            parent.winfo_exists()
        ):

            parent.deiconify()


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
        str(expense_name)
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
        str(description)
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


    amount_entry.insert(
        0,
        str(cost_amount)
    )


    # ======================================================
    # UPDATE EXPENSE
    # ======================================================

    def save_changes():

        # --------------------------------------------------
        # GET INPUT
        # --------------------------------------------------

        new_name = name_entry.get().strip()

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

            name_entry.focus()

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

            amount_entry.focus()

            return


        try:

            amount = float(
                new_amount
            )

        except ValueError:

            messagebox.showwarning(
                "Invalid Amount",
                "Cost amount must be a valid number.",
                parent=root
            )

            amount_entry.focus()

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

            amount_entry.focus()

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
        # SUCCESS
        # ==================================================

        messagebox.showinfo(
            "Expense Updated",
            "Expense updated successfully.",
            parent=root
        )


        # ==================================================
        # CLOSE WINDOW
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


    return root

