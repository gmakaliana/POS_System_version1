import tkinter as tk
from tkinter import ttk


# Import settings sub-windows
from gui.business_settings_window import open_business_settings
from gui.sales_settings_window import open_sales_settings
from gui.system_info_window import open_system_information

from gui.inventory_settings_window import open_inventory_settings 

from gui.backup_recovery_window import (
    open_backup_recovery_window
)

def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

def open_settings_window(parent):

    # =====================================
    # HIDE PARENT WINDOW
    # =====================================

    parent.withdraw()



    # =====================================
    # CREATE SETTINGS WINDOW
    # =====================================

    settings_window = tk.Toplevel()

    settings_window.title("Settings")

    settings_window.resizable(True, True)

    center_window(
        settings_window,
        800,
        550
    )



    # =====================================
    # CLOSE FUNCTION
    # =====================================

    def close_settings():

        settings_window.destroy()

        parent.deiconify()



    # =====================================
    # TITLE
    # =====================================

    title_label = ttk.Label(
        settings_window,
        text="SETTINGS",
        font=("Arial", 18, "bold")
    )

    title_label.pack(
        pady=20
    )



    # =====================================
    # BUTTON FRAME
    # =====================================

    button_frame = ttk.Frame(
        settings_window
    )

    button_frame.pack(
        expand=True,
        pady=10
    )



    # =====================================
    # BUSINESS INFORMATION
    # =====================================

    business_button = ttk.Button(
        button_frame,
        text="Business Information",
        width=30,
        command=lambda:
            open_business_settings(settings_window)
    )

    business_button.pack(
        pady=10
    )



    # =====================================
    # SALES SETTINGS
    # =====================================

    sales_button = ttk.Button(
        button_frame,
        text="Sales",
        width=30,
        command=lambda:
            open_sales_settings(settings_window)
    )

    sales_button.pack(
        pady=10
    )

    # =====================================
    # INVENTORY SETTINGS
    # =====================================

    inventory_button = ttk.Button(
        button_frame,
        text="Inventory",
        width=30,
        command=lambda:
            open_inventory_settings(settings_window)
    )

    inventory_button.pack(
        pady=10
    )


    # =====================================
    # BACKUP & RECOVERY
    # =====================================

    backup_button = ttk.Button(

        button_frame,

        text="Backup & Recovery",

        width=30,

        command=lambda:
        open_backup_recovery_window(settings_window)

    )

    backup_button.pack(
        pady=10
    )



    # =====================================
    # SYSTEM INFORMATION
    # =====================================

    system_button = ttk.Button(
        button_frame,
        text="System Information",
        width=30,
        command=lambda:
            open_system_information(settings_window)
    )

    system_button.pack(
        pady=10
    )



    # =====================================
    # CLOSE BUTTON
    # =====================================

    close_button = ttk.Button(
        settings_window,
        text="Close",
        width=15,
        command=close_settings
    )

    close_button.pack(
        pady=20
    )



    # =====================================
    # WINDOW CONTROL
    # =====================================

    # Handle window X button
    settings_window.protocol(
        "WM_DELETE_WINDOW",
        close_settings
    )