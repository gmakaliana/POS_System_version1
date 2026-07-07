import tkinter as tk
from tkinter import ttk, messagebox

from modules.settings.settings import (
    get_settings,
    update_sales_settings
)



def open_sales_settings(parent):

    # =====================================
    # HIDE PARENT WINDOW
    # =====================================

    parent.withdraw()



    # =====================================
    # CREATE WINDOW
    # =====================================

    window = tk.Toplevel()

    window.title("Sales Settings")

    window.geometry("400x250")

    window.resizable(False, False)



    # =====================================
    # CLOSE FUNCTION
    # =====================================

    def close_window():

        window.destroy()

        parent.deiconify()



    # =====================================
    # GET SETTINGS
    # =====================================

    settings = get_settings()


    try:

        receipt_start = settings["receipt_number_start"]


    except TypeError:

        receipt_start = settings[8]



    # =====================================
    # TITLE
    # =====================================

    ttk.Label(
        window,
        text="SALES SETTINGS",
        font=("Arial", 16, "bold")
    ).pack(
        pady=20
    )



    # =====================================
    # FORM FRAME
    # =====================================

    frame = ttk.Frame(window)

    frame.pack()



    ttk.Label(
        frame,
        text="Receipt Number Start"
    ).grid(
        row=0,
        column=0,
        pady=15
    )



    entry = ttk.Entry(
        frame,
        width=20
    )

    entry.grid(
        row=0,
        column=1,
        padx=10
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
                "Sales settings saved."
            )



        except ValueError:

            messagebox.showerror(
                "Error",
                "Receipt number must be numeric."
            )



    # =====================================
    # BUTTONS
    # =====================================

    button_frame = ttk.Frame(
        window
    )

    button_frame.pack(
        pady=30
    )



    ttk.Button(
        button_frame,
        text="Save",
        width=15,
        command=save
    ).grid(
        row=0,
        column=0,
        padx=15
    )



    ttk.Button(
        button_frame,
        text="Close",
        width=15,
        command=close_window
    ).grid(
        row=0,
        column=1,
        padx=15
    )



    # =====================================
    # WINDOW CONTROL
    # =====================================

    # Handle X button
    window.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )