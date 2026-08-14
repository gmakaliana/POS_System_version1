"""
GeoMaka POS Reports Dashboard

File:
gui/report_window.py

Purpose:
Display GeoMaka POS reports.

Responsibilities:

- Display daily sales reports.
- Display monthly sales reports.
- Display daily stock book.
- Display monthly stock book.
- Display daily expense reports.
- Display monthly expense reports.
- Display operating expenses in profit/loss reports.
- Display gross profit.
- Display net profit/loss.
- Export reports.
- Handle report window navigation.

Company:
GeoMaka Technologies
"""


import tkinter as tk

from tkinter import (
    ttk,
    messagebox
)

from datetime import (
    datetime,
    date
)


# ==========================================================
# REPORT MANAGEMENT
# ==========================================================

from modules.reports.reports import (
    get_daily_sales,
    get_monthly_sales,
    get_daily_expenses,
    get_monthly_expenses,
    get_daily_stock_report,
    get_monthly_stock_report
)


# ==========================================================
# REPORT EXPORT
# ==========================================================

from modules.reports.report_export import (
    save_daily_sales_report,
    save_monthly_sales_report,
    save_daily_stock_report,
    save_monthly_stock_report,
    save_daily_expenses_report,
    save_monthly_expenses_report
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
# DASHBOARD
# ==========================================================

def open_reports_dashboard(
    admin_root
):
    """
    Opens the Reports Dashboard.
    """

    if admin_root:
        admin_root.withdraw()


    # ======================================================
    # CREATE WINDOW
    # ======================================================

    root = tk.Toplevel()

    root.title(
        "REPORTS DASHBOARD"
    )

    root.resizable(
        True,
        True
    )

    center_window(
        root,
        900,
        500
    )


    # ======================================================
    # RESTORE ADMIN DASHBOARD
    # ======================================================

    def safe_restore():

        if (
            admin_root
            and
            admin_root.winfo_exists()
        ):
            admin_root.deiconify()


    # ======================================================
    # CLOSE
    # ======================================================

    def close_window():

        root.destroy()

        safe_restore()


    # ======================================================
    # MAIN FRAME
    # ======================================================

    main = tk.Frame(
        root,
        padx=20,
        pady=20
    )

    main.pack(
        expand=True
    )


    # ======================================================
    # TITLE
    # ======================================================

    tk.Label(
        main,
        text="REPORTS DASHBOARD",
        font=(
            "Arial",
            18,
            "bold"
        )
    ).pack(
        pady=10
    )


    # ======================================================
    # BUTTON FRAME
    # ======================================================

    btn = tk.Frame(
        main
    )

    btn.pack()


    style = {
        "width": 28,
        "height": 2
    }


    # ======================================================
    # DAILY SALES
    # ======================================================

    tk.Button(
        btn,
        text="Daily Sales Report & Profit/Loss",
        bg="#3498db",
        fg="white",
        **style,
        command=lambda:
            open_daily_sales(root)
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=10
    )


    # ======================================================
    # MONTHLY SALES
    # ======================================================

    tk.Button(
        btn,
        text="Monthly Sales Report & Profit/Loss",
        bg="#16a085",
        fg="white",
        **style,
        command=lambda:
            open_monthly_sales(root)
    ).grid(
        row=0,
        column=1,
        padx=10,
        pady=10
    )


    # ======================================================
    # DAILY EXPENSES
    # ======================================================

    tk.Button(
        btn,
        text="Daily Expenses",
        bg="#e67e22",
        fg="white",
        **style,
        command=lambda:
            open_daily_expenses(root)
    ).grid(
        row=1,
        column=0,
        padx=10,
        pady=10
    )


    # ======================================================
    # MONTHLY EXPENSES
    # ======================================================

    tk.Button(
        btn,
        text="Monthly Expenses",
        bg="#d35400",
        fg="white",
        **style,
        command=lambda:
            open_monthly_expenses(root)
    ).grid(
        row=1,
        column=1,
        padx=10,
        pady=10
    )


    # ======================================================
    # DAILY STOCK
    # ======================================================

    tk.Button(
        btn,
        text="Daily Stock Book",
        bg="#2ecc71",
        fg="white",
        **style,
        command=lambda:
            open_daily_stock(root)
    ).grid(
        row=2,
        column=0,
        padx=10,
        pady=10
    )


    # ======================================================
    # MONTHLY STOCK
    # ======================================================

    tk.Button(
        btn,
        text="Monthly Stock Book",
        bg="#8e44ad",
        fg="white",
        **style,
        command=lambda:
            open_monthly_stock(root)
    ).grid(
        row=2,
        column=1,
        padx=10,
        pady=10
    )


    # ======================================================
    # CLOSE BUTTON
    # ======================================================

    tk.Button(
        main,
        text="Close",
        bg="#7f8c8d",
        fg="white",
        width=15,
        command=close_window
    ).pack(
        pady=15
    )


    # ======================================================
    # WINDOW CLOSE EVENT
    # ======================================================

    root.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )

    return root


