"""
GeoMaka POS Audit Logs Window

File:
gui/audit_logs_window.py

Purpose:
Display GeoMaka POS audit logs and allow authorized
users to export the displayed audit records.

Responsibilities:

- Display audit logs.
- Display audit date/time.
- Display username.
- Display role.
- Display module.
- Display action.
- Display short description.
- Export audit logs to a text report.
- Handle audit loading errors safely.
- Handle audit export errors safely.
- Restore the parent window when closed.

Company:
GeoMaka Technologies
"""

import tkinter as tk
from tkinter import ttk, messagebox

from datetime import datetime


# ==========================================================
# AUDIT MANAGEMENT
# ==========================================================

from modules.audit.audit_logs import (
    get_all_audit_logs
)


# ==========================================================
# AUDIT EXPORT
# ==========================================================

from modules.audit.audit_export import (
    save_audit_logs_report
)


# ==========================================================
# CENTER WINDOW
# ==========================================================

def center_window(
    window,
    width,
    height
):
    """
    Centers a Tkinter window on the screen.
    """

    screen_width = (
        window.winfo_screenwidth()
    )

    screen_height = (
        window.winfo_screenheight()
    )


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


# ==========================================================
# FORMAT AUDIT DATE/TIME
# ==========================================================

def _format_audit_datetime(value):
    """
    Formats an audit date/time as:

        YYYY-MM-DD HH:MM:SS

    Example:

        2026-08-13 14:27:29
    """

    if not value:

        return ""


    # ------------------------------------------------------
    # Already a datetime object
    # ------------------------------------------------------

    if isinstance(
        value,
        datetime
    ):

        return value.strftime(
            "%Y-%m-%d %H:%M:%S"
        )


    value = str(value)


    # ------------------------------------------------------
    # Try common datetime formats
    # ------------------------------------------------------

    formats = (

        "%Y-%m-%d %H:%M:%S",

        "%Y-%m-%d %H:%M:%S.%f",

        "%d-%m-%Y %H:%M:%S",

        "%d/%m/%Y %H:%M:%S",

        "%Y/%m/%d %H:%M:%S"

    )


    for date_format in formats:

        try:

            parsed_datetime = datetime.strptime(
                value,
                date_format
            )


            return parsed_datetime.strftime(
                "%Y-%m-%d %H:%M:%S"
            )


        except ValueError:

            continue


    # ------------------------------------------------------
    # Return original value if parsing fails
    # ------------------------------------------------------

    return value


# ==========================================================
# GET AUDIT VALUE
# ==========================================================

def _get_audit_value(
    log,
    key,
    index
):
    """
    Safely gets an audit field.

    Supports:

    1. Dictionary-style rows
    2. SQLite tuple-style rows

    Returns:
        Field value or empty string.
    """

    # ======================================================
    # DICTIONARY / SQLITE ROW
    # ======================================================

    try:

        return log[key]

    except (
        TypeError,
        KeyError,
        IndexError
    ):

        pass


    # ======================================================
    # TUPLE / LIST
    # ======================================================

    try:

        return log[index]

    except (
        TypeError,
        IndexError
    ):

        return ""


# ==========================================================
# AUDIT LOG WINDOW
# ==========================================================

