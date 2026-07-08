import tkinter as tk
from tkinter import messagebox

from auth.logout import logout_user
from auth.session import get_session_user
from gui.login_window import create_login_window
from gui.user_management_window import open_user_management_window
from gui.supplier_management_window import open_supplier_management_window
from gui.product_management_window import open_product_management_window
from gui.report_window import open_reports_dashboard
from gui.settings_window import open_settings_window
from modules.inventory.stock_alerts import show_low_stock_alert

def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


def open_admin_dashboard(parent):

    root = tk.Toplevel(parent)
    root.title("ADMIN DASHBOARD")
    root.resizable(False, False)

    center_window(root, 800, 550)

    title_font = ("Arial", 20, "bold")
    button_font = ("Arial", 11, "bold")

    user = get_session_user()

    if not user:
        messagebox.showerror("Error", "Session expired. Please login again.")
        root.destroy()
        return

    user_id = user["user_id"]

    # safe low stock alert
    root.after(800, show_low_stock_alert)

    # ---------------------------
    # LOGOUT
    # ---------------------------
    def logout():
        logout_user()
        root.destroy()
        
        if parent and parent.winfo_exists():
            parent.deiconify()

    # ---------------------------
    # SALES
    # ---------------------------
    def open_sales():
        from gui.sales_window import open_sales_window
        root.withdraw()   # Hide dashboard
        open_sales_window(user_id=user_id, role="admin",parent=root)

    # ---------------------------
    # REPORTS (FIXED SAFELY)
    # ---------------------------
    def open_reports():
        try:
            if root.winfo_exists():
                open_reports_dashboard(root)
        except tk.TclError:
            # fallback safety (if root already destroyed)
            return

    # ---------------------------
    # WINDOW CLOSE (X BUTTON)
    # ---------------------------
    def close_dashboard():
        logout()


    root.protocol(
        "WM_DELETE_WINDOW",
        close_dashboard
    )


    # ---------------------------
    # UI
    # ---------------------------
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(expand=True)

    tk.Label(
        main_frame,
        text="ADMIN DASHBOARD",
        font=title_font
    ).pack(pady=(0, 25))

    btn_frame = tk.Frame(main_frame)
    btn_frame.pack()

    button_width = 18
    button_height = 2

    tk.Button(
        btn_frame,
        text="Sales",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=open_sales
    ).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Products",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=lambda: open_product_management_window(root)
    ).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Suppliers",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=lambda: open_supplier_management_window(root)
    ).grid(row=0, column=2, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Reports",
        width=button_width,
        height=button_height,
        bg="#9b59b6",
        fg="white",
        font=button_font,
        command=open_reports
    ).grid(row=1, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Users",
        width=button_width,
        height=button_height,
        bg="#16a085",
        fg="white",
        font=button_font,
        command=lambda: open_user_management_window(root)
    ).grid(row=1, column=1, padx=10, pady=10)

    tk.Button(
    btn_frame,
    text="Settings",
    width=button_width,
    height=button_height,
    bg="#34495e",
    fg="white",
    font=button_font,
    command=lambda: open_settings_window(root)
    ).grid(row=1, column=2, padx=10, pady=10)

    tk.Button(
        main_frame,
        text="LOGOUT",
        command=logout,
        width=25,
        height=2,
        bg="#e74c3c",
        fg="white"
    ).pack(pady=30)

    return root