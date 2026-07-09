import tkinter as tk


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

    window = tk.Toplevel(parent)

    window.title(
        "BACKUP & RECOVERY"
    )

    window.resizable(
        False,
        False
    )

    center_window(
        window,
        700,
        450
    )


    title_font = (
        "Arial",
        20,
        "bold"
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
    # MAIN FRAME
    # =====================================

    main_frame = tk.Frame(
        window,
        padx=20,
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
        text="BACKUP & RECOVERY",
        font=title_font
    ).pack(
        pady=(0,30)
    )



    # =====================================
    # BUTTON FRAME
    # =====================================

    btn_frame = tk.Frame(
        main_frame
    )

    btn_frame.pack()



    button_width = 18

    button_height = 2



    # =====================================
    # AUTOMATIC BACKUP
    # =====================================

    tk.Button(
        btn_frame,
        text="Automatic Backup",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=lambda:
        open_automatic_backup_window(window)
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )



    # =====================================
    # MANUAL BACKUP
    # =====================================

    tk.Button(
        btn_frame,
        text="Manual Backup",
        width=button_width,
        height=button_height,
        bg="#27ae60",
        fg="white",
        font=button_font,
        command=lambda:
        open_manual_backup_window(window)
    ).grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )



    # =====================================
    # RESTORE
    # =====================================

    tk.Button(
        btn_frame,
        text="Restore",
        width=button_width,
        height=button_height,
        bg="#e67e22",
        fg="white",
        font=button_font,
        command=lambda:
        open_restore_window(window)
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )



    # =====================================
    # CLOSE BUTTON
    # =====================================

    tk.Button(
        main_frame,
        text="CLOSE",
        width=25,
        height=2,
        bg="#7f8c8d",
        fg="white",
        font=button_font,
        command=close_window
    ).pack(
        pady=30
    )