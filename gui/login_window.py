import tkinter as tk
from tkinter import messagebox

from auth.login import authenticate_user
from auth.session import create_session
from auth.permissions import is_admin

#settings
from modules.settings.settings import get_settings


settings = get_settings()

business_name = settings["business_name"]

#settings

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


def create_login_window():

    root = tk.Tk()
    root.title("POS LOGIN")
    root.resizable(False, False)

    center_window(root, 500, 350)

    # Fonts
    title_font = ("Arial", 18, "bold")
    label_font = ("Arial", 12)
    entry_font = ("Arial", 12)
    button_font = ("Arial", 12, "bold")

    # Main Frame
    frame = tk.Frame(root, padx=30, pady=20)
    frame.pack(expand=True)

    # Title
    tk.Label(
        frame,
        text=f"{business_name}\nPOS System", #business name
        font=title_font
    ).pack(pady=(0, 25))

    # Username
    tk.Label(
        frame,
        text="Username",
        font=label_font
    ).pack(anchor="w")

    username_entry = tk.Entry(
        frame,
        font=entry_font,
        width=30
    )
    username_entry.pack(ipady=5, pady=(5, 15))

    # Password
    tk.Label(
        frame,
        text="Password",
        font=label_font
    ).pack(anchor="w")

    password_entry = tk.Entry(
        frame,
        show="*",
        font=entry_font,
        width=30
    )
    password_entry.pack(ipady=5, pady=(5, 20))

    def login():

        from gui.admin_dashboard import open_admin_dashboard
        from gui.cashier_dashboard import open_cashier_dashboard
        from gui.change_password import open_change_password

        user = authenticate_user(
            username_entry.get(),
            password_entry.get()
        )

        if user == "inactive":
            messagebox.showerror(
                "Error",
                "Account inactive"
            )
            return

        if not user:
            messagebox.showerror(
                "Error",
                "Invalid credentials"
            )
            return

        create_session(user)

        # Clear login credentials for security
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)

        if user["must_change_password"] == 1:
            root.destroy()
            open_change_password(user)
            return

        root.withdraw()

        if is_admin(user):
            open_admin_dashboard(root)
        else:
            open_cashier_dashboard(root)

    # Login Button
    tk.Button(
        frame,
        text="LOGIN",
        command=login,
        bg="#2ecc71",
        fg="white",
        font=button_font,
        width=20,
        height=2,
        cursor="hand2"
    ).pack(pady=10)

    # Enter key login
    root.bind("<Return>", lambda event: login())

    # Focus username automatically
    username_entry.focus()

    def close_login():
        root.destroy()

    root.protocol(
        "WM_DELETE_WINDOW",
        close_login
    )

    return root    