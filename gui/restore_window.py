import tkinter as tk
from tkinter import filedialog, messagebox


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

    window = tk.Toplevel(parent)


    window.title(
        "RESTORE DATABASE"
    )


    window.resizable(
        False,
        False
    )


    center_window(
        window,
        700,
        400
    )


    title_font = (
        "Arial",
        20,
        "bold"
    )


    label_font = (
        "Arial",
        11
    )


    button_font = (
        "Arial",
        11,
        "bold"
    )



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
    # VARIABLES
    # =====================================

    backup_file_var = tk.StringVar()



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
        text="RESTORE DATABASE",
        font=title_font
    ).pack(
        pady=(0,25)
    )



    # =====================================
    # FORM FRAME
    # =====================================

    frame = tk.Frame(
        main_frame
    )

    frame.pack()



    # =====================================
    # FILE SELECTION
    # =====================================

    tk.Label(
        frame,
        text="Backup file:",
        font=label_font
    ).grid(
        row=0,
        column=0,
        sticky="e",
        padx=10,
        pady=15
    )



    entry = tk.Entry(
        frame,
        width=45,
        textvariable=backup_file_var
    )

    entry.grid(
        row=0,
        column=1,
        ipady=4
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



    tk.Button(
        frame,
        text="Browse",
        width=10,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=browse_backup
    ).grid(
        row=0,
        column=2,
        padx=10
    )



    # =====================================
    # WARNING MESSAGE
    # =====================================

    tk.Label(
        main_frame,
        text=(
            "WARNING:\n\n"
            "Restoring will replace the current database.\n"
            "A safety backup will be created automatically."
        ),
        justify="center",
        font=("Arial",11),
        fg="#c0392b"
    ).pack(
        pady=25
    )



    # =====================================
    # RESTORE FUNCTION
    # =====================================

    def restore_now():

        backup_file = backup_file_var.get()


        if not backup_file:

            messagebox.showwarning(
                "No Backup Selected",
                "Please select a backup file.",parent=window
            )

            return



        if not validate_backup_file(
            backup_file
        ):

            messagebox.showerror(
                "Invalid Backup",
                "The selected file is not a valid POS database backup.",parent=window 
            )

            return



        confirm = messagebox.askyesno(
            "Confirm Restore",
            (
                "Are you sure you want to restore this backup?\n\n"
                "Current data will be replaced."
            ),parent=window
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
                ),parent=window 
            )


            if restart:

                window.quit()


            else:

                close_window()



        else:

            messagebox.showerror(
                "Restore Failed",
                "Database restore failed.",parent=window
            )



    # =====================================
    # BUTTONS
    # =====================================

    button_frame = tk.Frame(
        main_frame
    )

    button_frame.pack(
        pady=10
    )



    tk.Button(
        button_frame,
        text="RESTORE",
        width=18,
        height=2,
        bg="#27ae60",
        fg="white",
        font=button_font,
        command=restore_now
    ).grid(
        row=0,
        column=0,
        padx=10
    )

    # Press Enter to save settings
    window.bind(
        "<Return>",
        lambda event: restore_now()
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