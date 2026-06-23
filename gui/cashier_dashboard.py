import tkinter as tk
from auth.logout import logout_user



def open_cashier_dashboard():

    root = tk.Tk()
    root.title("CASHIER DASHBOARD")
    root.geometry("300x200")

    def logout():
        from gui.login_window import create_login_window
        logout_user()
        root.destroy()
        create_login_window()

    tk.Label(root, text="CASHIER DASHBOARD").pack(pady=10)

    tk.Button(root, text="New Sale", bg="#2ecc71", fg="white", width=20).pack(pady=5)
    tk.Button(root, text="Search Product", bg="#3498db", fg="white", width=20).pack(pady=5)

    tk.Button(
        root,
        text="Logout",
        bg="#e74c3c",
        fg="white",
        width=20,
        command=logout
    ).pack(pady=10)

    root.mainloop()