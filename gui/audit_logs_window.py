import tkinter as tk
from tkinter import ttk, messagebox

from datetime import datetime

from modules.audit.audit_logs import get_all_audit_logs

from modules.audit.audit_export import save_audit_logs_report



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
# AUDIT LOG WINDOW
# ==========================================================

def open_audit_logs_window(parent):


    parent.withdraw()



    root = tk.Toplevel()


    root.title(
        "AUDIT LOGS"
    )


    root.resizable(
        True,
        True
    )


    center_window(
        root,
        1100,
        550
    )



    # =====================================
    # CLOSE
    # =====================================

    def close_window():

        root.destroy()

        if parent.winfo_exists():

            parent.deiconify()





    # =====================================
    # TITLE
    # =====================================

    tk.Label(
        root,
        text="AUDIT LOGS",
        font=(
            "Arial",
            16,
            "bold"
        )
    ).pack(
        pady=10
    )



    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )



    tk.Label(
        root,
        text=f"Generated: {generated}"
    ).pack()



    # =====================================
    # TABLE FRAME
    # =====================================

    table_frame = tk.Frame(root)

    table_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )



    columns = (

        "Date Time",

        "Username",

        "Role",

        "Module",

        "Action",

        "Description"

    )



    tree = ttk.Treeview(

        table_frame,

        columns=columns,

        show="headings"

    )



    tree.heading(
        "Date Time",
        text="Date & Time"
    )


    tree.heading(
        "Username",
        text="Username"
    )


    tree.heading(
        "Role",
        text="Role"
    )


    tree.heading(
        "Module",
        text="Module"
    )


    tree.heading(
        "Action",
        text="Action"
    )


    tree.heading(
        "Description",
        text="Description"
    )



    tree.column(
        "Date Time",
        width=160
    )


    tree.column(
        "Username",
        width=120
    )


    tree.column(
        "Role",
        width=120
    )


    tree.column(
        "Module",
        width=120
    )


    tree.column(
        "Action",
        width=120
    )


    tree.column(
        "Description",
        width=350
    )



    tree.pack(
        side="left",
        fill="both",
        expand=True
    )



    scrollbar = ttk.Scrollbar(

        table_frame,

        orient="vertical",

        command=tree.yview

    )


    tree.configure(

        yscrollcommand=scrollbar.set

    )


    scrollbar.pack(

        side="right",

        fill="y"

    )



    # =====================================
    # LOAD AUDITS
    # =====================================

    logs = get_all_audit_logs()



    for log in logs:


        tree.insert(

            "",

            "end",

            values=(

                log["log_datetime"],

                log["username"],

                log["role"],

                log["module"],

                log["action"],

                log["description"]

            )

        )



    # =====================================
    # BUTTONS
    # =====================================

    button_frame = tk.Frame(root)


    button_frame.pack(
        pady=10
    )



    def save_report():


        file_path = save_audit_logs_report(
            generated,
            logs
        )


        messagebox.showinfo(
            "Audit Saved",
            f"Audit Logs saved:\n\n{file_path}",
            parent=root
        )



    tk.Button(

        button_frame,

        text="Save",

        width=14,

        bg="#27ae60",

        fg="white",

        command=save_report

    ).pack(

        side="left",

        padx=5

    )



    tk.Button(

        button_frame,

        text="Close",

        width=14,

        bg="#7f8c8d",

        fg="white",

        command=close_window

    ).pack(

        side="left",

        padx=5

    )

    root.protocol(

        "WM_DELETE_WINDOW",

        close_window

    )