# ==========================================================
# DAILY SALES REPORT
# ==========================================================

def open_daily_sales(
    parent
):
    """
    Displays the Daily Sales Report including:

    - Gross Sales
    - Discounts
    - Net Sales
    - Cost of Goods Sold
    - Gross Profit
    - Operating Expenses
    - Net Profit/Loss

    The visible sales detail table is limited to 9 rows
    so that it remains consistent with the 9-row summary.

    The complete sales data remains available to the
    report export function.
    """

    parent.withdraw()


    # ======================================================
    # CREATE WINDOW
    # ======================================================

    win = tk.Toplevel()

    win.title(
        "DAILY SALES REPORT"
    )

    win.resizable(
        True,
        True
    )

    center_window(
        win,
        1250,
        760
    )


    # ======================================================
    # CLOSE
    # ======================================================

    def close():

        win.destroy()

        if parent.winfo_exists():
            parent.deiconify()


    # ======================================================
    # REPORT INFORMATION
    # ======================================================

    report_date = str(
        date.today()
    )

    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )


    # ======================================================
    # TITLE
    # ======================================================

    tk.Label(
        win,
        text="DAILY SALES REPORT",
        font=(
            "Arial",
            16,
            "bold"
        )
    ).pack()

    tk.Label(
        win,
        text=f"Report Generated: {generated}"
    ).pack()

    tk.Label(
        win,
        text=f"Report Date: {report_date}"
    ).pack()


    # ======================================================
    # TABLE FRAME
    # ======================================================

    frame = tk.Frame(
        win
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


    # ======================================================
    # SALES COLUMNS
    # ======================================================

    columns = (
        "Product",
        "Barcode",
        "Unit Cost(M)",
        "Unit Price(M)",
        "Quantity",
        "Total Cost(M)",
        "Gross Sales(M)",
        "Discount(M)",
        "Net Sales(M)",
        "Gross Profit(M)"
    )


    # ======================================================
    # TREEVIEW
    # ======================================================

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        height=9
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=120,
            minwidth=100
        )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )


    # ======================================================
    # SCROLLBAR
    # ======================================================

    scroll = ttk.Scrollbar(
        frame,
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scroll.set
    )

    scroll.pack(
        side="right",
        fill="y"
    )


    # ======================================================
    # GET REPORT DATA
    # ======================================================

    rows, summary = get_daily_sales(
        report_date
    )


    # ======================================================
    # DISPLAY SALES
    #
    # Only the first 9 rows are displayed.
    #
    # IMPORTANT:
    # The original "rows" variable is NOT changed.
    # Therefore the complete report is still exported.
    # ======================================================

    for row in rows[:9]:

        row = list(row)

        for index in (
            2,
            3,
            5,
            6,
            7,
            8,
            9
        ):

            try:

                row[index] = (
                    f"M{float(row[index] or 0):.2f}"
                )

            except (
                TypeError,
                ValueError
            ):

                row[index] = "M0.00"

        tree.insert(
            "",
            "end",
            values=tuple(row)
        )


    # ======================================================
    # SUMMARY FRAME
    # ======================================================

    sum_frame = tk.Frame(
        win
    )

    sum_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    tk.Label(
        sum_frame,
        text="DAILY PROFIT/LOSS SUMMARY",
        font=(
            "Arial",
            12,
            "bold"
        )
    ).pack(
        anchor="w"
    )


    # ======================================================
    # SUMMARY TABLE
    # ======================================================

    sum_tree = ttk.Treeview(
        sum_frame,
        columns=(
            "Description",
            "Amount"
        ),
        show="headings",
        height=9
    )

    sum_tree.heading(
        "Description",
        text="Description"
    )

    sum_tree.heading(
        "Amount",
        text="Amount"
    )

    sum_tree.column(
        "Description",
        width=400
    )

    sum_tree.column(
        "Amount",
        width=250
    )

    sum_tree.pack(
        fill="x"
    )


    # ======================================================
    # FINANCIAL VALUES
    # ======================================================

    gross_sales = float(
        summary.get(
            "gross_sales",
            0
        ) or 0
    )

    discount = float(
        summary.get(
            "discount",
            0
        ) or 0
    )

    net_sales = float(
        summary.get(
            "net_sales",
            0
        ) or 0
    )

    cost = float(
        summary.get(
            "cost",
            0
        ) or 0
    )

    gross_profit = float(
        summary.get(
            "gross_profit",
            summary.get(
                "profit",
                0
            )
        ) or 0
    )

    total_expenses = float(
        summary.get(
            "total_expenses",
            summary.get(
                "expenses",
                0
            )
        ) or 0
    )

    net_profit = float(
        summary.get(
            "net_profit",
            summary.get(
                "net_profit_loss",
                gross_profit - total_expenses
            )
        ) or 0
    )


    # ======================================================
    # SUMMARY ROWS
    # ======================================================

    summary_rows = [

        (
            "Total Products Sold",
            summary.get(
                "products",
                0
            )
        ),

        (
            "Total Quantity Sold",
            f'{summary.get("quantity", 0)} Units'
        ),

        (
            "Gross Sales",
            f"M{gross_sales:.2f}"
        ),

        (
            "Total Discount",
            f"M{discount:.2f}"
        ),

        (
            "Net Sales",
            f"M{net_sales:.2f}"
        ),

        (
            "Cost of Goods Sold",
            f"M{cost:.2f}"
        ),

        (
            "Gross Profit",
            f"M{gross_profit:.2f}"
        ),

        (
            "Total Operating Expenses",
            f"M{total_expenses:.2f}"
        ),

        (
            "Net Profit/Loss",
            f"M{net_profit:.2f}"
        )
    ]

    for item in summary_rows:

        sum_tree.insert(
            "",
            "end",
            values=item
        )


    # ======================================================
    # PROFIT / LOSS STATUS
    # ======================================================

    if net_profit >= 0:

        result_text = (
            f"NET PROFIT: M{net_profit:.2f}"
        )

    else:

        result_text = (
            f"NET LOSS: M{abs(net_profit):.2f}"
        )

    tk.Label(
        sum_frame,
        text=result_text,
        font=(
            "Arial",
            13,
            "bold"
        )
    ).pack(
        anchor="e",
        pady=(5, 0)
    )


    # ======================================================
    # BUTTON FRAME
    # ======================================================

    button_frame = tk.Frame(
        win
    )

    button_frame.pack(
        pady=10
    )


    # ======================================================
    # SAVE REPORT
    # ======================================================

    def save_report():

        try:

            file_path = save_daily_sales_report(
                report_date,
                generated,
                rows,
                summary
            )

            messagebox.showinfo(
                "Report Saved",
                (
                    "Daily Sales Report saved "
                    "successfully.\n\n"
                    f"Saved File:\n{file_path}"
                ),
                parent=win
            )

        except Exception as error:

            messagebox.showerror(
                "Report Export Error",
                (
                    "The Daily Sales Report "
                    "could not be saved.\n\n"
                    f"Error:\n{error}"
                ),
                parent=win
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
        command=close
    ).pack(
        side="left",
        padx=5
    )

    win.protocol(
        "WM_DELETE_WINDOW",
        close
    )


