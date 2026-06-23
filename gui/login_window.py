import tkinter as tk
from tkinter import messagebox

from auth.login import authenticate_user
from auth.session import create_session
from auth.permissions import is_admin




def create_login_window():

    root = tk.Tk()
    root.title("POS LOGIN")
    root.geometry("350x250")

    tk.Label(root, text="Username").pack()
    username_entry = tk.Entry(root)
    username_entry.pack()

    tk.Label(root, text="Password").pack()
    password_entry = tk.Entry(root, show="*")
    password_entry.pack()

    def login():

        from gui.admin_dashboard import open_admin_dashboard
        from gui.cashier_dashboard import open_cashier_dashboard
        from gui.change_password import open_change_password

        user = authenticate_user(username_entry.get(), password_entry.get())

        if user == "inactive":
            messagebox.showerror("Error", "Account inactive")
            return

        if not user:
            messagebox.showerror("Error", "Invalid credentials")
            return

        create_session(user)

        if user["must_change_password"] == 1:
            root.destroy()
            open_change_password(user)
            return

        root.destroy()

        if is_admin(user):
            open_admin_dashboard()
        else:
            open_cashier_dashboard()

    tk.Button(
    root,
    text="LOGIN",
    command=login,
    bg="#2ecc71",     # green
    fg="white",
    width=20,
    font=("Arial", 10, "bold")
).pack(pady=20)

    root.mainloop()