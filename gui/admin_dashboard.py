
"""
GeoMaka POS Admin Dashboard

File:
gui/admin_dashboard.py

Purpose:
Provide the main dashboard interface for
GeoMaka POS administrative users.

Responsibilities:

- Display admin dashboard.
- Display available modules.
- Check UI permissions.
- Open management windows.
- Handle logout process.
- Provide access to Expense Management.

Company:
GeoMaka Technologies
"""

import tkinter as tk
from tkinter import messagebox


# ==========================================================
# AUTHENTICATION
# ==========================================================

from auth.logout import logout_user
from auth.session import get_session_user


# ==========================================================
# PERMISSIONS
# ==========================================================

from auth.permissions import (
    can_access_admin_dashboard,
    can_manage_settings,
    can_view_audit_logs,
    can_manage_expenses
)


# ==========================================================
# GUI WINDOWS
# ==========================================================

from gui.user_management_window import (
    open_user_management_window
)

from gui.supplier_management_window import (
    open_supplier_management_window
)

from gui.product_management_window import (
    open_product_management_window
)

from gui.report_window import (
    open_reports_dashboard
)

from gui.settings_window import (
    open_settings_window
)

from gui.audit_logs_window import (
    open_audit_logs_window
)

from gui.expense_management_window import (
    open_expense_management_window
)


# ==========================================================
# INVENTORY
# ==========================================================

from modules.inventory.stock_alerts import (
    show_low_stock_alert
)


# ==========================================================
# CENTER WINDOW
# ==========================================================

def center_window(
    window,
    width,
    height
):
    """
    Centers a Tkinter window on the screen.
    """

    screen_width = (
        window.winfo_screenwidth()
    )

    screen_height = (
        window.winfo_screenheight()
    )

    x = (
        screen_width // 2
        -
        width // 2
    )

    y = (
        screen_height // 2
        -
        height // 2
    )

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )


# ==========================================================
# OPEN ADMIN DASHBOARD
# ==========================================================