# ==========================================================
# MONTHLY SALES REPORT
# ==========================================================

def open_monthly_sales(
    parent
):
    """
    Displays the Monthly Sales Report including:

    - Gross Sales
    - Discounts
    - Net Sales
    - Cost of Goods Sold
    - Gross Profit
    - Operating Expenses
    - Net Profit/Loss

    The visible sales detail table is limited to 9 rows
    so that it remains consistent with the 9-row summary.

    The complete sales data remains available to the
    report export function.
    """

    parent.withdraw()


    # ======================================================
    # CREATE WINDOW
    # ======================================================

    win = tk.Toplevel()

    win.title(
        "MONTHLY SALES REPORT"
    )

    win.resizable(
        True,
        True
    )

    center_window(
        win,
        1250,
        760
    )


    # ======================================================
    # CLOSE
    # ======================================================

    def close():

        win.destroy()

        if parent.winfo_exists():
            parent.deiconify()


    # ======================================================
    # REPORT INFORMATION
    # ======================================================

    month = datetime.now().strftime(
        "%Y-%m"
    )

    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )


    # ======================================================
    # TITLE
    # ======================================================

    tk.Label(
        win,
        text="MONTHLY SALES REPORT",
        font=(
            "Arial",
            16,
            "bold"
        )
    ).pack()

    tk.Label(
        win,
        text=f"Report Generated: {generated}"
    ).pack()

    tk.Label(
        win,
        text=f"Period: {month}"
    ).pack()


    # ======================================================
    # TABLE FRAME
    # ======================================================

    frame = tk.Frame(
        win
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


    # ======================================================
    # COLUMNS
    # ======================================================

    columns = (
        "Product",
        "Barcode",
        "Unit Cost(M)",
        "Unit Price(M)",
        "Quantity",
        "Total Cost(M)",
        "Gross Sales(M)",
        "Discount(M)",
        "Net Sales(M)",
        "Gross Profit(M)"
    )

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        height=9
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=120,
            minwidth=100
        )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )


    # ======================================================
    # SCROLLBAR
    # ======================================================

    scroll = ttk.Scrollbar(
        frame,
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scroll.set
    )

    scroll.pack(
        side="right",
        fill="y"
    )


    # ======================================================
    # GET DATA
    # ======================================================

    rows, summary = get_monthly_sales(
        month
    )


    # ======================================================
    # DISPLAY DATA
    #
    # Only the first 9 rows are displayed.
    #
    # IMPORTANT:
    # The original "rows" variable is NOT changed.
    # Therefore the complete report is still exported.
    # ======================================================

    for row in rows[:9]:

        row = list(row)

        for index in (
            2,
            3,
            5,
            6,
            7,
            8,
            9
        ):

            try:

                row[index] = (
                    f"M{float(row[index] or 0):.2f}"
                )

            except (
                TypeError,
                ValueError
            ):

                row[index] = "M0.00"

        tree.insert(
            "",
            "end",
            values=tuple(row)
        )


    # ======================================================
    # SUMMARY
    # ======================================================

    sum_frame = tk.Frame(
        win
    )

    sum_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )

    tk.Label(
        sum_frame,
        text="MONTHLY PROFIT/LOSS SUMMARY",
        font=(
            "Arial",
            12,
            "bold"
        )
    ).pack(
        anchor="w"
    )

    sum_tree = ttk.Treeview(
        sum_frame,
        columns=(
            "Description",
            "Amount"
        ),
        show="headings",
        height=9
    )

    sum_tree.heading(
        "Description",
        text="Description"
    )

    sum_tree.heading(
        "Amount",
        text="Amount"
    )

    sum_tree.column(
        "Description",
        width=400
    )

    sum_tree.column(
        "Amount",
        width=250
    )

    sum_tree.pack(
        fill="x"
    )


    # ======================================================
    # FINANCIAL VALUES
    # ======================================================

    gross_sales = float(
        summary.get(
            "gross_sales",
            0
        ) or 0
    )

    discount = float(
        summary.get(
            "discount",
            0
        ) or 0
    )

    net_sales = float(
        summary.get(
            "net_sales",
            0
        ) or 0
    )

    cost = float(
        summary.get(
            "cost",
            0
        ) or 0
    )

    gross_profit = float(
        summary.get(
            "gross_profit",
            summary.get(
                "profit",
                0
            )
        ) or 0
    )

    total_expenses = float(
        summary.get(
            "total_expenses",
            summary.get(
                "expenses",
                0
            )
        ) or 0
    )

    net_profit = float(
        summary.get(
            "net_profit",
            summary.get(
                "net_profit_loss",
                gross_profit - total_expenses
            )
        ) or 0
    )


    # ======================================================
    # SUMMARY ROWS
    # ======================================================

    summary_rows = [

        (
            "Total Products Sold",
            summary.get(
                "products",
                0
            )
        ),

        (
            "Total Quantity Sold",
            f'{summary.get("quantity", 0)} Units'
        ),

        (
            "Gross Sales",
            f"M{gross_sales:.2f}"
        ),

        (
            "Total Discount",
            f"M{discount:.2f}"
        ),

        (
            "Net Sales",
            f"M{net_sales:.2f}"
        ),

        (
            "Cost of Goods Sold",
            f"M{cost:.2f}"
        ),

        (
            "Gross Profit",
            f"M{gross_profit:.2f}"
        ),

        (
            "Total Operating Expenses",
            f"M{total_expenses:.2f}"
        ),

        (
            "Net Profit/Loss",
            f"M{net_profit:.2f}"
        )
    ]

    for item in summary_rows:

        sum_tree.insert(
            "",
            "end",
            values=item
        )


    # ======================================================
    # PROFIT / LOSS STATUS
    # ======================================================

    if net_profit >= 0:

        result_text = (
            f"NET PROFIT: M{net_profit:.2f}"
        )

    else:

        result_text = (
            f"NET LOSS: M{abs(net_profit):.2f}"
        )

    tk.Label(
        sum_frame,
        text=result_text,
        font=(
            "Arial",
            13,
            "bold"
        )
    ).pack(
        anchor="e",
        pady=(5, 0)
    )


    # ======================================================
    # BUTTON FRAME
    # ======================================================

    button_frame = tk.Frame(
        win
    )

    button_frame.pack(
        pady=10
    )


    # ======================================================
    # SAVE REPORT
    # ======================================================

    def save_report():

        try:

            file_path = save_monthly_sales_report(
                month,
                generated,
                rows,
                summary
            )

            messagebox.showinfo(
                "Report Saved",
                (
                    "Monthly Sales Report saved "
                    "successfully.\n\n"
                    f"Saved File:\n{file_path}"
                ),
                parent=win
            )

        except Exception as error:

            messagebox.showerror(
                "Report Export Error",
                (
                    "The Monthly Sales Report "
                    "could not be saved.\n\n"
                    f"Error:\n{error}"
                ),
                parent=win
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
        command=close
    ).pack(
        side="left",
        padx=5
    )

    win.protocol(
        "WM_DELETE_WINDOW",
        close
    )


