"""
GeoMaka POS Expense Management Window

File:
gui/expense_management_window.py

Purpose:
Display and manage GeoMaka POS expenses.

Responsibilities:

- Display all expenses.
- Display expense name.
- Display description.
- Display cost amount.
- Display expense date.
- Display created date/time.
- Display the exact username of the user
  who entered the expense.
- Keep Expense ID for internal operations only.
- Allow authorized users to add expenses.
- Allow authorized users to edit expenses.
- Allow authorized users to delete expenses.
- Refresh the expense list after changes.
- Keep the Expense Management window open
  while Add/Edit windows are open.
- Prevent interaction with Expense Management
  while Add/Edit windows are open.
- Handle database errors safely.
- Restore the parent window when closed.

Important:

- Expense ID is used internally but is NOT displayed.
- entered_by is stored internally as the user ID.
- The expense management module resolves entered_by
  to the exact username when retrieving expenses.
- The GUI displays the username only.
- The raw user ID is never displayed.
- Expense permissions are enforced by the caller and
  the expense management module.
- Audit logging is handled by the expense management
  module.
- This is a standalone POS using the local database.

UI:

- Window opens horizontally centered.
- Window opens near the top of the screen.
- Table strictly displays 9 rows.
- Table height is sized around exactly 9 Treeview rows.
- No large unused area is left below the table.

Company:
GeoMaka Technologies
"""

import tkinter as tk

from tkinter import (
    ttk,
    messagebox
)


# ==========================================================
# SESSION
# ==========================================================

from auth.session import (
    get_session_user
)


# ==========================================================
# EXPENSE PERMISSIONS
# ==========================================================

from auth.permissions import (
    can_manage_expenses
)


# ==========================================================
# EXPENSE MANAGEMENT
# ==========================================================

from modules.expenses.expense_management import (
    get_all_expenses,
    delete_expense
)


# ==========================================================
# ADD EXPENSE WINDOW
# ==========================================================

from gui.expense_add_window import (
    open_expense_add_window
)


# ==========================================================
# EDIT EXPENSE WINDOW
# ==========================================================

from gui.expense_edit_window import (
    open_expense_edit_window
)


# ==========================================================
# WINDOW POSITIONING
# ==========================================================

