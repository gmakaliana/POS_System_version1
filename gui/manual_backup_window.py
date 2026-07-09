import tkinter as tk
from tkinter import filedialog, messagebox

from modules.backup.manual_backup import (
    create_manual_backup
)


def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )


def open_manual_backup_window(parent):

    # =====================================
    # HIDE PARENT
    # =====================================

    parent.withdraw()


    # =====================================
    # CREATE WINDOW
    # =====================================

    window = tk.Toplevel(parent)

    window.title(
        "MANUAL BACKUP"
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
        text="MANUAL DATABASE BACKUP",
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


    destination_var = tk.StringVar()


    # =====================================
    # DESTINATION
    # =====================================

    tk.Label(
        frame,
        text="Backup destination:",
        font=label_font
    ).grid(
        row=0,
        column=0,
        sticky="e",
        padx=(0,10),
        pady=15
    )


    destination_entry = tk.Entry(
        frame,
        width=45,
        textvariable=destination_var
    )

    destination_entry.grid(
        row=0,
        column=1,
        ipady=4,
        pady=15
    )


    def browse_destination():

        folder = filedialog.askdirectory()

        if folder:

            destination_var.set(
                folder
            )


    tk.Button(
        frame,
        text="Browse",
        width=10,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=browse_destination
    ).grid(
        row=0,
        column=2,
        padx=10
    )


    # =====================================
    # CREATE BACKUP
    # =====================================

    def backup_now():

        destination = destination_var.get()


        if not destination:

            messagebox.showwarning(
                "No Location",
                "Please select a backup destination."
            )

            return


        try:

            backup_file = create_manual_backup(
                destination
            )


            if backup_file:

                messagebox.showinfo(
                    "Backup Complete",
                    f"Backup created successfully:\n\n{backup_file}"
                )


            else:

                messagebox.showerror(
                    "Backup Failed",
                    "Database file was not found."
                )


        except Exception as error:

            messagebox.showerror(
                "Backup Error",
                str(error)
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
        text="CREATE BACKUP",
        width=20,
        height=2,
        bg="#27ae60",
        fg="white",
        font=button_font,
        command=backup_now
    ).grid(
        row=0,
        column=0,
        padx=10
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