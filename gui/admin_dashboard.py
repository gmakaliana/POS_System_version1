import tkinter as tk

from auth.logout import logout_user
from gui.login_window import create_login_window
from gui.user_management_window import open_user_management_window


# -----------------------------------
# CENTER WINDOW
# -----------------------------------
def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


def open_admin_dashboard():

    root = tk.Tk()
    root.title("ADMIN DASHBOARD")
    root.resizable(False, False)

    center_window(root, 800, 550)

    # -----------------------------------
    # FONTS
    # -----------------------------------
    title_font = ("Arial", 20, "bold")
    button_font = ("Arial", 11, "bold")

    # -----------------------------------
    # LOGOUT
    # -----------------------------------
    def logout():
        logout_user()
        root.destroy()
        create_login_window()

    # -----------------------------------
    # MAIN FRAME
    # -----------------------------------
    main_frame = tk.Frame(root, padx=20, pady=20)
    main_frame.pack(expand=True)

    # -----------------------------------
    # HEADER
    # -----------------------------------
    tk.Label(
        main_frame,
        text="ADMIN DASHBOARD",
        font=title_font
    ).pack(pady=(0, 25))

    # -----------------------------------
    # BUTTON FRAME
    # -----------------------------------
    btn_frame = tk.Frame(main_frame)
    btn_frame.pack()

    button_width = 18
    button_height = 2

    # Row 1
    tk.Button(
        btn_frame,
        text="Sales",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font
    ).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Products",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font
    ).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Suppliers",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font
    ).grid(row=0, column=2, padx=10, pady=10)

    # Row 2
    tk.Button(
        btn_frame,
        text="Reports",
        width=button_width,
        height=button_height,
        bg="#9b59b6",
        fg="white",
        font=button_font
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
        font=button_font
    ).grid(row=1, column=2, padx=10, pady=10)

    # -----------------------------------
    # LOGOUT BUTTON
    # -----------------------------------
    tk.Button(
        main_frame,
        text="LOGOUT",
        command=logout,
        width=25,
        height=2,
        bg="#e74c3c",
        fg="white",
        font=("Arial", 12, "bold"),
        cursor="hand2"
    ).pack(pady=30)

    root.mainloop()