import tkinter as tk
from tkinter import ttk
from datetime import datetime, date

from modules.reports.reports import (
    get_daily_sales,
    get_monthly_sales,
    get_daily_stock_report,
    get_monthly_stock_report
)


# ==========================================================
# CENTER WINDOW
# ==========================================================
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")


# ==========================================================
# DASHBOARD
# ==========================================================
def open_reports_dashboard(admin_root):

    if admin_root:
        admin_root.withdraw()

    root = tk.Toplevel()
    root.title("REPORTS DASHBOARD")
    center_window(root, 900, 450)

    def safe_restore():
        if admin_root and admin_root.winfo_exists():
            admin_root.deiconify()

    def close_window():
        root.destroy()
        safe_restore()

    main = tk.Frame(root, padx=20, pady=20)
    main.pack(expand=True)

    tk.Label(main, text="REPORTS DASHBOARD",
             font=("Arial", 18, "bold")).pack(pady=10)

    btn = tk.Frame(main)
    btn.pack()

    style = {"width": 28, "height": 2}

    tk.Button(btn, text="Daily Sales Report & Profit/Loss",
              bg="#3498db", fg="white",
              **style,
              command=lambda: open_daily_sales(root)
              ).grid(row=0, column=0, padx=10, pady=10)

    tk.Button(btn, text="Monthly Sales Report & Profit/Loss",
              bg="#16a085", fg="white",
              **style,
              command=lambda: open_monthly_sales(root)
              ).grid(row=0, column=1, padx=10, pady=10)

    tk.Button(btn, text="Daily Stock Book",
              bg="#2ecc71", fg="white",
              **style,
              command=lambda: open_daily_stock(root)
              ).grid(row=1, column=0, padx=10, pady=10)

    tk.Button(btn, text="Monthly Stock Book",
              bg="#8e44ad", fg="white",
              **style,
              command=lambda: open_monthly_stock(root)
              ).grid(row=1, column=1, padx=10, pady=10)

    tk.Button(main, text="Close",
              bg="#7f8c8d", fg="white",
              width=30,
              command=close_window).pack(pady=15)