def open_admin_dashboard(parent):
    """
    Opens the Admin Dashboard.

    Only System Admin, Default Admin and Admin
    users are allowed to access this dashboard.
    """

    user = get_session_user()


    # ======================================================
    # SECURITY CHECK
    # ======================================================

    if not user:

        messagebox.showerror(
            "Error",
            "Session expired. Please login again.",
            parent=parent
        )

        return


    if not can_access_admin_dashboard(user):

        messagebox.showerror(
            "Access Denied",
            "You do not have permission to access this dashboard.",
            parent=parent
        )

        return


    # ======================================================
    # CREATE DASHBOARD WINDOW
    # ======================================================

    root = tk.Toplevel(
        parent
    )

    root.title(
        "ADMIN DASHBOARD"
    )

    root.resizable(
        False,
        False
    )


    center_window(
        root,
        800,
        650
    )


    # ======================================================
    # FONTS
    # ======================================================

    title_font = (
        "Arial",
        20,
        "bold"
    )

    button_font = (
        "Arial",
        11,
        "bold"
    )


    # ======================================================
    # CURRENT USER
    # ======================================================

    user_id = user["user_id"]

    role = user["role"]


    # ======================================================
    # LOW STOCK ALERT
    # ======================================================

    root.after(
        800,
        lambda: show_low_stock_alert(root)
    )


    # ======================================================
    # LOGOUT
    # ======================================================

    def logout():

        logout_user()

        root.destroy()


        if (
            parent
            and
            parent.winfo_exists()
        ):

            parent.deiconify()


    # ======================================================
    # SALES
    # ======================================================

    def open_sales():

        from gui.sales_window import (
            open_sales_window
        )

        root.withdraw()

        open_sales_window(
            user_id=user_id,
            role=role,
            parent=root
        )


    # ======================================================
    # REPORTS
    # ======================================================

    def open_reports():

        try:

            if root.winfo_exists():

                open_reports_dashboard(
                    root
                )

        except tk.TclError:

            return


    # ======================================================
    # EXPENSES
    # ======================================================

    def open_expenses():

        try:

            if root.winfo_exists():

                open_expense_management_window(
                    root
                )

        except tk.TclError:

            return


    # ======================================================
    # CLOSE WINDOW
    # ======================================================

    root.protocol(
        "WM_DELETE_WINDOW",
        logout
    )


    # ======================================================
    # MAIN FRAME
    # ======================================================

    main_frame = tk.Frame(
        root,
        padx=20,
        pady=20
    )

    main_frame.pack(
        expand=True
    )


    # ======================================================
    # TITLE
    # ======================================================

    tk.Label(
        main_frame,
        text=f"ADMIN DASHBOARD\n({role})",
        font=title_font
    ).pack(
        pady=(0, 25)
    )


    # ======================================================
    # BUTTON FRAME
    # ======================================================

    btn_frame = tk.Frame(
        main_frame
    )

    btn_frame.pack()


    button_width = 18

    button_height = 2


    # ======================================================
    # SALES
    # ======================================================

    tk.Button(
        btn_frame,
        text="Sales",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=open_sales
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )


    # ======================================================
    # PRODUCTS
    # ======================================================

    tk.Button(
        btn_frame,
        text="Products",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=lambda:
            open_product_management_window(root)
    ).grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )


    # ======================================================
    # SUPPLIERS
    # ======================================================

    tk.Button(
        btn_frame,
        text="Suppliers",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=lambda:
            open_supplier_management_window(root)
    ).grid(
        row=0,
        column=2,
        padx=10,
        pady=10
    )


    # ======================================================
    # REPORTS
    # ======================================================

    tk.Button(
        btn_frame,
        text="Reports",
        width=button_width,
        height=button_height,
        bg="#9b59b6",
        fg="white",
        font=button_font,
        command=open_reports
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )


    # ======================================================
    # USERS
    # ======================================================

    tk.Button(
        btn_frame,
        text="Users",
        width=button_width,
        height=button_height,
        bg="#16a085",
        fg="white",
        font=button_font,
        command=lambda:
            open_user_management_window(root)
    ).grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )


    # ======================================================
    # EXPENSES
    #
    # System Admin:
    #     Access
    #
    # Default Admin:
    #     Access
    #
    # Admin:
    #     Access
    #
    # Cashier:
    #     No Admin Dashboard access
    #
    # Therefore the permission check is still performed
    # explicitly here.
    # ======================================================

    if can_manage_expenses(user):

        tk.Button(
            btn_frame,
            text="Expenses",
            width=button_width,
            height=button_height,
            bg="#e67e22",
            fg="white",
            font=button_font,
            command=open_expenses
        ).grid(
            row=1,
            column=2,
            padx=10,
            pady=10
        )


    # ======================================================
    # SETTINGS
    # ======================================================

    if can_manage_settings(user):

        tk.Button(
            btn_frame,
            text="Settings",
            width=button_width,
            height=button_height,
            bg="#34495e",
            fg="white",
            font=button_font,
            command=lambda:
                open_settings_window(root)
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )


    # ======================================================
    # AUDIT LOGS
    # ======================================================

    if can_view_audit_logs(user):

        tk.Button(
            btn_frame,
            text="Audit Logs",
            width=button_width,
            height=button_height,
            bg="#8e44ad",
            fg="white",
            font=button_font,
            command=lambda:
                open_audit_logs_window(root)
        ).grid(
            row=2,
            column=1,
            padx=10,
            pady=10
        )


    # ======================================================
    # LOGOUT BUTTON
    # ======================================================

    tk.Button(
        main_frame,
        text="LOGOUT",
        command=logout,
        width=25,
        height=2,
        bg="#e74c3c",
        fg="white"
    ).pack(
        pady=30
    )


    # ======================================================
    # RETURN DASHBOARD WINDOW
    # ======================================================

    return root

