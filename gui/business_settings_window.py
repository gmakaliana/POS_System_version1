import tkinter as tk
from tkinter import messagebox

from modules.settings.settings import (
    get_settings,
    update_business_information
)

from utils.validation import (
    validate_business_name,
    validate_address,
    validate_phone,
    validate_email,
    validate_receipt_text
)

def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


def open_business_settings(parent):

    # =====================================
    # HIDE PARENT
    # =====================================

    parent.withdraw()

    # =====================================
    # CREATE WINDOW
    # =====================================

    window = tk.Toplevel(parent)

    window.title("BUSINESS INFORMATION")
    window.resizable(False, False)

    center_window(
        window,
        800,
        650
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
    # MAIN FRAME
    # =====================================

    main_frame = tk.Frame(
        window,
        padx=20,
        pady=20
    )

    main_frame.pack(fill="both", expand=True)

    # =====================================
    # TITLE
    # =====================================

    tk.Label(
        main_frame,
        text="BUSINESS INFORMATION",
        font=title_font
    ).pack(
        pady=(0, 20)
    )

    # =====================================
    # FORM FRAME
    # =====================================

    form_frame = tk.Frame(main_frame)
    form_frame.pack()

    fields = {}

    def add_field(label, value, row):

        tk.Label(
            form_frame,
            text=label,
            font=label_font
        ).grid(
            row=row,
            column=0,
            sticky="e",
            padx=(0, 10),
            pady=8
        )

        entry = tk.Entry(
            form_frame,
            width=40,
            font=entry_font
        )

        entry.grid(
            row=row,
            column=1,
            pady=8,
            ipady=4
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
    # RECEIPT SETTINGS
    # =====================================

    tk.Label(
        form_frame,
        text="Receipt Settings",
        font=("Arial", 11, "bold")
    ).grid(
        row=4,
        column=0,
        columnspan=2,
        sticky="w",
        pady=(20, 10)
    )

    tk.Label(
        form_frame,
        text="Receipt Header",
        font=label_font
    ).grid(
        row=5,
        column=0,
        sticky="ne",
        padx=(0, 10),
        pady=5
    )

    header_box = tk.Text(
        form_frame,
        width=40,
        height=4,
        font=entry_font
    )

    header_box.grid(
        row=5,
        column=1,
        pady=5
    )

    header_box.insert(
        "1.0",
        receipt_header or ""
    )

    tk.Label(
        form_frame,
        text="Receipt Footer",
        font=label_font
    ).grid(
        row=6,
        column=0,
        sticky="ne",
        padx=(0, 10),
        pady=5
    )

    footer_box = tk.Text(
        form_frame,
        width=40,
        height=4,
        font=entry_font
    )

    footer_box.grid(
        row=6,
        column=1,
        pady=5
    )

    footer_box.insert(
        "1.0",
        receipt_footer or ""
    )

    # =====================================
    # SAVE
    # =====================================

    def save():


        business_name = fields["Business Name"].get().strip()

        business_address = fields["Business Address"].get().strip()

        business_phone = fields["Business Phone"].get().strip()

        business_email = fields["Business Email"].get().strip()


        receipt_header_value = header_box.get(
            "1.0",
            "end"
        ).strip()


        receipt_footer_value = footer_box.get(
            "1.0",
            "end"
        ).strip()



        checks = [

            validate_business_name(
                business_name
            ),

            validate_address(
                business_address
            ),

            validate_phone(
                business_phone
            ),

            validate_email(
                business_email
            ),

            validate_receipt_text(
                receipt_header_value
            ),

            validate_receipt_text(
                receipt_footer_value
            )

        ]



        for valid, message in checks:

            if not valid:

                messagebox.showerror(
                    "Invalid Input",
                    message,
                    parent=window
                )

                return

        update_business_information(
            business_name,

            business_address,

            business_phone,

            business_email,

            receipt_header_value,

            receipt_footer_value
        )

        messagebox.showinfo(
            "Success",
            "Business information saved successfully.",
            parent=window
        )

    # =====================================
    # BUTTONS
    # =====================================

    button_frame = tk.Frame(main_frame)

    button_frame.pack(
        fill="x",
        pady=25
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
        padx=10
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
        padx=10
    )