import tkinter as tk
from tkinter import messagebox

from modules.users.user_management import add_user


def open_add_user_window(refresh_callback=None):

    win = tk.Toplevel()
    win.title("ADD USER")
    win.geometry("300x250")

    tk.Label(win, text="Username").pack()
    username_entry = tk.Entry(win)
    username_entry.pack()

    tk.Label(win, text="Password").pack()
    password_entry = tk.Entry(win, show="*")
    password_entry.pack()

    role_var = tk.StringVar(value="Cashier")

    tk.Label(win, text="Role").pack()
    tk.Radiobutton(win, text="Admin", variable=role_var, value="Admin").pack()
    tk.Radiobutton(win, text="Cashier", variable=role_var, value="Cashier").pack()

    def save():
        username = username_entry.get()
        password = password_entry.get()
        role = role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "All fields required")
            return

        add_user(username, password, role)

        messagebox.showinfo("Success", "User added successfully")

        win.destroy()

        if refresh_callback:
            refresh_callback()

    tk.Button(win, text="Add User", command=save).pack(pady=10)