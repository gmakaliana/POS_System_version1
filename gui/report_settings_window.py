import tkinter as tk
from tkinter import messagebox

from modules.settings.settings import (
    get_report_scheduler_settings,
    update_report_scheduler_settings
)


# ==========================================================
# CENTER WINDOW
# ==========================================================

def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )



# ==========================================================
# REPORT SETTINGS WINDOW
# ==========================================================

def open_report_settings_window(parent):

    parent.withdraw()


    win = tk.Toplevel(parent)

    win.title(
        "REPORT AUTOMATION SETTINGS"
    )

    win.resizable(
        False,
        False
    )


    center_window(
        win,
        600,
        520
    )



    # ======================================================
    # CLOSE
    # ======================================================

    def close():

        win.destroy()

        if parent.winfo_exists():

            parent.deiconify()



    win.protocol(
        "WM_DELETE_WINDOW",
        close
    )



    # ======================================================
    # LOAD SETTINGS
    # ======================================================

    settings = get_report_scheduler_settings()



    if settings:

        (
            daily_enabled,
            daily_time,
            monthly_enabled,
            monthly_time,
            last_daily,
            last_monthly

        ) = settings


    else:

        daily_enabled = 0
        daily_time = "18:00"

        monthly_enabled = 0
        monthly_time = "18:00"



    # ======================================================
    # VARIABLES
    # ======================================================

    daily_var = tk.IntVar(
        value=daily_enabled
    )


    monthly_var = tk.IntVar(
        value=monthly_enabled
    )


    daily_time_var = tk.StringVar(
        value=daily_time
    )


    monthly_time_var = tk.StringVar(
        value=monthly_time
    )



    # ======================================================
    # MAIN FRAME
    # ======================================================

    main = tk.Frame(
        win,
        padx=30,
        pady=20
    )

    main.pack(
        expand=True
    )



    tk.Label(
        main,
        text="REPORT AUTOMATION SETTINGS",
        font=(
            "Arial",
            16,
            "bold"
        )
    ).pack(
        pady=15
    )



    # ======================================================
    # DAILY REPORT SETTINGS
    # ======================================================

    daily_frame = tk.LabelFrame(
        main,
        text="Daily Reports",
        padx=15,
        pady=10
    )

    daily_frame.pack(
        fill="x",
        pady=10
    )


    tk.Checkbutton(
        daily_frame,
        text="Enable Automatic Daily Reports",
        variable=daily_var
    ).pack(
        anchor="w"
    )


    tk.Label(
        daily_frame,
        text="Generate Time (24 Hour Format):"
    ).pack(
        anchor="w",
        pady=(10,0)
    )


    tk.Entry(
        daily_frame,
        textvariable=daily_time_var,
        width=15
    ).pack(
        anchor="w"
    )



    # ======================================================
    # MONTHLY REPORT SETTINGS
    # ======================================================

    monthly_frame = tk.LabelFrame(
        main,
        text="Monthly Reports",
        padx=15,
        pady=10
    )

    monthly_frame.pack(
        fill="x",
        pady=10
    )


    tk.Checkbutton(
        monthly_frame,
        text="Enable Automatic Monthly Reports",
        variable=monthly_var
    ).pack(
        anchor="w"
    )


    tk.Label(
        monthly_frame,
        text="Generate Time (24 Hour Format):"
    ).pack(
        anchor="w",
        pady=(10,0)
    )


    tk.Entry(
        monthly_frame,
        textvariable=monthly_time_var,
        width=15
    ).pack(
        anchor="w"
    )



    # ======================================================
    # SAVE FUNCTION
    # ======================================================

    def save():

        daily_time = daily_time_var.get().strip()

        monthly_time = monthly_time_var.get().strip()



        # Validate time format

        try:

            hour, minute = map(
                int,
                daily_time.split(":")
            )


            if hour > 23 or minute > 59:

                raise ValueError



            hour, minute = map(
                int,
                monthly_time.split(":")
            )


            if hour > 23 or minute > 59:

                raise ValueError



        except:

            messagebox.showerror(
                "Invalid Time",
                "Use 24 hour format.\nExample: 18:30"
            )

            return



        update_report_scheduler_settings(

            daily_var.get(),

            daily_time,

            monthly_var.get(),

            monthly_time

        )



        messagebox.showinfo(
            "Saved",
            "Report automation settings saved.",parent=main
        )



    # ======================================================
    # BUTTONS
    # ======================================================

    button_frame = tk.Frame(
        main
    )

    button_frame.pack(
        pady=20
    )


    tk.Button(
        button_frame,
        text="Save",
        width=15,
        bg="#27ae60",
        fg="white",
        command=save
    ).pack(
        side="left",
        padx=10
    )



    tk.Button(
        button_frame,
        text="Close",
        width=15,
        bg="#7f8c8d",
        fg="white",
        command=close
    ).pack(
        side="left",
        padx=10
    )