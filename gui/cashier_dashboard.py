import tkinter as tk

from auth.logout import logout_user


# -----------------------------------
# CENTER WINDOW
# -----------------------------------
def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


def open_cashier_dashboard():

    root = tk.Tk()
    root.title("CASHIER DASHBOARD")
    root.resizable(False, False)

    center_window(root, 700, 500)

    # -----------------------------------
    # FONTS
    # -----------------------------------
    title_font = ("Arial", 20, "bold")
    button_font = ("Arial", 11, "bold")

    # -----------------------------------
    # LOGOUT
    # -----------------------------------
    def logout():
        from gui.login_window import create_login_window

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
        text="CASHIER DASHBOARD",
        font=title_font
    ).pack(pady=(0, 30))

    # -----------------------------------
    # BUTTON FRAME
    # -----------------------------------
    button_frame = tk.Frame(main_frame)
    button_frame.pack()

    # -----------------------------------
    # NEW SALE BUTTON
    # -----------------------------------
    tk.Button(
        button_frame,
        text="NEW SALE",
        bg="#2ecc71",
        fg="white",
        width=22,
        height=2,
        font=button_font,
        cursor="hand2"
    ).pack(pady=10)

    # -----------------------------------
    # SEARCH PRODUCT BUTTON
    # -----------------------------------
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

    # -----------------------------------
    # LOGOUT BUTTON
    # -----------------------------------
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

    root.mainloop()