def position_expense_window(
    window,
    width,
    height
):
    """
    Positions the Expense Management window
    horizontally centered and near the top
    of the screen.

    This follows the same positioning style
    used by the Sales window.

    A small top margin of 40 pixels is used.
    """

    screen_width = (
        window.winfo_screenwidth()
    )

    # ------------------------------------------------------
    # Horizontal center
    # ------------------------------------------------------

    x = (
        screen_width // 2
        -
        width // 2
    )

    # ------------------------------------------------------
    # Small top margin
    # ------------------------------------------------------

    y = 40

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

    1. Dictionary-style database rows.
    2. Tuple/list database rows.

    Current tuple structure returned by
    expense_management.py:

        (
            expense_id,
            expense_name,
            description,
            cost_amount,
            expense_date,
            created_at,
            username
        )

    Expense ID remains available internally but
    is never displayed in the Treeview.
    """

    # ------------------------------------------------------
    # Dictionary / sqlite Row
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
# GET ENTERED-BY USERNAME
# ==========================================================

def _get_entered_by_username(
    expense
):
    """
    Retrieves the exact username of the user
    who entered the expense.

    Current expense_management.py result:

        (
            expense_id,
            expense_name,
            description,
            cost_amount,
            expense_date,
            created_at,
            username
        )

    Therefore:

        index 6 = username

    The raw entered_by user ID is never used
    as a display fallback.

    Returns:

        Exact username if available.

        Empty string if the username cannot
        be resolved.
    """

    # ------------------------------------------------------
    # Preferred dictionary / Row field
    #
    # Supports:
    #
    #     entered_by_username
    # ------------------------------------------------------

    try:

        username = expense[
            "entered_by_username"
        ]

        if username is not None:

            return str(
                username
            )

    except (
        TypeError,
        KeyError,
        IndexError
    ):

        pass


    # ------------------------------------------------------
    # Also support:
    #
    #     username
    # ------------------------------------------------------

    try:

        username = expense[
            "username"
        ]

        if username is not None:

            return str(
                username
            )

    except (
        TypeError,
        KeyError,
        IndexError
    ):

        pass


    # ------------------------------------------------------
    # Current tuple/list structure
    #
    # Index 6 = username
    # ------------------------------------------------------

    try:

        username = expense[6]

        if username is not None:

            return str(
                username
            )

    except (
        TypeError,
        IndexError
    ):

        pass


    # ------------------------------------------------------
    # IMPORTANT:
    #
    # Do NOT fall back to a separate entered_by ID.
    #
    # The GUI must never display the user ID.
    # ------------------------------------------------------

    return ""


# ==========================================================
# FORMAT MONEY
# ==========================================================

def _format_amount(
    value
):
    """
    Formats an expense amount as:

        850.00
    """

    try:

        return (
            f"{float(value):.2f}"
        )

    except (
        TypeError,
        ValueError
    ):

        return "0.00"


# ==========================================================
# EXPENSE MANAGEMENT WINDOW
# ==========================================================

def open_expense_management_window(
    parent
):
    """
    Opens the Expense Management window.

    Parameters:

        parent:
            Parent Tkinter window.

    Returns:

        Tkinter Toplevel window.

    Access:

        System Admin
        Default Admin
        Admin

        Cashier:
            No access.

    Important:

        The Expense Management window remains
        open when Add Expense or Edit Expense
        windows are opened.

        Add/Edit windows are modal child windows.
        The Expense Management window remains
        underneath them and cannot be interacted
        with until the child window is closed.
    """

    # ======================================================
    # GET CURRENT USER
    # ======================================================

    current_user = get_session_user()


    # ======================================================
    # CHECK SESSION
    # ======================================================

    if not current_user:

        messagebox.showerror(
            "Error",
            "Session expired.",
            parent=parent
        )

        return None


    # ======================================================
    # CHECK EXPENSE PERMISSION
    # ======================================================

    if not can_manage_expenses(
        current_user
    ):

        messagebox.showerror(
            "Access Denied",
            (
                "You do not have permission "
                "to access Expenses."
            ),
            parent=parent
        )

        return None


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
    # CREATE EXPENSE MANAGEMENT WINDOW
    # ======================================================

    root = tk.Toplevel(
        parent
    )

    root.title(
        "EXPENSE MANAGEMENT"
    )


    # ======================================================
    # WINDOW SIZE / POSITION
    # ======================================================
    #
    # The table is intentionally restricted to exactly
    # 9 Treeview rows.
    #
    # Treeview rowheight:
    #
    #     28 pixels
    #
    # Header:
    #
    #     approximately 30 pixels
    #
    # Table height:
    #
    #     9 rows
    #
    # The total window height is kept compact so there
    # is no unnecessary vertical space.
    #
    # ======================================================

    EXPENSE_WIDTH = 1100

    EXPENSE_HEIGHT = 500

    position_expense_window(
        root,
        EXPENSE_WIDTH,
        EXPENSE_HEIGHT
    )


    # ======================================================
    # RESIZABLE WINDOW
    # ======================================================

    root.resizable(
        True,
        True
    )


    # ======================================================
    # MINIMUM WINDOW SIZE
    # ======================================================
    #
    # The minimum height still accommodates:
    #
    # - Title
    # - 9 table rows
    # - Scrollbar
    # - Buttons
    #
    # ======================================================

    root.minsize(
        950,
        500
    )


    # ======================================================
    # FONT SETTINGS
    # ======================================================

    FONT_TITLE = (
        "Arial",
        16,
        "bold"
    )

    FONT_TABLE = (
        "Arial",
        10
    )

    FONT_TABLE_HEADING = (
        "Arial",
        10,
        "bold"
    )

    FONT_BUTTON = (
        "Arial",
        10,
        "bold"
    )


    # ======================================================
    # TREEVIEW STYLE
    # ======================================================

    style = ttk.Style(
        root
    )

    try:

        style.configure(
            "Expense.Treeview",
            font=FONT_TABLE,
            rowheight=28
        )

        style.configure(
            "Expense.Treeview.Heading",
            font=FONT_TABLE_HEADING,
            padding=3
        )

    except Exception:

        pass


    # ======================================================
    # CLOSE EXPENSE MANAGEMENT WINDOW
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
        text="EXPENSE MANAGEMENT",
        font=FONT_TITLE
    ).pack(
        pady=(8, 6)
    )


    # ======================================================
    # TABLE FRAME
    # ======================================================

    table_frame = tk.Frame(
        root
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=(2, 5)
    )


    # ======================================================
    # TABLE COLUMNS
    #
    # Expense ID is deliberately NOT included.
    # ======================================================

    columns = (

        "Expense Name",

        "Description",

        "Cost Amount",

        "Expense Date",

        "Created At",

        "Entered By"

    )


    # ======================================================
    # TREEVIEW
    # ======================================================
    #
    # STRICTLY 9 ROWS.
    #
    # This controls the visible height of the Treeview
    # independently of the number of expense records.
    #
    # ======================================================

    tree = ttk.Treeview(

        table_frame,

        columns=columns,

        show="headings",

        selectmode="browse",

        height=9,

        style="Expense.Treeview"

    )


    # ======================================================
    # HEADINGS
    # ======================================================

    tree.heading(
        "Expense Name",
        text="Expense Name"
    )

    tree.heading(
        "Description",
        text="Description"
    )

    tree.heading(
        "Cost Amount",
        text="Cost Amount (M)"
    )

    tree.heading(
        "Expense Date",
        text="Expense Date"
    )

    tree.heading(
        "Created At",
        text="Created At"
    )

    tree.heading(
        "Entered By",
        text="Entered By"
    )


    # ======================================================
    # COLUMN WIDTHS
    # ======================================================

    tree.column(
        "Expense Name",
        width=180,
        minwidth=140,
        anchor="w"
    )

    tree.column(
        "Description",
        width=300,
        minwidth=200,
        anchor="w"
    )

    tree.column(
        "Cost Amount",
        width=130,
        minwidth=110,
        anchor="w"
    )

    tree.column(
        "Expense Date",
        width=130,
        minwidth=110,
        anchor="w"
    )

    tree.column(
        "Created At",
        width=170,
        minwidth=140,
        anchor="w"
    )

    tree.column(
        "Entered By",
        width=150,
        minwidth=120,
        anchor="w"
    )


    # ======================================================
    # VERTICAL SCROLLBAR
    # ======================================================

    vertical_scrollbar = ttk.Scrollbar(

        table_frame,

        orient="vertical",

        command=tree.yview

    )


    tree.configure(
        yscrollcommand=vertical_scrollbar.set
    )


    # ======================================================
    # HORIZONTAL SCROLLBAR
    # ======================================================

    horizontal_scrollbar = ttk.Scrollbar(

        table_frame,

        orient="horizontal",

        command=tree.xview

    )


    tree.configure(
        xscrollcommand=horizontal_scrollbar.set
    )


    # ======================================================
    # PACK / GRID TREE
    # ======================================================

    tree.grid(
        row=0,
        column=0,
        sticky="nsew"
    )

    vertical_scrollbar.grid(
        row=0,
        column=1,
        sticky="ns"
    )

    horizontal_scrollbar.grid(
        row=1,
        column=0,
        sticky="ew"
    )


    table_frame.grid_rowconfigure(
        0,
        weight=1
    )

    table_frame.grid_columnconfigure(
        0,
        weight=1
    )


    # ======================================================
    # CURRENT EXPENSE RECORDS
    # ======================================================
    #
    # Complete records are retained internally.
    #
    # This allows:
    #
    # - Expense ID to remain available for deletion.
    # - Expense ID to remain available for editing.
    #
    # Expense ID is never displayed.
    #
    # ======================================================

    expenses_data = []


    # ======================================================
    # LOAD EXPENSES
    # ======================================================

    def load_expenses():

        # --------------------------------------------------
        # CLEAR TABLE
        # --------------------------------------------------

        for item in tree.get_children():

            tree.delete(
                item
            )


        # --------------------------------------------------
        # CLEAR INTERNAL DATA
        # --------------------------------------------------

        expenses_data.clear()


        # --------------------------------------------------
        # GET EXPENSES
        # --------------------------------------------------

        try:

            expenses = get_all_expenses()

            if expenses is None:

                expenses = []


        except Exception as error:

            messagebox.showerror(
                "Expense Error",
                (
                    "Unable to load expenses.\n\n"
                    f"Error:\n{error}"
                ),
                parent=root
            )

            return


        # --------------------------------------------------
        # STORE COMPLETE RECORDS
        # --------------------------------------------------

        expenses_data.extend(
            expenses
        )


        # --------------------------------------------------
        # DISPLAY EXPENSES
        # --------------------------------------------------

        for expense in expenses:

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

            expense_date = _get_expense_value(
                expense,
                "expense_date",
                4
            )

            created_at = _get_expense_value(
                expense,
                "created_at",
                5
            )


            # --------------------------------------------------
            # Display exact username.
            #
            # Never display entered_by user ID.
            # --------------------------------------------------

            entered_by_username = (
                _get_entered_by_username(
                    expense
                )
            )


            tree.insert(

                "",

                "end",

                values=(

                    expense_name,

                    description,

                    _format_amount(
                        cost_amount
                    ),

                    expense_date,

                    created_at,

                    entered_by_username

                )

            )


        # --------------------------------------------------
        # NO EXPENSES
        # --------------------------------------------------

        if not expenses:

            tree.insert(

                "",

                "end",

                values=(

                    "",

                    "No expense records found.",

                    "",

                    "",

                    "",

                    ""

                )

            )


    # ======================================================
    # GET SELECTED EXPENSE
    # ======================================================

    def get_selected_expense():

        selection = tree.selection()


        if not selection:

            messagebox.showwarning(
                "Expense Selection",
                "Please select an expense.",
                parent=root
            )

            return None


        selected_item = selection[0]


        # --------------------------------------------------
        # Determine row position.
        # --------------------------------------------------

        children = tree.get_children()


        try:

            row_index = children.index(
                selected_item
            )

        except ValueError:

            return None


        # --------------------------------------------------
        # Prevent selection of empty message.
        # --------------------------------------------------

        if row_index >= len(
            expenses_data
        ):

            messagebox.showwarning(
                "Expense Selection",
                "Please select a valid expense.",
                parent=root
            )

            return None


        return expenses_data[
            row_index
        ]


    # ======================================================
    # ADD EXPENSE
    # ======================================================

    def add_new_expense():

        # --------------------------------------------------
        # IMPORTANT:
        #
        # Do NOT withdraw or destroy the Expense
        # Management window.
        #
        # The Add Expense window is opened as a
        # modal child window.
        # --------------------------------------------------

        open_expense_add_window(

            root,

            on_saved=load_expenses

        )


    # ======================================================
    # EDIT EXPENSE
    # ======================================================

    def edit_selected_expense():

        expense = get_selected_expense()


        if not expense:

            return


        # --------------------------------------------------
        # IMPORTANT:
        #
        # Do NOT withdraw or destroy the Expense
        # Management window.
        #
        # The Edit Expense window is opened as a
        # modal child window.
        # --------------------------------------------------

        open_expense_edit_window(

            root,

            expense,

            on_saved=load_expenses

        )


    # ======================================================
    # DELETE EXPENSE
    # ======================================================

    def delete_selected_expense():

        expense = get_selected_expense()


        if not expense:

            return


        # --------------------------------------------------
        # Expense ID is retrieved internally only.
        #
        # It is NEVER displayed in the table.
        # --------------------------------------------------

        expense_id = _get_expense_value(
            expense,
            "expense_id",
            0
        )


        expense_name = _get_expense_value(
            expense,
            "expense_name",
            1
        )


        if not expense_id:

            messagebox.showerror(
                "Delete Expense",
                "The selected expense has no valid ID.",
                parent=root
            )

            return


        # --------------------------------------------------
        # CONFIRM DELETE
        # --------------------------------------------------

        confirmed = messagebox.askyesno(

            "Delete Expense",

            (
                "Are you sure you want to delete "
                f"the expense '{expense_name}'?"
            ),

            parent=root

        )


        if not confirmed:

            return


        # --------------------------------------------------
        # DELETE
        # --------------------------------------------------

        try:

            result = delete_expense(
                expense_id
            )


        except Exception as error:

            messagebox.showerror(
                "Delete Expense Error",
                (
                    "The expense could not be deleted.\n\n"
                    f"Error:\n{error}"
                ),
                parent=root
            )

            return


        # --------------------------------------------------
        # HANDLE FAILED DELETE
        # --------------------------------------------------

        if result is False:

            messagebox.showerror(
                "Delete Expense",
                "The expense could not be deleted.",
                parent=root
            )

            return


        # --------------------------------------------------
        # SUCCESS
        # --------------------------------------------------

        messagebox.showinfo(
            "Expense Deleted",
            "Expense deleted successfully.",
            parent=root
        )


        # --------------------------------------------------
        # REFRESH
        # --------------------------------------------------

        load_expenses()


    # ======================================================
    # BUTTON FRAME
    # ======================================================

    button_frame = tk.Frame(
        root
    )

    button_frame.pack(
        fill="x",
        padx=10,
        pady=(3, 8)
    )


    # ======================================================
    # ADD BUTTON
    # ======================================================

    tk.Button(

        button_frame,

        text="Add Expense",

        width=14,

        bg="#27ae60",

        fg="white",

        font=FONT_BUTTON,

        command=add_new_expense

    ).pack(

        side="left",

        padx=5,

        ipadx=3,

        ipady=3

    )


    # ======================================================
    # EDIT BUTTON
    # ======================================================

    tk.Button(

        button_frame,

        text="Edit Expense",

        width=14,

        bg="#2980b9",

        fg="white",

        font=FONT_BUTTON,

        command=edit_selected_expense

    ).pack(

        side="left",

        padx=5,

        ipadx=3,

        ipady=3

    )


    # ======================================================
    # DELETE BUTTON
    # ======================================================

    tk.Button(

        button_frame,

        text="Delete Expense",

        width=14,

        bg="#c0392b",

        fg="white",

        font=FONT_BUTTON,

        command=delete_selected_expense

    ).pack(

        side="left",

        padx=5,

        ipadx=3,

        ipady=3

    )


    # ======================================================
    # CLOSE BUTTON
    # ======================================================

    tk.Button(

        button_frame,

        text="Close",

        width=14,

        bg="#7f8c8d",

        fg="white",

        font=FONT_BUTTON,

        command=close_window

    ).pack(

        side="right",

        padx=5,

        ipadx=3,

        ipady=3

    )


    # ======================================================
    # WINDOW CLOSE EVENT
    # ======================================================

    root.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )


    # ======================================================
    # INITIAL LOAD
    # ======================================================

    load_expenses()


    # ======================================================
    # RETURN WINDOW
    # ======================================================

    return root
