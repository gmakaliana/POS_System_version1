import tkinter as tk
from tkinter import filedialog, messagebox


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



def open_backup_window(parent):


    window = tk.Toplevel(parent)

    window.title(
        "Backup Management"
    )

    window.resizable(
        False,
        False
    )


    center_window(
        window,
        450,
        250
    )



    frame = tk.Frame(
        window,
        padx=30,
        pady=30
    )

    frame.pack(
        expand=True
    )



    tk.Label(
        frame,
        text="Manual Database Backup",
        font=(
            "Arial",
            16,
            "bold"
        )
    ).pack(
        pady=15
    )



    def select_destination():


        folder = filedialog.askdirectory()


        if not folder:

            return



        backup = create_manual_backup(
            folder
        )


        if backup:


            messagebox.showinfo(
                "Backup Complete",
                f"Backup saved:\n\n{backup}"
            )


        else:


            messagebox.showerror(
                "Backup Failed",
                "Database file not found."
            )



    tk.Button(

        frame,

        text="Choose Backup Location",

        width=25,

        height=2,

        command=select_destination

    ).pack(
        pady=20
    )