import tkinter as tk
from tkinter import messagebox

from database.db import get_connection
from auth.password_utils import hash_password
from auth.permissions import is_admin
from gui.admin_dashboard import open_admin_dashboard
from gui.cashier_dashboard import open_cashier_dashboard


def open_change_password(user, parent=None):
    """
    Forces user to change password on first login.
    """

    if parent:
        root = tk.Toplevel(parent)
    else:
        root = tk.Tk()

    root.title("CHANGE PASSWORD")
    root.geometry("300x250")

    root.resizable(False, False)

    tk.Label(root, text="New Password").pack(pady=5)

    new_password_entry = tk.Entry(root, show="*")
    new_password_entry.pack()

    tk.Label(root, text="Confirm Password").pack(pady=5)

    confirm_password_entry = tk.Entry(root, show="*")
    confirm_password_entry.pack()


    # ----------------------------
    # SAVE NEW PASSWORD
    # ----------------------------
    def save_password():

        new_password = new_password_entry.get()
        confirm_password = confirm_password_entry.get()

        if not new_password or not confirm_password:
            messagebox.showerror(
                "Error",
                "All fields required"
            )
            return

        if new_password != confirm_password:
            messagebox.showerror(
                "Error",
                "Passwords do not match"
            )
            return


        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE users
            SET password_hash = ?,
                must_change_password = 0
            WHERE user_id = ?
        """, (
            hash_password(new_password),
            user["user_id"]
        ))

        conn.commit()
        conn.close()


        messagebox.showinfo(
            "Success",
            "Password updated successfully"
        )


        root.destroy()


        # ----------------------------
        # REDIRECT TO DASHBOARD
        # ----------------------------

        if is_admin(user):
            open_admin_dashboard(parent)

        else:
            open_cashier_dashboard(parent)


    tk.Button(
        root,
        text="SAVE PASSWORD",
        command=save_password
    ).pack(pady=15)


    if not parent:
        root.mainloop()