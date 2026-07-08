import tkinter as tk
from tkinter import messagebox

from auth.logout import logout_user
from auth.session import get_session_user


# -----------------------------------
# CENTER WINDOW
# -----------------------------------
def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


def open_cashier_dashboard(parent):

    root = tk.Toplevel(parent)
    root.title("CASHIER DASHBOARD")
    root.resizable(False, False)

    center_window(root, 700, 500)

    title_font = ("Arial", 20, "bold")
    button_font = ("Arial", 11, "bold")

    # -----------------------------------
    # GET SESSION USER
    # -----------------------------------
    user = get_session_user()

    if not user:
        messagebox.showerror("Error", "Session expired. Please login again.")
        root.destroy()
        return

    user_id = user["user_id"]

    # -----------------------------------
    # LOGOUT
    # -----------------------------------
    def logout():
        from gui.login_window import create_login_window
        logout_user()
        root.destroy()
        
        if parent and parent.winfo_exists():
            parent.deiconify()

    # -----------------------------------
    # OPEN SALES WINDOW
    # -----------------------------------
    def open_new_sale():

        from gui.sales_window import open_sales_window
        root.withdraw()   # Hide dashboard
        open_sales_window(user_id=user_id, role="cashier",parent=root)

    # ---------------------------
    # WINDOW CLOSE (X BUTTON)
    # ---------------------------
    def close_dashboard():
        logout()


    root.protocol(
        "WM_DELETE_WINDOW",
        close_dashboard
    )

    # -----------------------------------
    # UI
    # -----------------------------------
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(expand=True)

    tk.Label(
        main_frame,
        text="CASHIER DASHBOARD",
        font=title_font
    ).pack(pady=(0, 30))

    button_frame = tk.Frame(main_frame)
    button_frame.pack()

    tk.Button(
        button_frame,
        text="NEW SALE",
        bg="#2ecc71",
        fg="white",
        width=22,
        height=2,
        font=button_font,
        cursor="hand2",
        command=open_new_sale
    ).pack(pady=10)

    tk.Button(
        button_frame,
        text="SEARCH PRODUCT",
        bg="#3498db",
        fg="white",
        width=22,
        height=2,
        font=button_font,
        cursor="hand2"
    ).pack(pady=10)

    tk.Button(
        main_frame,
        text="LOGOUT",
        bg="#e74c3c",
        fg="white",
        width=22,
        height=2,
        font=("Arial", 12, "bold"),
        cursor="hand2",
        command=logout
    ).pack(pady=30)

    return root