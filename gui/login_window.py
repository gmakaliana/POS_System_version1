import tkinter as tk
from tkinter import messagebox

from auth.login import authenticate_user
from auth.session import create_session
from auth.permissions import can_access_admin_dashboard

from modules.audit.audit_logs import log_activity

# settings
from modules.settings.settings import get_settings

from modules.system.application_exit import (
    close_application
)


settings = get_settings()

business_name = settings["business_name"]

# settings


def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )


def create_login_window():

    root = tk.Tk()

    root.title("POS LOGIN")

    root.resizable(
        False,
        False
    )

    center_window(
        root,
        500,
        350
    )


    # =====================================
    # FONTS
    # =====================================

    title_font = (
        "Arial",
        18,
        "bold"
    )

    label_font = (
        "Arial",
        12
    )

    entry_font = (
        "Arial",
        12
    )

    button_font = (
        "Arial",
        12,
        "bold"
    )


    # =====================================
    # MAIN FRAME
    # =====================================

    frame = tk.Frame(
        root,
        padx=30,
        pady=20
    )

    frame.pack(
        expand=True
    )


    # =====================================
    # TITLE
    # =====================================

    tk.Label(
        frame,
        text=f"{business_name}\nPOS System",
        font=title_font
    ).pack(
        pady=(0, 25)
    )


    # =====================================
    # USERNAME
    # =====================================

    tk.Label(
        frame,
        text="Username",
        font=label_font
    ).pack(
        anchor="w"
    )


    username_entry = tk.Entry(
        frame,
        font=entry_font,
        width=30
    )

    username_entry.pack(
        ipady=5,
        pady=(5, 15)
    )


    # =====================================
    # PASSWORD
    # =====================================

    tk.Label(
        frame,
        text="Password",
        font=label_font
    ).pack(
        anchor="w"
    )


    password_entry = tk.Entry(
        frame,
        show="*",
        font=entry_font,
        width=30
    )

    password_entry.pack(
        ipady=5,
        pady=(5, 20)
    )


    # =====================================
    # LOGIN
    # =====================================

    def login():

        from gui.admin_dashboard import (
            open_admin_dashboard
        )

        from gui.cashier_dashboard import (
            open_cashier_dashboard
        )

        from gui.change_password import (
            open_change_password
        )


        # =================================
        # AUTHENTICATE USER
        # =================================

        user = authenticate_user(
            username_entry.get(),
            password_entry.get()
        )


        # =================================
        # ACCOUNT INACTIVE
        # =================================

        if user == "inactive":

            messagebox.showerror(
                "Error",
                "Account inactive",
                parent=root
            )

            return


        # =================================
        # INVALID LOGIN
        # =================================

        if not user:

            messagebox.showerror(
                "Error",
                "Invalid credentials",
                parent=root
            )

            return


        # =================================
        # CREATE SESSION
        # =================================

        create_session(
            user
        )


        # =================================
        # AUDIT LOG
        # =================================

        log_activity(
            module="AUTH",
            action="LOGIN",
            description="User logged in"
        )


        # =================================
        # CLEAR LOGIN CREDENTIALS
        # =================================
        #
        # Clear username and password from
        # the login form after successful
        # authentication.
        #
        # =================================

        username_entry.delete(
            0,
            tk.END
        )

        password_entry.delete(
            0,
            tk.END
        )


        # =================================
        # PASSWORD CHANGE REQUIREMENT
        # =================================
        #
        # System Admin must NEVER be forced
        # to change the password after login.
        #
        # Other users with
        # must_change_password = 1 must
        # change their password before
        # accessing the POS.
        #
        # This also protects existing
        # installations where the System
        # Admin may still have
        # must_change_password = 1.
        #
        # =================================

        if (
            user["must_change_password"] == 1
            and user["role"] != "System Admin"
        ):

            open_change_password(
                user,
                root
            )

            return


        # =================================
        # OPEN DASHBOARD
        # =================================

        root.withdraw()


        if can_access_admin_dashboard(
            user
        ):

            open_admin_dashboard(
                root
            )

        else:

            open_cashier_dashboard(
                root
            )


    # =====================================
    # LOGIN BUTTON
    # =====================================

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
    ).pack(
        pady=10
    )


    # =====================================
    # ENTER KEY LOGIN
    # =====================================

    root.bind(
        "<Return>",
        lambda event: login()
    )


    # =====================================
    # FOCUS USERNAME
    # =====================================

    username_entry.focus()


    # =====================================
    # CLOSE LOGIN WINDOW
    # =====================================

    def close_login():

        close_application(
            root
        )


    root.protocol(
        "WM_DELETE_WINDOW",
        close_login
    )


    return root