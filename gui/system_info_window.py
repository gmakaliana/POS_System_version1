import tkinter as tk
from tkinter import ttk

from modules.settings.settings import get_settings



def open_system_information(parent):

    # =====================================
    # HIDE PARENT WINDOW
    # =====================================

    parent.withdraw()



    # =====================================
    # CREATE WINDOW
    # =====================================

    window = tk.Toplevel()

    window.title("System Information")

    window.geometry("500x550")

    window.resizable(False, False)



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

        installed = settings["installed_datetime"]

        backup = settings["last_backup_datetime"]


    except TypeError:

        installed = settings[9]

        backup = settings[10]



    # =====================================
    # TITLE
    # =====================================

    ttk.Label(
        window,
        text="SYSTEM INFORMATION",
        font=("Arial", 16, "bold")
    ).pack(
        pady=20
    )



    # =====================================
    # SYSTEM DETAILS
    # =====================================

    info = [

        ("Software Name",
         "POS System"),

        ("Software Version",
         "1.0"),

        ("Database Version",
         "1.0"),

        ("Installed Date & Time",
         installed),

        ("Last Backup Date & Time",
         backup or "Never"),

        ("Database Location",
         "database/pos.db"),

        ("Developed By",
         "Mpho George Makaliana"),

        ("Phone Number",
         "+266 53239121"),

        ("Email Address",
         "makalianamphogeorge@gmail.com")

    ]



    frame = ttk.Frame(
        window
    )

    frame.pack(
        padx=30
    )



    for index, (label, value) in enumerate(info):

        ttk.Label(
            frame,
            text=label + ":",
            font=("Arial", 10, "bold")
        ).grid(
            row=index,
            column=0,
            sticky="w",
            pady=6
        )



        ttk.Label(
            frame,
            text=value
        ).grid(
            row=index,
            column=1,
            sticky="w",
            padx=15
        )



    # =====================================
    # CLOSE BUTTON
    # =====================================

    ttk.Button(
        window,
        text="Close",
        width=15,
        command=close_window
    ).pack(
        pady=25
    )



    # =====================================
    # WINDOW CONTROL
    # =====================================

    # Handle X button
    window.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )