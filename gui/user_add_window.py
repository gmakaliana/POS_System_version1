# gui/user_add_window.py

import tkinter as tk
from tkinter import messagebox
from modules.users.user_management import add_user
from auth.permissions import can_create_user
from auth.password_policy import validate_password
from utils.validation import validate_username

def open_add_user_window(
        parent,
        current_user,
        refresh_callback=None
):

    win = tk.Toplevel(parent)

    win.transient(parent)
    win.grab_set()

    win.title("ADD USER")
    win.geometry("320x320")
    win.resizable(False, False)



    # =====================================
    # CHECK AVAILABLE ROLES
    # =====================================

    available_roles = []


    possible_roles = [
        "System Admin",
        "Default Admin",
        "Admin",
        "Cashier"
    ]


    for role in possible_roles:

        if can_create_user(
            current_user,
            role
        ):

            available_roles.append(role)



    if not available_roles:

        messagebox.showerror(
            "Permission Denied",
            "You cannot create users.",
            parent=win
        )

        win.destroy()
        return



    # =====================================
    # USERNAME
    # =====================================

    tk.Label(
        win,
        text="Username"
    ).pack(pady=5)


    username_entry = tk.Entry(win)

    username_entry.pack()

    username_entry.focus()



    # =====================================
    # TEMP PASSWORD
    # =====================================

    tk.Label(
        win,
        text="Temporary Password"
    ).pack(pady=5)


    password_entry = tk.Entry(
        win,
        show="*"
    )

    password_entry.pack()



    # =====================================
    # ROLE
    # =====================================

    tk.Label(
        win,
        text="Role"
    ).pack(pady=5)



    role_var = tk.StringVar(
        value=available_roles[0]
    )



    for role in available_roles:

        tk.Radiobutton(
            win,
            text=role,
            variable=role_var,
            value=role
        ).pack()



    # =====================================
    # SAVE
    # =====================================

    def save():

        username = username_entry.get().strip()

        password = password_entry.get().strip()

        role = role_var.get()



        # =============================
        # USERNAME VALIDATION
        # =============================

        valid, message = validate_username(
            username
        )


        if not valid:

            messagebox.showerror(
                "Invalid Username",
                message,
                parent=win
            )

            return



        if not password:

            messagebox.showerror(
                "Error",
                "Password is required.",
                parent=win
            )

            return

        # PASSWORD POLICY
        valid, message = validate_password(
            password
        )


        if not valid:

            messagebox.showerror(
                "Weak Password",
                message,
                parent=win
            )

            return



        try:

            add_user(
                current_user,
                username,
                password,
                role
            )


            messagebox.showinfo(
                "Success",
                "User added successfully.",
                parent=win
            )


            win.destroy()


            if refresh_callback:

                refresh_callback()



        except Exception as e:

            messagebox.showerror(
                "Error",
                str(e),
                parent=win
            )



    # =====================================
    # BUTTON
    # =====================================

    tk.Button(
        win,
        text="Add User",
        bg="#3498db",
        fg="white",
        width=15,
        command=save
    ).pack(
        pady=15
    )



    # ENTER = SAVE

    win.bind(
        "<Return>",
        lambda event: save()
    )