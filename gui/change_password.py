import tkinter as tk
from tkinter import messagebox

from database.db import get_connection
from auth.password_utils import hash_password
from auth.permissions import is_admin
from gui.admin_dashboard import open_admin_dashboard
from gui.cashier_dashboard import open_cashier_dashboard


def open_change_password(user, parent):
    """
    Forces user to change password on first login.
    """

    root = tk.Toplevel(parent)

    root.title("CHANGE PASSWORD")
    root.geometry("300x250")
    root.resizable(False, False)

    # Keep window on top
    root.transient(parent)
    root.grab_set()

    # Prevent closing window before password change
    def prevent_close():
        messagebox.showwarning(
            "Password Change Required",
            "You must change your password before continuing.",
            parent=root
        )


    root.protocol(
        "WM_DELETE_WINDOW",
        prevent_close
    )


    tk.Label(
        root,
        text="New Password"
    ).pack(pady=5)

    new_password_entry = tk.Entry(
        root,
        show="*"
    )
    new_password_entry.pack()


    tk.Label(
        root,
        text="Confirm Password"
    ).pack(pady=5)

    confirm_password_entry = tk.Entry(
        root,
        show="*"
    )
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
                "All fields required",
                parent=root
            )
            return


        if new_password != confirm_password:
            messagebox.showerror(
                "Error",
                "Passwords do not match",
                parent=root
            )
            return


        try:
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
                "Password updated successfully",
                parent=root
            )


            # Close change password window
            root.destroy()

            # Close login window
            #if parent:
            #hide login window
            parent.withdraw()

            # ----------------------------
            # OPEN DASHBOARD
            # ----------------------------

            if is_admin(user):
                open_admin_dashboard(parent)

            else:
                open_cashier_dashboard(parent)


        except Exception as e:

            messagebox.showerror(
                "Database Error",
                str(e),
                parent=root
            )



    tk.Button(
        root,
        text="SAVE PASSWORD",
        command=save_password
    ).pack(pady=15)

    # Press Enter to save password
    root.bind(
        "<Return>",
        lambda event: save_password()
    )

    # Focus first field
    new_password_entry.focus()

    root.bind(
        "<Return>",
        lambda event: save_password()
    )