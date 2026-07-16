import tkinter as tk

# Import settings sub-windows
from gui.business_settings_window import open_business_settings
from gui.sales_settings_window import open_sales_settings
from gui.system_info_window import open_system_information
from gui.inventory_settings_window import open_inventory_settings
from gui.backup_recovery_window import (
    open_backup_recovery_window
)

from gui.report_settings_window import (
    open_report_settings_window
)



def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )



def open_settings_window(parent):

    parent.withdraw()



    settings_window = tk.Toplevel(parent)

    settings_window.title(
        "SETTINGS"
    )

    settings_window.resizable(
        False,
        False
    )


    center_window(
        settings_window,
        800,
        550
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


    button_width = 18

    button_height = 2



    # =====================================
    # CLOSE FUNCTION
    # =====================================

    def close_settings():

        settings_window.destroy()

        parent.deiconify()



    settings_window.protocol(
        "WM_DELETE_WINDOW",
        close_settings
    )



    # =====================================
    # MAIN FRAME
    # =====================================

    main_frame = tk.Frame(
        settings_window,
        padx=20,
        pady=20
    )

    main_frame.pack(
        expand=True
    )



    tk.Label(
        main_frame,
        text="SETTINGS",
        font=title_font
    ).pack(
        pady=(0,25)
    )



    # =====================================
    # BUTTON FRAME
    # =====================================

    btn_frame = tk.Frame(
        main_frame
    )

    btn_frame.pack()



    # =====================================
    # BUSINESS INFORMATION
    # =====================================

    tk.Button(
        btn_frame,
        text="Business",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=lambda:
            open_business_settings(settings_window)

    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )



    # =====================================
    # SALES SETTINGS
    # =====================================

    tk.Button(
        btn_frame,
        text="Sales",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=lambda:
            open_sales_settings(settings_window)

    ).grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )



    # =====================================
    # INVENTORY SETTINGS
    # =====================================

    tk.Button(
        btn_frame,
        text="Inventory",
        width=button_width,
        height=button_height,
        bg="#16a085",
        fg="white",
        font=button_font,
        command=lambda:
            open_inventory_settings(settings_window)

    ).grid(
        row=0,
        column=2,
        padx=10,
        pady=10
    )



    # =====================================
    # BACKUP & RECOVERY
    # =====================================

    tk.Button(
        btn_frame,
        text="Backup & Recovery",
        width=button_width,
        height=button_height,
        bg="#9b59b6",
        fg="white",
        font=button_font,
        command=lambda:
            open_backup_recovery_window(settings_window)

    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )



    # =====================================
    # SYSTEM INFORMATION
    # =====================================

    tk.Button(
        btn_frame,
        text="System Information",
        width=button_width,
        height=button_height,
        bg="#34495e",
        fg="white",
        font=button_font,
        command=lambda:
            open_system_information(settings_window)

    ).grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )



    # =====================================
    # REPORT AUTOMATION SETTINGS
    # =====================================

    tk.Button(
        btn_frame,
        text="Reports",
        width=button_width,
        height=button_height,
        bg="#e67e22",
        fg="white",
        font=button_font,
        command=lambda:
            open_report_settings_window(settings_window)

    ).grid(
        row=1,
        column=2,
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
        command=close_settings

    ).pack(
        pady=30
    )