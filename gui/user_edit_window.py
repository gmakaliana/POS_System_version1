# gui/user_edit_window.py

import tkinter as tk
from tkinter import messagebox, ttk

from modules.users.user_management import update_user
from auth.permissions import can_change_role



def open_edit_user_window(
        user_data,
        current_user,
        refresh_callback,
        parent
):


    target_user = user_data



    # =====================================
    # PROTECT SYSTEM ADMIN
    # =====================================

    if target_user["role"] == "System Admin":

        messagebox.showerror(
            "Restricted",
            "System Admin account cannot be edited.",
            parent=parent
        )

        return



    win = tk.Toplevel(parent)

    win.title(
        "EDIT USER"
    )

    win.geometry(
        "320x250"
    )

    win.resizable(
        False,
        False
    )


    win.transient(parent)

    win.grab_set()



    # =====================================
    # USERNAME
    # =====================================

    tk.Label(
        win,
        text="Username"
    ).pack(
        pady=5
    )


    username_entry = tk.Entry(
        win
    )

    username_entry.pack()


    username_entry.insert(
        0,
        target_user["username"]
    )


    username_entry.focus()



    # =====================================
    # ROLE
    # =====================================

    tk.Label(
        win,
        text="Role"
    ).pack(
        pady=5
    )


    role_var = tk.StringVar(
        value=target_user["role"]
    )



    allowed_roles = [
        target_user["role"]
    ]



    possible_roles = [
        "Default Admin",
        "Admin",
        "Cashier"
    ]



    for role in possible_roles:


        if role == target_user["role"]:

            continue



        if can_change_role(
            current_user,
            target_user,
            role
        ):

            allowed_roles.append(
                role
            )



    role_box = ttk.Combobox(
        win,
        textvariable=role_var,
        values=allowed_roles,
        state="readonly"
    )


    role_box.pack()



    # =====================================
    # SAVE
    # =====================================

    def save():


        username = username_entry.get().strip()

        role = role_var.get()



        if not username:

            messagebox.showerror(
                "Error",
                "Username is required.",
                parent=win
            )

            return



        try:


            update_user(

                current_user,

                target_user["user_id"],

                username,

                role

            )



            messagebox.showinfo(
                "Success",
                "User updated successfully.",
                parent=win
            )



            win.destroy()



            refresh_callback()



        except Exception as e:


            messagebox.showerror(
                "Error",
                str(e),
                parent=win
            )



    # =====================================
    # BUTTONS
    # =====================================

    button_frame = tk.Frame(win)

    button_frame.pack(
        pady=15
    )



    tk.Button(
        button_frame,
        text="Save",
        width=12,
        bg="#3498db",
        fg="white",
        command=save
    ).pack(
        side="left",
        padx=5
    )



    tk.Button(
        button_frame,
        text="Close",
        width=12,
        bg="#7f8c8d",
        fg="white",
        command=win.destroy
    ).pack(
        side="left",
        padx=5
    )



    win.bind(
        "<Return>",
        lambda event: save()
    )