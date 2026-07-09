import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from modules.settings.settings import (
    get_settings,
    update_business_information
)

def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


def open_business_settings(parent):

    # =====================================
    # HIDE PARENT WINDOW
    # =====================================

    parent.withdraw()



    # =====================================
    # CREATE WINDOW
    # =====================================

    window = tk.Toplevel()

    window.title("Business Information")

    window.resizable(True, True)

    center_window(
        window,
        650,
        650
    )

    # =====================================
    # CLOSE FUNCTION
    # =====================================

    def close_window():

        window.destroy()

        parent.deiconify()



    # =====================================
    # LOAD SETTINGS
    # =====================================

    settings = get_settings()


    try:

        business_name = settings["business_name"]
        business_address = settings["business_address"]
        business_phone = settings["business_phone"]
        business_email = settings["business_email"]
        receipt_header = settings["receipt_header"]
        receipt_footer = settings["receipt_footer"]


    except TypeError:

        business_name = settings[1]
        business_address = settings[2]
        business_phone = settings[3]
        business_email = settings[4]
        receipt_header = settings[6]
        receipt_footer = settings[7]



   



    # =====================================
    # TITLE
    # =====================================

    ttk.Label(
        window,
        text="BUSINESS INFORMATION",
        font=("Arial", 16, "bold")
    ).pack(
        pady=15
    )



    frame = ttk.Frame(
        window
    )

    frame.pack(
        padx=30,
        pady=10
    )



    fields = {}



    def add_field(label, value, row):

        ttk.Label(
            frame,
            text=label
        ).grid(
            row=row,
            column=0,
            sticky="w",
            pady=8
        )


        entry = ttk.Entry(
            frame,
            width=40
        )

        entry.grid(
            row=row,
            column=1,
            padx=10
        )


        entry.insert(
            0,
            value or ""
        )


        fields[label] = entry



    add_field(
        "Business Name",
        business_name,
        0
    )


    add_field(
        "Business Address",
        business_address,
        1
    )


    add_field(
        "Business Phone",
        business_phone,
        2
    )


    add_field(
        "Business Email",
        business_email,
        3
    )


    # =====================================
    # RECEIPT HEADER
    # =====================================

    ttk.Label(
        frame,
        text="Receipt Header"
    ).grid(
        row=6,
        column=0,
        sticky="nw"
    )



    header_box = tk.Text(
        frame,
        width=40,
        height=4
    )

    header_box.grid(
        row=6,
        column=1
    )


    header_box.insert(
        "1.0",
        receipt_header or ""
    )



    # =====================================
    # RECEIPT FOOTER
    # =====================================

    ttk.Label(
        frame,
        text="Receipt Footer"
    ).grid(
        row=7,
        column=0,
        sticky="nw"
    )


    footer_box = tk.Text(
        frame,
        width=40,
        height=4
    )

    footer_box.grid(
        row=7,
        column=1
    )


    footer_box.insert(
        "1.0",
        receipt_footer or ""
    )



    # =====================================
    # SAVE FUNCTION
    # =====================================

    def save():

        update_business_information(

            fields["Business Name"].get(),

            fields["Business Address"].get(),

            fields["Business Phone"].get(),

            fields["Business Email"].get(),

            header_box.get(
                "1.0",
                "end"
            ).strip(),

            footer_box.get(
                "1.0",
                "end"
            ).strip()

        )


        messagebox.showinfo(
            "Saved",
            "Business information saved."
        )



    # =====================================
    # BUTTONS
    # =====================================

    button_frame = ttk.Frame(
        window
    )

    button_frame.pack(
        pady=25
    )



    ttk.Button(
        button_frame,
        text="Save",
        width=15,
        command=save
    ).grid(
        row=0,
        column=0,
        padx=20
    )



    ttk.Button(
        button_frame,
        text="Close",
        width=15,
        command=close_window
    ).grid(
        row=0,
        column=1,
        padx=20
    )



    # =====================================
    # WINDOW CONTROL
    # =====================================

    # Handle X button
    window.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )