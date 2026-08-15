"""
GeoMaka POS Report Scheduler

File:
modules/reports/report_scheduler.py

Purpose:
Automatically generate scheduled sales, stock and expense reports.

Responsibilities:

- Generate daily sales reports.
- Generate daily stock books.
- Generate daily expense reports.
- Generate monthly sales reports.
- Generate monthly stock books.
- Generate monthly expense reports.
- Include gross profit in scheduled sales reports.
- Include operating expenses in scheduled sales reports.
- Include net profit/loss in scheduled sales reports.
- Respect automatic report settings.
- Prevent duplicate daily reports.
- Prevent duplicate monthly reports.
- Run the scheduler in a background thread.
- Update the last generated report dates.
- Handle scheduler errors safely.

Company:
GeoMaka Technologies
"""


import threading
import time

from datetime import (
    datetime,
    date
)

import calendar


# ==========================================================
# REPORT SCHEDULER SETTINGS
# ==========================================================

from modules.settings.settings import (
    get_report_scheduler_settings,
    update_last_daily_report_date,
    update_last_monthly_report_month
)


# ==========================================================
# REPORT MANAGEMENT
# ==========================================================

from modules.reports.reports import (
    get_daily_sales,
    get_monthly_sales,
    get_daily_stock_report,
    get_monthly_stock_report,
    get_daily_expenses,
    get_monthly_expenses
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
# REPORT SCHEDULER RUNNING FLAG
# ==========================================================

scheduler_running = False


# ==========================================================
# CHECK IF LAST DAY OF MONTH
# ==========================================================

def is_last_day_of_month():
    """
    Determines whether today is the last day of the month.

    Returns:

        True
            if today is the last day.

        False
            otherwise.
    """

    today = date.today()

    last_day = calendar.monthrange(
        today.year,
        today.month
    )[1]

    return (
        today.day == last_day
    )


# ==========================================================
# GENERATE DAILY SALES REPORT
# ==========================================================

def generate_daily_sales_report():
    """
    Generates and exports the daily sales report.

    The report includes:

    - Total Products Sold
    - Total Quantity Sold
    - Gross Sales
    - Discounts
    - Net Sales
    - Cost of Goods Sold
    - Gross Profit
    - Operating Expenses
    - Net Profit/Loss
    """

    print(
        "Generating daily sales report..."
    )

    today = str(
        date.today()
    )

    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )

    rows, summary = get_daily_sales(
        today
    )

    file_path = save_daily_sales_report(
        today,
        generated,
        rows,
        summary
    )

    print(
        "Daily sales report saved:",
        file_path
    )

    return file_path


# ==========================================================
# GENERATE DAILY STOCK REPORT
# ==========================================================

def generate_daily_stock_report():
    """
    Generates and exports the daily stock book.
    """

    print(
        "Generating daily stock book..."
    )

    today = str(
        date.today()
    )

    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )

    rows = get_daily_stock_report(
        today
    )

    file_path = save_daily_stock_report(
        today,
        generated,
        rows
    )

    print(
        "Daily stock book saved:",
        file_path
    )

    return file_path


# ==========================================================
# GENERATE DAILY EXPENSES REPORT
# ==========================================================

def generate_daily_expenses_report():
    """
    Generates and exports the daily expenses report.

    The report contains:

    - Expense Name
    - Description
    - Amount
    - Expense Date
    - Created At
    - Exact Username

    Expense ID remains internal and is not exported.
    """

    print(
        "Generating daily expenses report..."
    )

    today = str(
        date.today()
    )

    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )

    rows = get_daily_expenses(
        today
    )

    file_path = save_daily_expenses_report(
        today,
        generated,
        rows
    )

    print(
        "Daily expenses report saved:",
        file_path
    )

    return file_path


# ==========================================================
# GENERATE ALL DAILY REPORTS
# ==========================================================

def generate_daily_reports():
    """
    Generates all daily reports.

    Reports:

    1. Daily Sales Report
    2. Daily Stock Book
    3. Daily Expenses Report

    The sales report includes the complete financial
    summary returned by reports.py.

    The last daily report date is updated only after
    all three reports have been successfully exported.
    """

    print(
        "Generating daily reports..."
    )

    today = str(
        date.today()
    )

    # ======================================================
    # DAILY SALES
    # ======================================================

    try:

        generate_daily_sales_report()

    except Exception as error:

        print(
            "Daily Sales Report Error:",
            error
        )

        return False

    # ======================================================
    # DAILY STOCK
    # ======================================================

    try:

        generate_daily_stock_report()

    except Exception as error:

        print(
            "Daily Stock Book Error:",
            error
        )

        return False

    # ======================================================
    # DAILY EXPENSES
    # ======================================================

    try:

        generate_daily_expenses_report()

    except Exception as error:

        print(
            "Daily Expenses Report Error:",
            error
        )

        return False

    # ======================================================
    # MARK DAILY REPORTS AS COMPLETED
    # ======================================================

    update_last_daily_report_date(
        today
    )

    print(
        "Daily reports completed."
    )

    return True


# ==========================================================
# GENERATE MONTHLY SALES REPORT
# ==========================================================

def generate_monthly_sales_report():
    """
    Generates and exports the monthly sales report.

    The report includes:

    - Total Products Sold
    - Total Quantity Sold
    - Gross Sales
    - Discounts
    - Net Sales
    - Cost of Goods Sold
    - Gross Profit
    - Operating Expenses
    - Net Profit/Loss
    """

    print(
        "Generating monthly sales report..."
    )

    month = datetime.now().strftime(
        "%Y-%m"
    )

    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )

    rows, summary = get_monthly_sales(
        month
    )

    file_path = save_monthly_sales_report(
        month,
        generated,
        rows,
        summary
    )

    print(
        "Monthly sales report saved:",
        file_path
    )

    return file_path


