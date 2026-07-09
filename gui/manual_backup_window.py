import tkinter as tk
from tkinter import ttk, filedialog, messagebox


from pathlib import Path


from modules.backup.manual_backup import (
    create_manual_backup
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



def open_manual_backup_window(parent):


    # =====================================
    # HIDE PARENT
    # =====================================

    parent.withdraw()



    # =====================================
    # CREATE WINDOW
    # =====================================

    window = tk.Toplevel()


    window.title(
        "Manual Backup"
    )


    window.resizable(
        False,
        False
    )


    center_window(
        window,
        600,
        300
    )



    # =====================================
    # CLOSE FUNCTION
    # =====================================

    def close_window():

        window.destroy()

        parent.deiconify()



    # =====================================
    # TITLE
    # =====================================

    ttk.Label(

        window,

        text="MANUAL DATABASE BACKUP",

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



    destination_var = tk.StringVar()



    # =====================================
    # DESTINATION
    # =====================================

    ttk.Label(

        frame,

        text="Backup destination:"

    ).grid(

        row=0,

        column=0,

        sticky="w",

        pady=20

    )



    destination_entry = ttk.Entry(

        frame,

        width=45,

        textvariable=destination_var

    )


    destination_entry.grid(

        row=0,

        column=1,

        padx=10

    )



    def browse_destination():


        folder = filedialog.askdirectory()



        if folder:

            destination_var.set(
                folder
            )



    ttk.Button(

        frame,

        text="Browse",

        command=browse_destination

    ).grid(

        row=0,

        column=2

    )



    # =====================================
    # CREATE BACKUP
    # =====================================

    def backup_now():


        destination = (
            destination_var.get()
        )


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

    button_frame = ttk.Frame(
        window
    )


    button_frame.pack(
        pady=25
    )



    ttk.Button(

        button_frame,

        text="CREATE BACKUP",

        width=20,

        command=backup_now

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