# ==========================================================
# DAILY SALES REPORT
# ==========================================================
def open_daily_sales(parent):

    parent.withdraw()

    win = tk.Toplevel()
    win.title("DAILY SALES REPORT")
    center_window(win, 1100, 650)

    def close():
        win.destroy()
        if parent.winfo_exists():
            parent.deiconify()

    report_date = str(date.today())
    generated = datetime.now().strftime("%d %B %Y | %H:%M")

    tk.Label(win, text="DAILY SALES REPORT",
             font=("Arial", 16, "bold")).pack()
    tk.Label(win, text=f"Report Generated: {generated}").pack()

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("Product", "Barcode", "UnitCost(M)", "UnitPrice(M)",
               "Quantity(Units)", "TotalCost(M)", "TotalSales(M)", "UnitProfit/Loss(M)")

    tree = ttk.Treeview(frame, columns=columns, show="headings")

    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=120)

    tree.pack(side="left", fill="both", expand=True)

    scroll = ttk.Scrollbar(frame, command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    rows, summary = get_daily_sales(report_date)

    for r in rows:
        tree.insert("", "end", values=tuple(r))

    # SUMMARY TABLE
    sum_frame = tk.Frame(win)
    sum_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(sum_frame, text="DAILY SALES SUMMARY",
             font=("Arial", 12, "bold")).pack(anchor="w")

    sum_tree = ttk.Treeview(sum_frame, columns=("Description", "Amount"),
                            show="headings", height=5)

    sum_tree.heading("Description", text="Description")
    sum_tree.heading("Amount", text="Amount")

    sum_tree.pack(fill="x")

    sum_tree.insert("", "end", values=("Total Products Sold", summary["products"]))
    sum_tree.insert("", "end", values=("Total Quantity Sold", f'{summary["quantity"]} Units'))
    sum_tree.insert("", "end", values=("Total Cost of Goods Sold", f'M{summary["cost"]:.2f}'))
    sum_tree.insert("", "end", values=("Total Sales", f'M{summary["sales"]:.2f}'))
    sum_tree.insert("", "end", values=("Profit/Loss", f'+M{summary["profit"]:.2f}'))

    tk.Button(win, text="Close", command=close).pack(pady=10)


# ==========================================================
# MONTHLY SALES REPORT
# ==========================================================
def open_monthly_sales(parent):

    parent.withdraw()

    win = tk.Toplevel()
    win.title("MONTHLY SALES REPORT")
    center_window(win, 1100, 650)

    def close():
        win.destroy()
        if parent.winfo_exists():
            parent.deiconify()

    month = datetime.now().strftime("%Y-%m")
    generated = datetime.now().strftime("%d %B %Y | %H:%M")

    tk.Label(win, text="MONTHLY SALES REPORT",
             font=("Arial", 16, "bold")).pack()
    tk.Label(win, text=f"Report Generated: {generated}").pack()
    tk.Label(win, text=f"Period: {month}").pack()

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("Product", "Barcode", "UnitCost(M)", "UnitPrice(M)",
               "Quantity(Units)", "TotalCost(M)", "TotalSales(M)", "Profit/Loss(M)")

    tree = ttk.Treeview(frame, columns=columns, show="headings")

    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=120)

    tree.pack(side="left", fill="both", expand=True)

    scroll = ttk.Scrollbar(frame, command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    rows, summary = get_monthly_sales(month)

    for r in rows:
        tree.insert("", "end", values=tuple(r))

    sum_frame = tk.Frame(win)
    sum_frame.pack(fill="x", padx=10, pady=10)

    tk.Label(sum_frame, text="MONTHLY SALES SUMMARY",
             font=("Arial", 12, "bold")).pack(anchor="w")

    sum_tree = ttk.Treeview(sum_frame, columns=("Description", "Amount"),
                            show="headings", height=5)

    sum_tree.heading("Description", text="Description")
    sum_tree.heading("Amount", text="Amount")

    sum_tree.pack(fill="x")

    sum_tree.insert("", "end", values=("Total Products Sold", summary["products"]))
    sum_tree.insert("", "end", values=("Total Quantity Sold", f'{summary["quantity"]} Units'))
    sum_tree.insert("", "end", values=("Total Cost of Goods Sold", f'M{summary["cost"]:.2f}'))
    sum_tree.insert("", "end", values=("Total Sales", f'M{summary["sales"]:.2f}'))
    sum_tree.insert("", "end", values=("Gross Profit/Loss", f'+M{summary["profit"]:.2f}'))

    tk.Button(win, text="Close", command=close).pack(pady=10)


# ==========================================================
# DAILY STOCK BOOK (WITH TOTAL ROW)
# ==========================================================
def open_daily_stock(parent):

    parent.withdraw()

    win = tk.Toplevel()
    win.title("DAILY STOCK BOOK")
    center_window(win, 900, 500)

    def close():
        win.destroy()
        if parent.winfo_exists():
            parent.deiconify()

    generated = datetime.now().strftime("%d %B %Y | %H:%M")

    tk.Label(win, text="DAILY STOCK BOOK",
             font=("Arial", 16, "bold")).pack()
    tk.Label(win, text=f"Report Generated: {generated}").pack()

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("Product", "Opening Stock", "Quantity Sold", "Closing Stock")

    tree = ttk.Treeview(frame, columns=columns, show="headings")

    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=150)

    tree.pack(side="left", fill="both", expand=True)

    scroll = ttk.Scrollbar(frame, command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    today = str(date.today())
    rows = get_daily_stock_report(today)

    total_open, total_sold, total_close = 0, 0, 0

    for r in rows:
        product, sold, closing, opening = r
        tree.insert("", "end", values=(product, opening, sold, closing))

        total_open += opening
        total_sold += sold
        total_close += closing

    # TOTAL ROW
    tree.insert("", "end", values=("TOTAL", total_open, total_sold, total_close))

    tk.Button(win, text="Close", command=close).pack(pady=10)


# ==========================================================
# MONTHLY STOCK BOOK (WITH TOTAL ROW)
# ==========================================================
def open_monthly_stock(parent):

    parent.withdraw()

    win = tk.Toplevel()
    win.title("MONTHLY STOCK BOOK")
    center_window(win, 900, 500)

    def close():
        win.destroy()
        if parent.winfo_exists():
            parent.deiconify()

    generated = datetime.now().strftime("%d %B %Y | %H:%M")
    month = datetime.now().strftime("%Y-%m")

    tk.Label(win, text="MONTHLY STOCK BOOK",
             font=("Arial", 16, "bold")).pack()
    tk.Label(win, text=f"Report Generated: {generated}").pack()
    tk.Label(win, text=f"Period: {month}").pack()

    frame = tk.Frame(win)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = ("Product", "Opening Stock", "Quantity Sold", "Closing Stock")

    tree = ttk.Treeview(frame, columns=columns, show="headings")

    for c in columns:
        tree.heading(c, text=c)
        tree.column(c, width=150)

    tree.pack(side="left", fill="both", expand=True)

    scroll = ttk.Scrollbar(frame, command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    rows = get_monthly_stock_report(month)

    total_open, total_sold, total_close = 0, 0, 0

    for r in rows:
        product, sold, closing, opening = r
        tree.insert("", "end", values=(product, opening, sold, closing))

        total_open += opening
        total_sold += sold
        total_close += closing

    tree.insert("", "end", values=("TOTAL", total_open, total_sold, total_close))

    tk.Button(win, text="Close", command=close).pack(pady=10)