# ==========================================================
# DAILY EXPENSES
# ==========================================================

def open_daily_expenses(
    parent
):
    """
    Displays expenses recorded for today.

    Expense ID is intentionally NOT displayed.

    Report row structure from reports.py:

        index 0 = Expense Name
        index 1 = Description
        index 2 = Amount
        index 3 = Expense Date
        index 4 = Created At
        index 5 = Exact Username
        index 6 = Expense ID

    The GUI displays indexes 0 through 5 only.

    Expense ID remains available internally at index 6.
    """

    parent.withdraw()


    # ======================================================
    # CREATE WINDOW
    # ======================================================

    win = tk.Toplevel()

    win.title(
        "DAILY EXPENSES"
    )

    win.resizable(
        True,
        True
    )

    center_window(
        win,
        1050,
        600
    )


    # ======================================================
    # CLOSE
    # ======================================================

    def close():

        win.destroy()

        if parent.winfo_exists():
            parent.deiconify()


    # ======================================================
    # REPORT INFORMATION
    # ======================================================

    today = str(
        date.today()
    )

    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )


    # ======================================================
    # TITLE
    # ======================================================

    tk.Label(
        win,
        text="DAILY EXPENSES",
        font=(
            "Arial",
            16,
            "bold"
        )
    ).pack()

    tk.Label(
        win,
        text=f"Report Date: {today}"
    ).pack()

    tk.Label(
        win,
        text=f"Report Generated: {generated}"
    ).pack()


    # ======================================================
    # TABLE FRAME
    # ======================================================

    frame = tk.Frame(
        win
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


    # ======================================================
    # EXPENSE COLUMNS
    # ======================================================

    columns = (
        "Expense Name",
        "Description",
        "Amount(M)",
        "Expense Date",
        "Created At",
        "Entered By"
    )

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings"
    )

    widths = (
        170,
        250,
        120,
        130,
        160,
        160
    )

    for column, width in zip(
        columns,
        widths
    ):

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=width,
            minwidth=100
        )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )


    # ======================================================
    # SCROLLBAR
    # ======================================================

    scroll = ttk.Scrollbar(
        frame,
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scroll.set
    )

    scroll.pack(
        side="right",
        fill="y"
    )


    # ======================================================
    # GET EXPENSE DATA
    # ======================================================

    rows = get_daily_expenses(
        today
    )

    total_expenses = 0


    # ======================================================
    # DISPLAY EXPENSES
    # ======================================================

    for row in rows:

        try:

            amount = float(
                row[2] or 0
            )

            total_expenses += amount

            amount_display = (
                f"M{amount:.2f}"
            )

        except (
            TypeError,
            ValueError
        ):

            amount_display = "M0.00"


        display_row = (
            row[0],
            row[1],
            amount_display,
            row[3],
            row[4],
            row[5]
        )

        tree.insert(
            "",
            "end",
            values=display_row
        )


    # ======================================================
    # TOTAL
    # ======================================================

    tree.insert(
        "",
        "end",
        values=(
            "TOTAL",
            "",
            f"M{total_expenses:.2f}",
            "",
            "",
            ""
        )
    )


    # ======================================================
    # BUTTON FRAME
    # ======================================================

    button_frame = tk.Frame(
        win
    )

    button_frame.pack(
        pady=10
    )


    # ======================================================
    # SAVE REPORT
    # ======================================================

    def save_report():

        try:

            file_path = save_daily_expenses_report(
                today,
                generated,
                rows
            )

            messagebox.showinfo(
                "Report Saved",
                (
                    "Daily Expenses Report saved "
                    "successfully.\n\n"
                    f"Saved File:\n{file_path}"
                ),
                parent=win
            )

        except Exception as error:

            messagebox.showerror(
                "Report Export Error",
                (
                    "The Daily Expenses Report "
                    "could not be saved.\n\n"
                    f"Error:\n{error}"
                ),
                parent=win
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
        command=close
    ).pack(
        side="left",
        padx=5
    )

    win.protocol(
        "WM_DELETE_WINDOW",
        close
    )


