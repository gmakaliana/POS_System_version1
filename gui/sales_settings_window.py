import tkinter as tk
from tkinter import messagebox

from modules.settings.settings import (
    get_settings,
    update_sales_settings
)


def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


def open_sales_settings(parent):

    # =====================================
    # HIDE PARENT WINDOW
    # =====================================

    parent.withdraw()

    # =====================================
    # CREATE WINDOW
    # =====================================

    window = tk.Toplevel(parent)

    window.title("SALES SETTINGS")
    window.resizable(False, False)

    center_window(
        window,
        500,
        300
    )

    title_font = ("Arial", 20, "bold")
    label_font = ("Arial", 11)
    entry_font = ("Arial", 11)
    button_font = ("Arial", 11, "bold")

    # =====================================
    # CLOSE FUNCTION
    # =====================================

    def close_window():

        window.destroy()
        parent.deiconify()

    window.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )

    # =====================================
    # GET SETTINGS
    # =====================================

    settings = get_settings()

    try:

        receipt_start = settings["receipt_number_start"]

    except TypeError:

        receipt_start = settings[8]

    # =====================================
    # MAIN FRAME
    # =====================================

    main_frame = tk.Frame(
        window,
        padx=20,
        pady=20
    )

    main_frame.pack(
        fill="both",
        expand=True
    )

    # =====================================
    # TITLE
    # =====================================

    tk.Label(
        main_frame,
        text="SALES SETTINGS",
        font=title_font
    ).pack(
        pady=(0, 25)
    )

    # =====================================
    # FORM FRAME
    # =====================================

    form_frame = tk.Frame(main_frame)

    form_frame.pack()

    tk.Label(
        form_frame,
        text="Receipt Number Start",
        font=label_font
    ).grid(
        row=0,
        column=0,
        sticky="e",
        padx=(0, 10),
        pady=10
    )

    entry = tk.Entry(
        form_frame,
        width=20,
        font=entry_font
    )

    entry.grid(
        row=0,
        column=1,
        ipady=4,
        pady=10
    )

    entry.insert(
        0,
        receipt_start
    )

    # =====================================
    # SAVE FUNCTION
    # =====================================

    def save():

        try:

            number = int(
                entry.get()
            )

            update_sales_settings(
                number
            )

            messagebox.showinfo(
                "Saved",
                "Sales settings saved.",parent=window
            )

        except ValueError:

            messagebox.showerror(
                "Error",
                "Receipt number must be numeric.",parent=window
            )

    # =====================================
    # BUTTONS
    # =====================================

    button_frame = tk.Frame(
        main_frame
    )

    button_frame.pack(
        fill="x",
        pady=30
    )

    tk.Button(
        button_frame,
        text="SAVE",
        width=15,
        height=2,
        bg="#27ae60",
        fg="white",
        font=button_font,
        command=save
    ).pack(
        side="left",
        padx=5
    )

    # Press Enter to save settings
    window.bind(
        "<Return>",
        lambda event: save()
    )

    tk.Button(
        button_frame,
        text="CLOSE",
        width=15,
        height=2,
        bg="#7f8c8d",
        fg="white",
        font=button_font,
        command=close_window
    ).pack(
        side="right",
        padx=5
    )