# ==========================================================
# GENERATE MONTHLY STOCK REPORT
# ==========================================================

def generate_monthly_stock_report():
    """
    Generates and exports the monthly stock book.
    """

    print(
        "Generating monthly stock book..."
    )

    month = datetime.now().strftime(
        "%Y-%m"
    )

    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )

    rows = get_monthly_stock_report(
        month
    )

    file_path = save_monthly_stock_report(
        month,
        generated,
        rows
    )

    print(
        "Monthly stock book saved:",
        file_path
    )

    return file_path


# ==========================================================
# GENERATE MONTHLY EXPENSES REPORT
# ==========================================================

def generate_monthly_expenses_report():
    """
    Generates and exports the monthly expenses report.

    The report contains:

    - Expense Name
    - Description
    - Amount
    - Expense Date
    - Created At
    - Exact Username

    Expense ID remains internal and is not exported.
    """

    print(
        "Generating monthly expenses report..."
    )

    month = datetime.now().strftime(
        "%Y-%m"
    )

    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )

    rows = get_monthly_expenses(
        month
    )

    file_path = save_monthly_expenses_report(
        month,
        generated,
        rows
    )

    print(
        "Monthly expenses report saved:",
        file_path
    )

    return file_path


# ==========================================================
# GENERATE ALL MONTHLY REPORTS
# ==========================================================

def generate_monthly_reports():
    """
    Generates all monthly reports.

    Reports:

    1. Monthly Sales Report
    2. Monthly Stock Book
    3. Monthly Expenses Report

    The sales report includes the complete financial
    summary returned by reports.py.

    The last monthly report month is updated only after
    all three reports have been successfully exported.
    """

    print(
        "Generating monthly reports..."
    )

    month = datetime.now().strftime(
        "%Y-%m"
    )

    # ======================================================
    # MONTHLY SALES
    # ======================================================

    try:

        generate_monthly_sales_report()

    except Exception as error:

        print(
            "Monthly Sales Report Error:",
            error
        )

        return False

    # ======================================================
    # MONTHLY STOCK
    # ======================================================

    try:

        generate_monthly_stock_report()

    except Exception as error:

        print(
            "Monthly Stock Book Error:",
            error
        )

        return False

    # ======================================================
    # MONTHLY EXPENSES
    # ======================================================

    try:

        generate_monthly_expenses_report()

    except Exception as error:

        print(
            "Monthly Expenses Report Error:",
            error
        )

        return False

    # ======================================================
    # MARK MONTHLY REPORTS AS COMPLETED
    # ======================================================

    update_last_monthly_report_month(
        month
    )

    print(
        "Monthly reports completed."
    )

    return True


# ==========================================================
# SCHEDULER LOOP
# ==========================================================

def report_scheduler_loop():
    """
    Background report scheduler.

    Checks the report settings every 60 seconds.

    Daily reports:

        Generated when:
            - automatic daily reports are enabled.
            - current time matches daily_report_time.
            - today's reports have not already been generated.

        Daily reports generated:
            1. Sales
            2. Stock
            3. Expenses

    Monthly reports:

        Generated when:
            - automatic monthly reports are enabled.
            - today is the last day of the month.
            - current time matches monthly_report_time.
            - this month's reports have not already been generated.

        Monthly reports generated:
            1. Sales
            2. Stock
            3. Expenses
    """

    global scheduler_running

    while scheduler_running:

        try:

            settings = (
                get_report_scheduler_settings()
            )

            if settings:

                # ==================================================
                # READ SETTINGS
                # ==================================================

                daily_enabled = settings[
                    "automatic_daily_report_enabled"
                ]

                daily_time = settings[
                    "daily_report_time"
                ]

                monthly_enabled = settings[
                    "automatic_monthly_report_enabled"
                ]

                monthly_time = settings[
                    "monthly_report_time"
                ]

                last_daily = settings[
                    "last_daily_report_date"
                ]

                last_monthly = settings[
                    "last_monthly_report_month"
                ]

                # ==================================================
                # CURRENT DATE / TIME
                # ==================================================

                current_time = datetime.now().strftime(
                    "%H:%M"
                )

                today = str(
                    date.today()
                )

                current_month = datetime.now().strftime(
                    "%Y-%m"
                )

                # ==================================================
                # DAILY REPORT CHECK
                # ==================================================

                if (

                    daily_enabled == 1

                    and

                    current_time == daily_time

                    and

                    last_daily != today

                ):

                    generate_daily_reports()

                # ==================================================
                # MONTHLY REPORT CHECK
                # ==================================================

                if (

                    monthly_enabled == 1

                    and

                    is_last_day_of_month()

                    and

                    current_time == monthly_time

                    and

                    last_monthly != current_month

                ):

                    generate_monthly_reports()

        except Exception as error:

            print(
                "Report Scheduler Error:",
                error
            )

        # ======================================================
        # WAIT BEFORE NEXT CHECK
        # ======================================================

        time.sleep(
            60
        )


# ==========================================================
# START SCHEDULER
# ==========================================================

def start_report_scheduler():
    """
    Starts the report scheduler in a daemon thread.

    If the scheduler is already running, this function
    does nothing.
    """

    global scheduler_running

    if scheduler_running:

        return

    scheduler_running = True

    thread = threading.Thread(
        target=report_scheduler_loop,
        daemon=True
    )

    thread.start()


# ==========================================================
# STOP SCHEDULER
# ==========================================================

def stop_report_scheduler():
    """
    Stops the background report scheduler.
    """

    global scheduler_running

    scheduler_running = False