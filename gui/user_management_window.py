# gui/user_management_window.py

import tkinter as tk
from tkinter import ttk, messagebox

from auth.session import get_session_user

from auth.permissions import (
    can_create_user,
    can_edit_user,
    can_delete_user,
    can_reset_password
)

from modules.users.user_management import (
    get_visible_users,
    get_user_by_id,
    delete_user
)

from gui.user_edit_window import open_edit_user_window
from gui.user_add_window import open_add_user_window
from gui.reset_password_window import open_reset_password_window


# ==========================================================
# POSITION WINDOW TOWARDS TOP
# ==========================================================

def position_window_top(
    window,
    width,
    height
):
    """
    Positions the window horizontally centered
    and towards the top of the screen.
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
    # Position towards the top
    # ------------------------------------------------------

    y = 40

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )


# ==========================================================
# OPEN USER MANAGEMENT WINDOW
# ==========================================================

def open_user_management_window(
    admin_root
):

    # ======================================================
    # GET CURRENT USER
    # ======================================================

    current_user = get_session_user()


    if not current_user:

        messagebox.showerror(
            "Error",
            "Session expired.",
            parent=admin_root
        )

        return


    # ======================================================
    # CASHIER ACCESS CHECK
    # ======================================================

    if current_user["role"] == "Cashier":

        messagebox.showerror(
            "Access Denied",
            "You cannot access User Management.",
            parent=admin_root
        )

        return


    # ======================================================
    # HIDE ADMIN DASHBOARD
    # ======================================================

    admin_root.withdraw()


    # ======================================================
    # CREATE WINDOW
    # ======================================================

    root = tk.Toplevel(
        admin_root
    )


    root.title(
        "USER MANAGEMENT"
    )


    root.resizable(
        True,
        True
    )


    # ======================================================
    # POSITION WINDOW TOWARDS TOP
    # ======================================================

    position_window_top(
        root,
        850,
        450
    )


    # ======================================================
    # CLOSE WINDOW
    # ======================================================

    def close_window():

        root.destroy()


        if admin_root.winfo_exists():

            admin_root.deiconify()


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
        pady=10
    )


    # ======================================================
    # USER TABLE
    # ======================================================

    tree = ttk.Treeview(

        table_frame,

        columns=(
            "Username",
            "Role",
            "Status"
        ),

        show="headings"

    )


    # ======================================================
    # TABLE HEADINGS
    # ======================================================

    for col in (
        "Username",
        "Role",
        "Status"
    ):

        tree.heading(
            col,
            text=col
        )


    # ======================================================
    # TABLE COLUMNS
    # ======================================================

    tree.column(
        "Username",
        width=250
    )


    tree.column(
        "Role",
        width=170
    )


    tree.column(
        "Status",
        width=150
    )


    # ======================================================
    # TABLE
    # ======================================================

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )


    # ======================================================
    # SCROLLBAR
    # ======================================================

    scrollbar = ttk.Scrollbar(

        table_frame,

        orient="vertical",

        command=tree.yview

    )


    scrollbar.pack(
        side="right",
        fill="y"
    )


    tree.configure(
        yscrollcommand=scrollbar.set
    )


    # ======================================================
    # LOAD USERS
    # ======================================================

    def load_users():

        for item in tree.get_children():

            tree.delete(item)


        users = get_visible_users(
            current_user
        )


        for user in users:

            status = (

                "Temporary"

                if user["must_change_password"]

                else

                "Changed"

            )


            tree.insert(

                "",

                "end",

                values=(

                    user["username"],

                    user["role"],

                    status

                ),

                tags=(

                    user["user_id"],

                )

            )


    # ======================================================
    # GET SELECTED USER ID
    # ======================================================

    def get_selected_user_id():

        selected = tree.focus()


        if not selected:

            return None


        return int(
            tree.item(
                selected
            )["tags"][0]
        )


    # ======================================================
    # EDIT USER
    # ======================================================

    def edit_selected():

        user_id = get_selected_user_id()


        if not user_id:

            messagebox.showwarning(
                "Warning",
                "Select a user.",
                parent=root
            )

            return


        target_user = get_user_by_id(
            user_id
        )


        if not can_edit_user(
            current_user,
            target_user
        ):

            messagebox.showerror(
                "Denied",
                "You cannot edit this user.",
                parent=root
            )

            return


        open_edit_user_window(
            target_user,
            current_user,
            load_users,
            root
        )


    # ======================================================
    # RESET PASSWORD
    # ======================================================

    def reset_selected_password():

        user_id = get_selected_user_id()


        if not user_id:

            messagebox.showwarning(
                "Warning",
                "Select a user.",
                parent=root
            )

            return


        target_user = get_user_by_id(
            user_id
        )


        if not can_reset_password(
            current_user,
            target_user
        ):

            messagebox.showerror(
                "Denied",
                "You cannot reset this password.",
                parent=root
            )

            return


        open_reset_password_window(
            root,
            current_user,
            target_user,
            load_users
        )


    # ======================================================
    # DELETE USER
    # ======================================================

    def delete_selected():

        user_id = get_selected_user_id()


        if not user_id:

            messagebox.showwarning(
                "Warning",
                "Select a user.",
                parent=root
            )

            return


        target_user = get_user_by_id(
            user_id
        )


        if not can_delete_user(
            current_user,
            target_user
        ):

            messagebox.showerror(
                "Denied",
                "You cannot delete this user.",
                parent=root
            )

            return


        confirm = messagebox.askyesno(
            "Confirm",
            "Delete this user?",
            parent=root
        )


        if confirm:

            try:

                delete_user(
                    current_user,
                    user_id
                )


                load_users()


            except Exception as e:

                messagebox.showerror(
                    "Error",
                    str(e),
                    parent=root
                )


    # ======================================================
    # BUTTON FRAME
    # ======================================================

    btn_frame = tk.Frame(
        root
    )


    btn_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )


    # ======================================================
    # ADD USER
    # ======================================================

    if (

        can_create_user(
            current_user,
            "Cashier"
        )

        or

        can_create_user(
            current_user,
            "Admin"
        )

        or

        can_create_user(
            current_user,
            "Default Admin"
        )

    ):

        tk.Button(

            btn_frame,

            text="Add User",

            width=12,

            bg="#3498db",

            fg="white",

            command=lambda:
            open_add_user_window(
                root,
                current_user,
                load_users
            )

        ).pack(

            side="left",

            padx=5

        )


    # ======================================================
    # EDIT USER BUTTON
    # ======================================================

    tk.Button(

        btn_frame,

        text="Edit User",

        width=12,

        bg="#f39c12",

        fg="white",

        command=edit_selected

    ).pack(

        side="left",

        padx=5

    )


    # ======================================================
    # RESET PASSWORD BUTTON
    # ======================================================

    tk.Button(

        btn_frame,

        text="Reset Password",

        width=14,

        bg="#8e44ad",

        fg="white",

        command=reset_selected_password

    ).pack(

        side="left",

        padx=5

    )


    # ======================================================
    # DELETE USER BUTTON
    # ======================================================

    tk.Button(

        btn_frame,

        text="Delete User",

        width=12,

        bg="#e74c3c",

        fg="white",

        command=delete_selected

    ).pack(

        side="left",

        padx=5

    )


    # ======================================================
    # CLOSE BUTTON
    # ======================================================

    tk.Button(

        btn_frame,

        text="Close",

        width=12,

        bg="#7f8c8d",

        fg="white",

        command=close_window

    ).pack(

        side="right",

        padx=5

    )


    # ======================================================
    # INITIAL LOAD
    # ======================================================

    load_users()


    # ======================================================
    # WINDOW CLOSE EVENT
    # ======================================================

    root.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )

    