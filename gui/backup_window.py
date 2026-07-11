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


def open_backup_window(parent):

    # =====================================
    # HIDE PARENT
    # =====================================

    parent.withdraw()


    # =====================================
    # CREATE WINDOW
    # =====================================

    window = tk.Toplevel(parent)

    window.title(
        "BACKUP MANAGEMENT"
    )

    window.resizable(
        False,
        False
    )

    center_window(
        window,
        500,
        300
    )


    title_font = ("Arial", 20, "bold")
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

    frame = tk.Frame(
        window,
        padx=30,
        pady=25
    )

    frame.pack(
        expand=True
    )


    # =====================================
    # TITLE
    # =====================================

    tk.Label(
        frame,
        text="MANUAL DATABASE BACKUP",
        font=title_font
    ).pack(
        pady=(0,25)
    )


    # =====================================
    # BACKUP FUNCTION
    # =====================================

    def select_destination():

        folder = filedialog.askdirectory()


        if not folder:

            return


        try:

            backup = create_manual_backup(
                folder
            )


            if backup:

                messagebox.showinfo(
                    "Backup Complete",
                    f"Backup saved:\n\n{backup}",parent=window
                )


            else:

                messagebox.showerror(
                    "Backup Failed",
                    "Database file not found.",parent=window
                )


        except Exception as error:

            messagebox.showerror(
                "Backup Error",
                str(error),parent=window
            )


    # =====================================
    # BUTTON FRAME
    # =====================================

    button_frame = tk.Frame(
        frame
    )

    button_frame.pack(
        pady=20
    )


    # =====================================
    # BACKUP BUTTON
    # =====================================

    tk.Button(
        button_frame,
        text="CHOOSE BACKUP LOCATION",
        width=25,
        height=2,
        bg="#27ae60",
        fg="white",
        font=button_font,
        command=select_destination
    ).pack(
        pady=10
    )

    # Press Enter to save settings
    window.bind(
        "<Return>",
        lambda event: select_destination()
    )

    # =====================================
    # CLOSE BUTTON
    # =====================================

    tk.Button(
        button_frame,
        text="CLOSE",
        width=20,
        height=2,
        bg="#7f8c8d",
        fg="white",
        font=button_font,
        command=close_window
    ).pack(
        pady=10
    )