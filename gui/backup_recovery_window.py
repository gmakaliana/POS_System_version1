import tkinter as tk
from tkinter import ttk


from gui.automatic_backup_window import (
    open_automatic_backup_window
)

from gui.manual_backup_window import (
    open_manual_backup_window
)

from gui.restore_window import (
    open_restore_window
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



def open_backup_recovery_window(parent):


    # =====================================
    # HIDE PARENT
    # =====================================

    parent.withdraw()



    # =====================================
    # CREATE WINDOW
    # =====================================

    window = tk.Toplevel()


    window.title(
        "Backup & Recovery"
    )


    window.resizable(
        False,
        False
    )


    center_window(
        window,
        450,
        350
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

        text="BACKUP & RECOVERY",

        font=(
            "Arial",
            18,
            "bold"
        )

    ).pack(
        pady=25
    )



    # =====================================
    # BUTTON FRAME
    # =====================================

    frame = ttk.Frame(
        window
    )

    frame.pack(
        expand=True
    )



    # =====================================
    # AUTOMATIC BACKUP
    # =====================================

    ttk.Button(

        frame,

        text="Automatic Backup",

        width=30,

        command=lambda:
        open_automatic_backup_window(
            window
        )

    ).pack(
        pady=10
    )



    # =====================================
    # MANUAL BACKUP
    # =====================================

    ttk.Button(

        frame,

        text="Manual Backup",

        width=30,

        command=lambda:
        open_manual_backup_window(
            window
        )

    ).pack(
        pady=10
    )



    # =====================================
    # RESTORE
    # =====================================

    ttk.Button(

        frame,

        text="Restore",

        width=30,

        command=lambda:
        open_restore_window(
            window
        )

    ).pack(
        pady=10
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
        pady=20
    )



    # =====================================
    # WINDOW X BUTTON
    # =====================================

    window.protocol(

        "WM_DELETE_WINDOW",

        close_window

    )