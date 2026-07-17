import threading
import time
from datetime import datetime, date
import calendar


from modules.settings.settings import (
    get_report_scheduler_settings,
    update_last_daily_report_date,
    update_last_monthly_report_month
)


from modules.reports.reports import (
    get_daily_sales,
    get_monthly_sales,
    get_daily_stock_report,
    get_monthly_stock_report
)


from modules.reports.report_export import (
    save_daily_sales_report,
    save_monthly_sales_report,
    save_daily_stock_report,
    save_monthly_stock_report
)



# ==========================================================
# REPORT SCHEDULER RUNNING FLAG
# ==========================================================

scheduler_running = False



# ==========================================================
# CHECK IF LAST DAY OF MONTH
# ==========================================================

def is_last_day_of_month():

    today = date.today()

    last_day = calendar.monthrange(
        today.year,
        today.month
    )[1]

    return today.day == last_day




# ==========================================================
# GENERATE DAILY REPORTS
# ==========================================================

def generate_daily_reports():

    print("Generating daily reports...")


    today = str(date.today())


    rows, summary = get_daily_sales(
        today
    )


    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )


    save_daily_sales_report(
        today,
        generated,
        rows,
        summary
    )



    stock_rows = get_daily_stock_report(
        today
    )


    save_daily_stock_report(
        today,
        generated,
        stock_rows
    )


    update_last_daily_report_date(
        today
    )


    print("Daily reports completed.")




# ==========================================================
# GENERATE MONTHLY REPORTS
# ==========================================================

def generate_monthly_reports():

    print("Generating monthly reports...")


    month = datetime.now().strftime(
        "%Y-%m"
    )


    rows, summary = get_monthly_sales(
        month
    )


    generated = datetime.now().strftime(
        "%d %B %Y | %H:%M"
    )


    save_monthly_sales_report(
        month,
        generated,
        rows,
        summary
    )



    stock_rows = get_monthly_stock_report(
        month
    )


    save_monthly_stock_report(
        month,
        generated,
        stock_rows
    )


    update_last_monthly_report_month(
        month
    )


    print("Monthly reports completed.")




# ==========================================================
# SCHEDULER LOOP
# ==========================================================

def report_scheduler_loop():

    global scheduler_running

    while scheduler_running:

        try:
            settings = get_report_scheduler_settings()

            if settings:

                # sqlite Row conversion

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

                current_time = datetime.now().strftime(
                    "%H:%M"
                )

                today = str(
                    date.today()
                )


                current_month = datetime.now().strftime(
                    "%Y-%m"
                )

                # =====================================
                # DAILY REPORT CHECK
                # =====================================

                if (

                    daily_enabled == 1

                    and

                    current_time == daily_time

                    and

                    last_daily != today

                ):

                    generate_daily_reports()

                # =====================================
                # MONTHLY REPORT CHECK
                # =====================================

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

        # Check every 60 seconds

        time.sleep(60)

# ==========================================================
# START SCHEDULER
# ==========================================================

def start_report_scheduler():

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

    global scheduler_running


    scheduler_running = False