# ==========================================================
# MONTHLY EXPENSES
# ==========================================================

def open_monthly_expenses(
    parent
):
    """
    Displays expenses recorded during the current month.

    Expense ID is intentionally NOT displayed.
    """

    parent.withdraw()


    # ======================================================
    # CREATE WINDOW
    # ======================================================

    win = tk.Toplevel()

    win.title(
        "MONTHLY EXPENSES"
    )

    win.resizable(
        True,
        True
    )

    center_window(
        win,
        1050,
        600
    )


    # ======================================================
    # CLOSE
    # ======================================================

    def close():

        win.destroy()

        if parent.winfo_exists():
            parent.deiconify()


    # ======================================================
    # REPORT INFORMATION
    # ======================================================

    month = datetime.now().strftime(
        "%Y-%m"
    )

    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )


    # ======================================================
    # TITLE
    # ======================================================

    tk.Label(
        win,
        text="MONTHLY EXPENSES",
        font=(
            "Arial",
            16,
            "bold"
        )
    ).pack()

    tk.Label(
        win,
        text=f"Period: {month}"
    ).pack()

    tk.Label(
        win,
        text=f"Report Generated: {generated}"
    ).pack()


    # ======================================================
    # TABLE FRAME
    # ======================================================

    frame = tk.Frame(
        win
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


    # ======================================================
    # EXPENSE COLUMNS
    # ======================================================

    columns = (
        "Expense Name",
        "Description",
        "Amount(M)",
        "Expense Date",
        "Created At",
        "Entered By"
    )

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings"
    )

    widths = (
        170,
        250,
        120,
        130,
        160,
        160
    )

    for column, width in zip(
        columns,
        widths
    ):

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=width,
            minwidth=100
        )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )


    # ======================================================
    # SCROLLBAR
    # ======================================================

    scroll = ttk.Scrollbar(
        frame,
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scroll.set
    )

    scroll.pack(
        side="right",
        fill="y"
    )


    # ======================================================
    # GET EXPENSE DATA
    # ======================================================

    rows = get_monthly_expenses(
        month
    )

    total_expenses = 0


    # ======================================================
    # DISPLAY EXPENSES
    # ======================================================

    for row in rows:

        try:

            amount = float(
                row[2] or 0
            )

            total_expenses += amount

            amount_display = (
                f"M{amount:.2f}"
            )

        except (
            TypeError,
            ValueError
        ):

            amount_display = "M0.00"


        display_row = (
            row[0],
            row[1],
            amount_display,
            row[3],
            row[4],
            row[5]
        )

        tree.insert(
            "",
            "end",
            values=display_row
        )


    # ======================================================
    # TOTAL
    # ======================================================

    tree.insert(
        "",
        "end",
        values=(
            "TOTAL",
            "",
            f"M{total_expenses:.2f}",
            "",
            "",
            ""
        )
    )


    # ======================================================
    # BUTTON FRAME
    # ======================================================

    button_frame = tk.Frame(
        win
    )

    button_frame.pack(
        pady=10
    )


    # ======================================================
    # SAVE REPORT
    # ======================================================

    def save_report():

        try:

            file_path = save_monthly_expenses_report(
                month,
                generated,
                rows
            )

            messagebox.showinfo(
                "Report Saved",
                (
                    "Monthly Expenses Report saved "
                    "successfully.\n\n"
                    f"Saved File:\n{file_path}"
                ),
                parent=win
            )

        except Exception as error:

            messagebox.showerror(
                "Report Export Error",
                (
                    "The Monthly Expenses Report "
                    "could not be saved.\n\n"
                    f"Error:\n{error}"
                ),
                parent=win
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
        command=close
    ).pack(
        side="left",
        padx=5
    )

    win.protocol(
        "WM_DELETE_WINDOW",
        close
    )


