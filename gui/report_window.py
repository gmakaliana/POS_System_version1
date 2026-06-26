import tkinter as tk
from datetime import datetime

from modules.reports.reports import (
    get_daily_sales,
    get_monthly_sales,
    get_stock_report,
    get_daily_profit_loss,
    get_monthly_profit_loss
)

from modules.reports.report_charts import (
    bar_chart,
    line_chart
)


# -----------------------------------
# CENTER WINDOW (MATCH ADMIN STYLE)
# -----------------------------------
def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


# -----------------------------------
# REPORT DASHBOARD (RESTORED ADMIN STYLE)
# -----------------------------------
def open_reports_dashboard():

    window = tk.Tk()
    window.title("REPORTS DASHBOARD")
    window.resizable(False, False)

    center_window(window, 800, 550)

    # ✔ MATCH ADMIN DASHBOARD STYLE
    title_font = ("Arial", 20, "bold")
    button_font = ("Arial", 11, "bold")

    def go_back():
        window.destroy()
        from gui.admin_dashboard import open_admin_dashboard
        open_admin_dashboard()

    # -----------------------------------
    # MAIN FRAME (SAME AS ADMIN)
    # -----------------------------------
    main_frame = tk.Frame(window, padx=20, pady=20)
    main_frame.pack(expand=True)

    tk.Label(
        main_frame,
        text="REPORTS DASHBOARD",
        font=title_font
    ).pack(pady=(0, 25))

    btn_frame = tk.Frame(main_frame)
    btn_frame.pack()

    button_width = 18
    button_height = 2

    # =========================
    # ROW 1
    # =========================
    tk.Button(
        btn_frame,
        text="Daily Sales",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=lambda: open_daily_sales(window)
    ).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Monthly Sales",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=lambda: open_monthly_sales(window)
    ).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Stock Report",
        width=button_width,
        height=button_height,
        bg="#3498db",
        fg="white",
        font=button_font,
        command=lambda: open_stock(window)
    ).grid(row=0, column=2, padx=10, pady=10)

    # =========================
    # ROW 2
    # =========================
    tk.Button(
        btn_frame,
        text="Daily Profit",
        width=button_width,
        height=button_height,
        bg="#16a085",
        fg="white",
        font=button_font,
        command=lambda: open_daily_profit(window)
    ).grid(row=1, column=0, padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Monthly Profit",
        width=button_width,
        height=button_height,
        bg="#16a085",
        fg="white",
        font=button_font,
        command=lambda: open_monthly_profit(window)
    ).grid(row=1, column=1, padx=10, pady=10)

    # -----------------------------------
    # BACK BUTTON (ADMIN STYLE RESTORED)
    # -----------------------------------
    tk.Button(
        main_frame,
        text="CLOSE",
        width=25,
        height=2,
        bg="#7f8c8d",
        fg="white",
        font=("Arial", 12, "bold"),
        command=go_back
    ).pack(pady=30)

    window.mainloop()


# ==============================
# DAILY SALES
# ==============================
def open_daily_sales(parent):

    parent.destroy()

    win = tk.Tk()
    win.title("Daily Sales")
    center_window(win, 900, 600)

    from datetime import date
    data = get_daily_sales(str(date.today()))

    labels = [str(r[0]) for r in data]
    values = [r[1] for r in data]

    bar_chart(win, "Daily Sales", labels, values)

    tk.Button(
        win,
        text="Close",
        width=14,
        bg="#7f8c8d",
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda: reopen_reports(win)
    ).pack(pady=10)

    win.mainloop()


# ==============================
# MONTHLY SALES
# ==============================
def open_monthly_sales(parent):

    parent.destroy()

    win = tk.Tk()
    win.title("Monthly Sales")
    center_window(win, 900, 600)

    month = datetime.now().strftime("%Y-%m")
    data = get_monthly_sales(month)

    labels = [str(r[0]) for r in data]
    values = [r[1] for r in data]

    line_chart(win, "Monthly Sales", labels, values)

    tk.Button(
        win,
        text="Close",
        width=14,
        bg="#7f8c8d",
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda: reopen_reports(win)
    ).pack(pady=10)

    win.mainloop()


# ==============================
# STOCK REPORT
# ==============================
def open_stock(parent):

    parent.destroy()

    win = tk.Tk()
    win.title("Stock Report")
    center_window(win, 900, 600)

    data = get_stock_report()

    labels = [r[1] for r in data]
    values = [r[2] for r in data]

    bar_chart(win, "Stock Levels", labels, values)

    tk.Button(
        win,
        text="Close",
        width=14,
        bg="#7f8c8d",
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda: reopen_reports(win)
    ).pack(pady=10)

    win.mainloop()


# ==============================
# DAILY PROFIT
# ==============================
def open_daily_profit(parent):

    parent.destroy()

    win = tk.Tk()
    win.title("Daily Profit")
    center_window(win, 900, 600)

    from datetime import date
    data, total = get_daily_profit_loss(str(date.today()))

    labels = [str(r[0]) for r in data]
    values = [r[1] for r in data]

    bar_chart(win, f"Daily Profit (Total: {total})", labels, values)

    tk.Button(
        win,
        text="Close",
        width=14,
        bg="#7f8c8d",
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda: reopen_reports(win)
    ).pack(pady=10)

    win.mainloop()


# ==============================
# MONTHLY PROFIT
# ==============================
def open_monthly_profit(parent):

    parent.destroy()

    win = tk.Tk()
    win.title("Monthly Profit")
    center_window(win, 900, 600)

    month = datetime.now().strftime("%Y-%m")
    data, total = get_monthly_profit_loss(month)

    labels = [str(r[0]) for r in data]
    values = [r[1] for r in data]

    line_chart(win, f"Monthly Profit (Total: {total})", labels, values)

    tk.Button(
        win,
        text="Close",
        width=14,
        bg="#7f8c8d",
        fg="white",
        font=("Arial", 10, "bold"),
        command=lambda: reopen_reports(win)
    ).pack(pady=10)

    win.mainloop()


# ==============================
# RETURN
# ==============================
def reopen_reports(current_window):
    current_window.destroy()
    open_reports_dashboard()