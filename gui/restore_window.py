import tkinter as tk
from tkinter import ttk, filedialog, messagebox


from pathlib import Path


from modules.backup.restore_manager import (
    validate_backup_file,
    restore_database
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



def open_restore_window(parent):


    # =====================================
    # HIDE PARENT
    # =====================================

    parent.withdraw()



    # =====================================
    # CREATE WINDOW
    # =====================================

    window = tk.Toplevel()


    window.title(
        "Restore Database"
    )


    window.resizable(
        False,
        False
    )


    center_window(
        window,
        650,
        350
    )



    # =====================================
    # CLOSE FUNCTION
    # =====================================

    def close_window():

        window.destroy()

        parent.deiconify()



    # =====================================
    # VARIABLES
    # =====================================

    backup_file_var = tk.StringVar()



    # =====================================
    # TITLE
    # =====================================

    ttk.Label(

        window,

        text="RESTORE DATABASE",

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
        pady=10
    )



    # =====================================
    # BACKUP FILE SELECTION
    # =====================================

    ttk.Label(

        frame,

        text="Backup file:"

    ).grid(

        row=0,

        column=0,

        sticky="w",

        pady=15

    )



    entry = ttk.Entry(

        frame,

        width=50,

        textvariable=backup_file_var

    )


    entry.grid(

        row=0,

        column=1,

        padx=10

    )



    def browse_backup():


        file = filedialog.askopenfilename(

            title="Select Database Backup",

            filetypes=[

                (
                    "SQLite Database",
                    "*.db"
                ),

                (
                    "All Files",
                    "*.*"
                )

            ]

        )



        if file:


            backup_file_var.set(
                file
            )



    ttk.Button(

        frame,

        text="Browse",

        command=browse_backup

    ).grid(

        row=0,

        column=2

    )



    # =====================================
    # WARNING
    # =====================================

    warning = ttk.Label(

        window,

        text=(

            "WARNING:\n"

            "Restoring will replace the current database.\n"

            "A safety backup will be created automatically."

        ),

        justify="center"

    )


    warning.pack(
        pady=20
    )



    # =====================================
    # RESTORE FUNCTION
    # =====================================

    def restore_now():


        backup_file = (

            backup_file_var.get()

        )



        if not backup_file:


            messagebox.showwarning(

                "No Backup Selected",

                "Please select a backup file."

            )

            return



        if not validate_backup_file(

            backup_file

        ):


            messagebox.showerror(

                "Invalid Backup",

                "The selected file is not a valid POS database backup."

            )

            return



        confirm = messagebox.askyesno(

            "Confirm Restore",

            (

                "Are you sure you want to restore this backup?\n\n"

                "Current data will be replaced."

            )

        )



        if not confirm:

            return



        success = restore_database(

            backup_file

        )



        if success:


            restart = messagebox.askyesno(

                "Restore Complete",

                (

                    "Database restored successfully.\n\n"

                    "Restart application now?"

                )

            )



            if restart:


                window.quit()



            else:


                close_window()



        else:


            messagebox.showerror(

                "Restore Failed",

                "Database restore failed."

            )



    # =====================================
    # BUTTONS
    # =====================================

    button_frame = ttk.Frame(
        window
    )


    button_frame.pack(
        pady=20
    )



    ttk.Button(

        button_frame,

        text="RESTORE",

        width=18,

        command=restore_now

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