# ==========================================================
# DAILY STOCK BOOK
# ==========================================================

def open_daily_stock(
    parent
):

    parent.withdraw()


    # ======================================================
    # CREATE WINDOW
    # ======================================================

    win = tk.Toplevel()

    win.title(
        "DAILY STOCK BOOK"
    )

    win.resizable(
        True,
        True
    )

    center_window(
        win,
        950,
        550
    )


    # ======================================================
    # CLOSE
    # ======================================================

    def close():

        win.destroy()

        if parent.winfo_exists():
            parent.deiconify()


    # ======================================================
    # REPORT INFORMATION
    # ======================================================

    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )

    today = str(
        date.today()
    )


    # ======================================================
    # TITLE
    # ======================================================

    tk.Label(
        win,
        text="DAILY STOCK BOOK",
        font=(
            "Arial",
            16,
            "bold"
        )
    ).pack()

    tk.Label(
        win,
        text=f"Report Generated: {generated}"
    ).pack()

    tk.Label(
        win,
        text=f"Report Date: {today}"
    ).pack()


    # ======================================================
    # TABLE FRAME
    # ======================================================

    frame = tk.Frame(
        win
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


    # ======================================================
    # COLUMNS
    # ======================================================

    columns = (
        "Product",
        "Opening Stock",
        "Quantity Sold",
        "Closing Stock"
    )

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=180
        )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )


    # ======================================================
    # SCROLLBAR
    # ======================================================

    scroll = ttk.Scrollbar(
        frame,
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scroll.set
    )

    scroll.pack(
        side="right",
        fill="y"
    )


    # ======================================================
    # GET DATA
    # ======================================================

    rows = get_daily_stock_report(
        today
    )

    total_open = 0
    total_sold = 0
    total_close = 0


    # ======================================================
    # DISPLAY DATA
    # ======================================================

    for row in rows:

        product, sold, closing, opening = row

        tree.insert(
            "",
            "end",
            values=(
                product,
                opening,
                sold,
                closing
            )
        )

        total_open += (
            opening or 0
        )

        total_sold += (
            sold or 0
        )

        total_close += (
            closing or 0
        )


    # ======================================================
    # TOTAL
    # ======================================================

    tree.insert(
        "",
        "end",
        values=(
            "TOTAL",
            total_open,
            total_sold,
            total_close
        )
    )


    # ======================================================
    # BUTTON FRAME
    # ======================================================

    button_frame = tk.Frame(
        win
    )

    button_frame.pack(
        pady=10
    )


    # ======================================================
    # SAVE REPORT
    # ======================================================

    def save_report():

        try:

            file_path = save_daily_stock_report(
                today,
                generated,
                rows
            )

            messagebox.showinfo(
                "Report Saved",
                (
                    "Daily Stock Book saved "
                    "successfully.\n\n"
                    f"Saved File:\n{file_path}"
                ),
                parent=win
            )

        except Exception as error:

            messagebox.showerror(
                "Report Export Error",
                (
                    "The Daily Stock Book "
                    "could not be saved.\n\n"
                    f"Error:\n{error}"
                ),
                parent=win
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
        command=close
    ).pack(
        side="left",
        padx=5
    )

    win.protocol(
        "WM_DELETE_WINDOW",
        close
    )


