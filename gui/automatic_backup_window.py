import tkinter as tk
from tkinter import filedialog, messagebox

from modules.settings.settings import (
    get_backup_settings,
    update_backup_settings
)

from modules.system.app_paths import (
    get_backup_directory
)


def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )


def open_automatic_backup_window(parent):

    # =====================================
    # HIDE PARENT
    # =====================================

    parent.withdraw()


    # =====================================
    # CREATE WINDOW
    # =====================================

    window = tk.Toplevel(parent)

    window.title(
        "AUTOMATIC BACKUP SETTINGS"
    )

    window.resizable(
        False,
        False
    )

    center_window(
        window,
        700,
        500
    )


    title_font = ("Arial", 20, "bold")
    label_font = ("Arial", 11)
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

    settings = get_backup_settings()


    if settings:

        enabled_value = settings["automatic_backup_enabled"]

        last_backup = (
            settings["last_backup_datetime"]
            or
            "No backup created yet"
        )

        backup_location = (
            settings["backup_location"]
            or
            str(get_backup_directory())
        )

        keep_count = (
            settings["backup_keep_count"]
            or
            10
        )

    else:

        enabled_value = 1

        last_backup = (
            "No backup created yet"
        )

        backup_location = str(
            get_backup_directory()
        )

        keep_count = 10


    # =====================================
    # VARIABLES
    # =====================================

    automatic_backup_var = tk.BooleanVar()

    automatic_backup_var.set(
        enabled_value == 1
    )


    location_var = tk.StringVar()

    location_var.set(
        backup_location
    )


    keep_count_var = tk.StringVar()

    keep_count_var.set(
        str(keep_count)
    )


    # =====================================
    # MAIN FRAME
    # =====================================

    main_frame = tk.Frame(
        window,
        padx=25,
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
        text="AUTOMATIC BACKUP",
        font=title_font
    ).pack(
        pady=(0,25)
    )


    # =====================================
    # SETTINGS FRAME
    # =====================================

    frame = tk.Frame(
        main_frame
    )

    frame.pack()


    # =====================================
    # ENABLE BACKUP
    # =====================================

    tk.Checkbutton(
        frame,
        text="Enable automatic backup",
        variable=automatic_backup_var,
        font=label_font
    ).grid(
        row=0,
        column=0,
        columnspan=3,
        sticky="w",
        pady=15
    )


    # =====================================
    # LAST BACKUP
    # =====================================

    tk.Label(
        frame,
        text="Last backup:",
        font=label_font
    ).grid(
        row=1,
        column=0,
        sticky="e",
        padx=(0,10),
        pady=15
    )


    tk.Label(
        frame,
        text=last_backup,
        font=label_font
    ).grid(
        row=1,
        column=1,
        sticky="w",
        pady=15
    )


    # =====================================
    # BACKUP LOCATION
    # =====================================

    tk.Label(
        frame,
        text="Backup location:",
        font=label_font
    ).grid(
        row=2,
        column=0,
        sticky="e",
        padx=(0,10),
        pady=15
    )


    location_entry = tk.Entry(
        frame,
        width=45,
        textvariable=location_var
    )

    location_entry.grid(
        row=2,
        column=1,
        ipady=4,
        pady=15
    )



    def browse_location():

        folder = filedialog.askdirectory()

        if folder:

            location_var.set(folder)



    tk.Button(
        frame,
        text="Browse",
        width=10,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=browse_location
    ).grid(
        row=2,
        column=2,
        padx=10
    )



    # =====================================
    # RETENTION COUNT
    # =====================================

    tk.Label(
        frame,
        text="Backups to keep:",
        font=label_font
    ).grid(
        row=3,
        column=0,
        sticky="e",
        padx=(0,10),
        pady=15
    )


    keep_entry = tk.Entry(
        frame,
        width=15,
        textvariable=keep_count_var
    )

    keep_entry.grid(
        row=3,
        column=1,
        sticky="w",
        ipady=4,
        pady=15
    )

    # =====================================
    # SAVE FUNCTION
    # =====================================

    def save_settings():

        try:

            keep_count = int(
                keep_count_var.get()
            )


            if keep_count <= 0:

                raise ValueError


        except ValueError:

            messagebox.showerror(
                "Invalid Value",
                "Backups to keep must be a positive number.",parent=window
            )

            return


        enabled = 1


        if not automatic_backup_var.get():

            enabled = 0


        update_backup_settings(
            enabled,
            location_var.get(),
            keep_count
        )


        messagebox.showinfo(
            "Saved",
            "Automatic backup settings updated.",parent=window
        )


    # =====================================
    # BUTTONS
    # =====================================

    button_frame = tk.Frame(
        main_frame
    )

    button_frame.pack(
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
        command=save_settings
    ).grid(
        row=0,
        column=0,
        padx=10
    )

    # Press Enter to save settings
    window.bind(
        "<Return>",
        lambda event: save_settings()
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
    ).grid(
        row=0,
        column=1,
        padx=10
    )