def open_audit_logs_window(
    parent
):
    """
    Opens the Audit Logs window.
    """

    # ======================================================
    # HIDE PARENT
    # ======================================================

    if (
        parent
        and
        parent.winfo_exists()
    ):

        parent.withdraw()


    # ======================================================
    # CREATE WINDOW
    # ======================================================

    root = tk.Toplevel(
        parent
    )


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


    # ======================================================
    # CLOSE WINDOW
    # ======================================================

    def close_window():

        root.destroy()


        if (
            parent
            and
            parent.winfo_exists()
        ):

            parent.deiconify()


    # ======================================================
    # TITLE
    # ======================================================

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


    # ======================================================
    # GENERATED DATE/TIME
    # ======================================================

    generated = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    tk.Label(
        root,
        text=f"Generated: {generated}"
    ).pack()


    # ======================================================
    # TABLE FRAME
    # ======================================================

    table_frame = tk.Frame(
        root
    )


    table_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


    # ======================================================
    # TABLE COLUMNS
    # ======================================================

    columns = (

        "Date Time",

        "Username",

        "Role",

        "Module",

        "Action",

        "Description"

    )


    # ======================================================
    # TREEVIEW
    # ======================================================

    tree = ttk.Treeview(

        table_frame,

        columns=columns,

        show="headings"

    )


    # ======================================================
    # HEADINGS
    # ======================================================

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


    # ======================================================
    # COLUMN WIDTHS
    # ======================================================

    tree.column(
        "Date Time",
        width=170,
        minwidth=150
    )


    tree.column(
        "Username",
        width=120,
        minwidth=100
    )


    tree.column(
        "Role",
        width=130,
        minwidth=110
    )


    tree.column(
        "Module",
        width=120,
        minwidth=100
    )


    tree.column(
        "Action",
        width=120,
        minwidth=100
    )


    tree.column(
        "Description",
        width=350,
        minwidth=250
    )


    # ======================================================
    # TABLE SCROLLBAR
    # ======================================================

    scrollbar = ttk.Scrollbar(

        table_frame,

        orient="vertical",

        command=tree.yview

    )


    tree.configure(
        yscrollcommand=scrollbar.set
    )


    # ======================================================
    # PACK TABLE
    # ======================================================

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )


    scrollbar.pack(
        side="right",
        fill="y"
    )


    # ======================================================
    # LOAD AUDIT LOGS
    # ======================================================

    logs = []


    try:

        logs = get_all_audit_logs()


        if logs is None:

            logs = []


    except Exception as error:

        messagebox.showerror(
            "Audit Logs Error",
            (
                "Unable to load audit logs.\n\n"
                f"Error:\n{error}"
            ),
            parent=root
        )


        logs = []


    # ======================================================
    # DISPLAY AUDIT LOGS
    # ======================================================

    for log in logs:

        # --------------------------------------------------
        # DATE/TIME
        # --------------------------------------------------

        log_datetime = _get_audit_value(
            log,
            "log_datetime",
            1
        )


        log_datetime = _format_audit_datetime(
            log_datetime
        )


        # --------------------------------------------------
        # USERNAME
        # --------------------------------------------------

        username = _get_audit_value(
            log,
            "username",
            2
        )


        # --------------------------------------------------
        # ROLE
        # --------------------------------------------------

        role = _get_audit_value(
            log,
            "role",
            3
        )


        # --------------------------------------------------
        # MODULE
        # --------------------------------------------------

        module = _get_audit_value(
            log,
            "module",
            4
        )


        # --------------------------------------------------
        # ACTION
        # --------------------------------------------------

        action = _get_audit_value(
            log,
            "action",
            5
        )


        # --------------------------------------------------
        # SHORT DESCRIPTION
        # --------------------------------------------------

        description = _get_audit_value(
            log,
            "description",
            6
        )


        tree.insert(

            "",

            "end",

            values=(

                log_datetime,

                username,

                role,

                module,

                action,

                description

            )

        )


    # ======================================================
    # NO LOGS MESSAGE
    # ======================================================

    if not logs:

        tree.insert(

            "",

            "end",

            values=(

                "",

                "",

                "",

                "",

                "",

                "No audit log records found."

            )

        )


    # ======================================================
    # BUTTON FRAME
    # ======================================================

    button_frame = tk.Frame(
        root
    )


    button_frame.pack(
        pady=10
    )


    # ======================================================
    # SAVE AUDIT REPORT
    # ======================================================

    def save_report():

        # --------------------------------------------------
        # PREVENT EXPORT WHEN THERE ARE NO LOGS
        # --------------------------------------------------

        if not logs:

            messagebox.showinfo(
                "Audit Export",
                (
                    "There are no audit log records "
                    "to export."
                ),
                parent=root
            )

            return


        # --------------------------------------------------
        # EXPORT AUDIT REPORT
        # --------------------------------------------------

        try:

            file_path = save_audit_logs_report(
                generated,
                logs
            )


        except Exception as error:

            messagebox.showerror(
                "Audit Export Error",
                (
                    "The audit log report could not "
                    "be saved.\n\n"
                    f"Error:\n{error}"
                ),
                parent=root
            )

            return


        # --------------------------------------------------
        # EXPORT SUCCESS
        # --------------------------------------------------

        messagebox.showinfo(
            "Audit Report Saved",
            (
                "Audit Logs exported successfully.\n\n"
                f"Saved File:\n{file_path}"
            ),
            parent=root
        )


    # ======================================================
    # SAVE BUTTON
    # ======================================================

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


    # ======================================================
    # CLOSE BUTTON
    # ======================================================

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


    # ======================================================
    # WINDOW CLOSE EVENT
    # ======================================================

    root.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )


    return root