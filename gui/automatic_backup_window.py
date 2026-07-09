import tkinter as tk
from tkinter import ttk, filedialog, messagebox


from pathlib import Path


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


    x = (
        screen_width // 2
        -
        width // 2
    )


    y = (
        screen_height // 2
        -
        height // 2
    )


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

    window = tk.Toplevel()


    window.title(
        "Automatic Backup Settings"
    )


    window.resizable(
        False,
        False
    )


    center_window(
        window,
        650,
        450
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

    settings = get_backup_settings()



    if settings:


        enabled_value = (
            settings["automatic_backup_enabled"]
        )


        last_backup = (
            settings["last_backup_datetime"]
            or
            "No backup created yet"
        )


        backup_location = (
            settings["backup_location"]
            or
            str(
                get_backup_directory()
            )
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
    # TITLE
    # =====================================

    ttk.Label(

        window,

        text="AUTOMATIC BACKUP",

        font=(
            "Arial",
            18,
            "bold"
        )

    ).pack(
        pady=20
    )



    # =====================================
    # MAIN FRAME
    # =====================================

    frame = ttk.Frame(
        window
    )


    frame.pack(
        padx=30,
        pady=10,
        fill="both"
    )



    # =====================================
    # ENABLE BACKUP
    # =====================================

    ttk.Checkbutton(

        frame,

        text="Enable automatic backup",

        variable=automatic_backup_var

    ).grid(

        row=0,

        column=0,

        sticky="w",

        pady=10

    )



    # =====================================
    # LAST BACKUP
    # =====================================

    ttk.Label(

        frame,

        text="Last automatic backup:"

    ).grid(

        row=1,

        column=0,

        sticky="w",

        pady=10

    )


    ttk.Label(

        frame,

        text=last_backup

    ).grid(

        row=1,

        column=1,

        sticky="w",

        padx=20

    )



    # =====================================
    # BACKUP LOCATION
    # =====================================

    ttk.Label(

        frame,

        text="Backup location:"

    ).grid(

        row=2,

        column=0,

        sticky="w",

        pady=10

    )



    location_entry = ttk.Entry(

        frame,

        width=45,

        textvariable=location_var

    )


    location_entry.grid(

        row=2,

        column=1,

        padx=10

    )



    def browse_location():


        folder = filedialog.askdirectory()


        if folder:

            location_var.set(
                folder
            )



    ttk.Button(

        frame,

        text="Browse",

        command=browse_location

    ).grid(

        row=2,

        column=2,

        padx=5

    )



    # =====================================
    # BACKUP RETENTION
    # =====================================

    ttk.Label(

        frame,

        text="Backups to keep:"

    ).grid(

        row=3,

        column=0,

        sticky="w",

        pady=10

    )



    ttk.Entry(

        frame,

        width=10,

        textvariable=keep_count_var

    ).grid(

        row=3,

        column=1,

        sticky="w",

        padx=10

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

                "Backups to keep must be a positive number."

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

            "Automatic backup settings updated."

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

        text="SAVE",

        width=15,

        command=save_settings

    ).grid(

        row=0,

        column=0,

        padx=10

    )



    ttk.Button(

        button_frame,

        text="Close",

        width=15,

        command=close_window

    ).grid(

        row=0,

        column=1,

        padx=10

    )



    # =====================================
    # WINDOW X BUTTON
    # =====================================

    window.protocol(

        "WM_DELETE_WINDOW",

        close_window

    )