# ==========================================================
# MONTHLY STOCK BOOK
# ==========================================================

def open_monthly_stock(
    parent
):

    parent.withdraw()


    # ======================================================
    # CREATE WINDOW
    # ======================================================

    win = tk.Toplevel()

    win.title(
        "MONTHLY STOCK BOOK"
    )

    win.resizable(
        True,
        True
    )

    center_window(
        win,
        950,
        550
    )


    # ======================================================
    # CLOSE
    # ======================================================

    def close():

        win.destroy()

        if parent.winfo_exists():
            parent.deiconify()


    # ======================================================
    # REPORT INFORMATION
    # ======================================================

    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )

    month = datetime.now().strftime(
        "%Y-%m"
    )


    # ======================================================
    # TITLE
    # ======================================================

    tk.Label(
        win,
        text="MONTHLY STOCK BOOK",
        font=(
            "Arial",
            16,
            "bold"
        )
    ).pack()

    tk.Label(
        win,
        text=f"Report Generated: {generated}"
    ).pack()

    tk.Label(
        win,
        text=f"Period: {month}"
    ).pack()


    # ======================================================
    # TABLE FRAME
    # ======================================================

    frame = tk.Frame(
        win
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


    # ======================================================
    # COLUMNS
    # ======================================================

    columns = (
        "Product",
        "Opening Stock",
        "Quantity Sold",
        "Closing Stock"
    )

    tree = ttk.Treeview(
        frame,
        columns=columns,
        show="headings"
    )

    for column in columns:

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=180
        )

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )


    # ======================================================
    # SCROLLBAR
    # ======================================================

    scroll = ttk.Scrollbar(
        frame,
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scroll.set
    )

    scroll.pack(
        side="right",
        fill="y"
    )


    # ======================================================
    # GET DATA
    # ======================================================

    rows = get_monthly_stock_report(
        month
    )

    total_open = 0
    total_sold = 0
    total_close = 0


    # ======================================================
    # DISPLAY DATA
    # ======================================================

    for row in rows:

        product, sold, closing, opening = row

        tree.insert(
            "",
            "end",
            values=(
                product,
                opening,
                sold,
                closing
            )
        )

        total_open += (
            opening or 0
        )

        total_sold += (
            sold or 0
        )

        total_close += (
            closing or 0
        )


    # ======================================================
    # TOTAL
    # ======================================================

    tree.insert(
        "",
        "end",
        values=(
            "TOTAL",
            total_open,
            total_sold,
            total_close
        )
    )


    # ======================================================
    # BUTTON FRAME
    # ======================================================

    button_frame = tk.Frame(
        win
    )

    button_frame.pack(
        pady=10
    )


    # ======================================================
    # SAVE REPORT
    # ======================================================

    def save_report():

        try:

            file_path = save_monthly_stock_report(
                month,
                generated,
                rows
            )

            messagebox.showinfo(
                "Report Saved",
                (
                    "Monthly Stock Book saved "
                    "successfully.\n\n"
                    f"Saved File:\n{file_path}"
                ),
                parent=win
            )

        except Exception as error:

            messagebox.showerror(
                "Report Export Error",
                (
                    "The Monthly Stock Book "
                    "could not be saved.\n\n"
                    f"Error:\n{error}"
                ),
                parent=win
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
        command=close
    ).pack(
        side="left",
        padx=5
    )

    win.protocol(
        "WM_DELETE_WINDOW",
        close
    )

    