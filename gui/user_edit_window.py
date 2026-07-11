import tkinter as tk
from tkinter import messagebox

from modules.users.user_management import update_user


def open_edit_user_window(user_data, refresh_callback):

    user_id, username, role, _ = user_data

    win = tk.Toplevel()
    win.title("EDIT USER")
    win.geometry("300x250")

    tk.Label(win, text="Username").pack()
    username_entry = tk.Entry(win)
    username_entry.pack()
    username_entry.insert(0, username)

    # Focus username automatically
    username_entry.focus()

    role_var = tk.StringVar(value=role)

    tk.Label(win, text="Role").pack()

    tk.Radiobutton(win, text="Admin", variable=role_var, value="Admin").pack()
    tk.Radiobutton(win, text="Cashier", variable=role_var, value="Cashier").pack()

    def save():
        update_user(user_id, username_entry.get(), role_var.get())
        messagebox.showinfo("Success", "Updated successfully",parent=win)
        win.destroy()
        refresh_callback()

    tk.Button(win, text="Save", command=save).pack(pady=10)