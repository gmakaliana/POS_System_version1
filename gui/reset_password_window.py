# gui/reset_password_window.py

import tkinter as tk
from tkinter import messagebox

from modules.users.user_management import reset_password



def open_reset_password_window(
        parent,
        current_user,
        target_user,
        refresh_callback=None
):

    win = tk.Toplevel(parent)

    win.title("RESET PASSWORD")

    win.geometry(
        "320x270"
    )

    win.resizable(
        False,
        False
    )


    win.transient(parent)

    win.grab_set()



    # =====================================
    # USER INFORMATION
    # =====================================

    tk.Label(
        win,
        text=f"Reset password for: {target_user['username']}",
        font=("Arial", 10, "bold")
    ).pack(
        pady=10
    )



    # =====================================
    # NEW PASSWORD
    # =====================================

    tk.Label(
        win,
        text="New Password"
    ).pack()


    password_entry = tk.Entry(
        win,
        show="*"
    )

    password_entry.pack()



    password_entry.focus()



    # =====================================
    # CONFIRM PASSWORD
    # =====================================

    tk.Label(
        win,
        text="Confirm Password"
    ).pack(
        pady=(10, 0)
    )


    confirm_entry = tk.Entry(
        win,
        show="*"
    )

    confirm_entry.pack()



    # =====================================
    # RESET PASSWORD
    # =====================================

    def reset():

        new_password = password_entry.get().strip()

        confirm_password = confirm_entry.get().strip()



        if not new_password or not confirm_password:

            messagebox.showerror(
                "Error",
                "All fields are required.",
                parent=win
            )

            return



        # PASSWORD POLICY

        if len(new_password) < 8:

            messagebox.showerror(
                "Weak Password",
                "Password must be at least 8 characters long.",
                parent=win
            )

            return



        if new_password != confirm_password:

            messagebox.showerror(
                "Error",
                "Passwords do not match.",
                parent=win
            )

            return



        try:

            reset_password(
                current_user,
                target_user["user_id"],
                new_password
            )



            messagebox.showinfo(
                "Success",
                "Password reset successfully.\n\n"
                "User must change password on next login.",
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
    # BUTTONS
    # =====================================

    tk.Button(
        win,
        text="Reset Password",
        width=18,
        bg="#8e44ad",
        fg="white",
        command=reset
    ).pack(
        pady=15
    )



    tk.Button(
        win,
        text="Close",
        width=18,
        bg="#7f8c8d",
        fg="white",
        command=win.destroy
    ).pack()



    # =====================================
    # ENTER KEY
    # =====================================

    win.bind(
        "<Return>",
        lambda event: reset()
    )


    return win