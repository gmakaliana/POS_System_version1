import tkinter as tk
from auth.logout import logout_user
from gui.login_window import create_login_window
from gui.user_management_window import open_user_management_window


def open_admin_dashboard():

    root = tk.Tk()
    root.title("ADMIN DASHBOARD")
    root.geometry("500x350")

    # -----------------------------------
    # LOGOUT
    # -----------------------------------
    def logout():
        logout_user()
        root.destroy()
        create_login_window()

    # -----------------------------------
    # UI HEADER
    # -----------------------------------
    tk.Label(root, text="ADMIN DASHBOARD",
             font=("Arial", 14, "bold")).pack(pady=10)

    # -----------------------------------
    # MENU BUTTONS
    # -----------------------------------
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Sales", width=12, bg="#2980b9", fg="white").grid(row=0, column=0, padx=5, pady=5)
    tk.Button(btn_frame, text="Products", width=12, bg="#2980b9", fg="white").grid(row=0, column=1, padx=5, pady=5)
    tk.Button(btn_frame, text="Suppliers", width=12, bg="#2980b9", fg="white").grid(row=0, column=2, padx=5, pady=5)

    tk.Button(btn_frame, text="Reports", width=12, bg="#8e44ad", fg="white").grid(row=1, column=0, padx=5, pady=5)

    tk.Button(btn_frame, text="Users", width=12, bg="#16a085", fg="white",
            command=lambda: open_user_management_window(root)).grid(row=1, column=1, padx=5, pady=5)

    tk.Button(btn_frame, text="Settings", width=12, bg="#34495e", fg="white").grid(row=1, column=2, padx=5, pady=5)

    tk.Button(
        root,
        text="LOGOUT",
        width=20,
        command=logout,
        bg="#e74c3c",
        fg="white",
        font=("Arial", 10, "bold")
    ).pack(pady=15)

    root.mainloop()