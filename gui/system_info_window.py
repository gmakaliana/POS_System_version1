import tkinter as tk

from modules.settings.settings import get_settings


def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")



def open_system_information(parent):

    # =====================================
    # HIDE PARENT WINDOW
    # =====================================

    parent.withdraw()


    # =====================================
    # CREATE WINDOW
    # =====================================

    window = tk.Toplevel(parent)

    window.title("SYSTEM INFORMATION")
    window.resizable(False, False)

    center_window(
        window,
        650,
        550
    )


    title_font = ("Arial", 20, "bold")
    label_font = ("Arial", 11, "bold")
    value_font = ("Arial", 11)



    # =====================================
    # CLOSE FUNCTION
    # =====================================

    def close_window():

        window.destroy()

        if parent and parent.winfo_exists():
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
    # MAIN FRAME
    # =====================================

    main_frame = tk.Frame(
        window,
        padx=30,
        pady=20
    )

    main_frame.pack(
        expand=True
    )



    # =====================================
    # TITLE
    # =====================================

    tk.Label(
        main_frame,
        text="SYSTEM INFORMATION",
        font=title_font
    ).pack(
        pady=(0,25)
    )



    # =====================================
    # INFORMATION FRAME
    # =====================================

    info_frame = tk.Frame(
        main_frame
    )

    info_frame.pack()



    info = [

        ("Software Name", "POS System"),

        ("Software Version", "1.0"),

        ("Database Version", "1.0"),

        ("Installed Date & Time", installed),

        ("Last Backup Date & Time", backup or "Never"),

        ("Developed By", "Mpho George Makaliana"),

        ("Phone Number", "+266 53239121"),

        ("Email Address", "makalianamphogeorge@gmail.com")

    ]



    for index, (label, value) in enumerate(info):

        tk.Label(
            info_frame,
            text=label + ":",
            font=label_font,
            anchor="w"
        ).grid(
            row=index,
            column=0,
            sticky="w",
            pady=7
        )


        tk.Label(
            info_frame,
            text=value,
            font=value_font,
            anchor="w"
        ).grid(
            row=index,
            column=1,
            sticky="w",
            padx=20,
            pady=7
        )



    # =====================================
    # CLOSE BUTTON
    # =====================================

    tk.Button(
        main_frame,
        text="Close",
        width=18,
        height=2,
        bg="#7f8c8d",
        fg="white",
        font=("Arial", 11, "bold"),
        command=close_window
    ).pack(
        pady=30
    )



    # =====================================
    # WINDOW CONTROL
    # =====================================

    window.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )


    return window