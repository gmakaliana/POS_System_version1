
"""
GeoMaka POS Report Export

Purpose:
Export sales and stock reports to text files.

Responsibilities:

- Save report text files.
- Format sales reports.
- Format stock reports.
- Export daily sales reports.
- Export monthly sales reports.
- Export daily stock reports.
- Export monthly stock reports.
- Use YYYY-MM-DD date format for daily reports.
- Use YYYY-MM date format for monthly reports.
- Record successful report exports in the audit log.
- Never fail a report export because of an audit failure.

Company:
GeoMaka Technologies
"""

from datetime import datetime

from modules.system.app_paths import (
    get_reports_directory
)

from modules.audit.audit_logs import (
    log_activity
)


# ==========================================================
# DATE FORMAT
# ==========================================================

def _format_report_date(
    value
):
    """
    Converts a date/datetime value to:

        YYYY-MM-DD

    Example:

        2026-08-13
    """

    if isinstance(
        value,
        datetime
    ):

        return value.strftime(
            "%Y-%m-%d"
        )


    return str(value)


# ==========================================================
# MONTH FORMAT
# ==========================================================

def _format_report_month(
    value
):
    """
    Converts a month value to:

        YYYY-MM

    Example:

        2026-08
    """

    if isinstance(
        value,
        datetime
    ):

        return value.strftime(
            "%Y-%m"
        )


    value = str(value)


    # ------------------------------------------------------
    # If a complete date was supplied, keep only YYYY-MM.
    # ------------------------------------------------------

    if len(value) >= 7:

        return value[:7]


    return value


# ==========================================================
# SAVE TEXT FILE
# ==========================================================

def _save_text_file(
    filename,
    content
):

    reports_directory = (
        get_reports_directory()
    )


    reports_directory.mkdir(
        parents=True,
        exist_ok=True
    )


    file_path = (
        reports_directory
        /
        filename
    )


    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)


    return file_path


# ==========================================================
# AUDIT REPORT EXPORT
# ==========================================================

def _audit_report_export():
    """
    Records a successful report export.

    Audit logging is non-fatal.
    """

    try:

        log_activity(
            module="REPORTS",
            action="EXPORT",
            description="Report exported"
        )

    except Exception:

        # --------------------------------------------------
        # Audit failure must never affect report export.
        # --------------------------------------------------

        pass


# ==========================================================
# SALES TABLE FORMATTER
# ==========================================================

def _format_sales_table(
    rows
):

    text = ""


    text += (
        "-" * 150
        +
        "\n"
    )


    text += (
        f"{'Product':25}"
        f"{'Barcode':15}"
        f"{'Unit Cost(M)':15}"
        f"{'Unit Price(M)':15}"
        f"{'Quantity':10}"
        f"{'Total Cost(M)':15}"
        f"{'Gross Sales(M)':15}"
        f"{'Discount(M)':15}"
        f"{'Net Sales(M)':15}"
        f"{'Profit/Loss(M)':15}\n"
    )


    text += (
        "-" * 150
        +
        "\n"
    )


    for row in rows:

        text += (
            f"{str(row[0]):25}"
            f"{str(row[1]):15}"
            f"{row[2]:15.2f}"
            f"{row[3]:15.2f}"
            f"{row[4]:10}"
            f"{row[5]:15.2f}"
            f"{row[6]:15.2f}"
            f"{row[7]:15.2f}"
            f"{row[8]:15.2f}"
            f"{row[9]:15.2f}\n"
        )


    text += (
        "-" * 150
        +
        "\n"
    )


    return text


# ==========================================================
# STOCK TABLE FORMATTER
# ==========================================================

def _format_stock_table(
    rows
):

    text = ""


    text += (
        "-" * 70
        +
        "\n"
    )


    text += (
        f"{'Product':35}"
        f"{'Opening Stock':15}"
        f"{'Quantity Sold':15}"
        f"{'Closing Stock':15}\n"
    )


    text += (
        "-" * 70
        +
        "\n"
    )


    total_open = 0
    total_sold = 0
    total_close = 0


    for row in rows:

        product, sold, closing, opening = row


        text += (
            f"{product:35}"
            f"{opening:<15}"
            f"{sold:<15}"
            f"{closing:<15}\n"
        )


        total_open += opening
        total_sold += sold
        total_close += closing


    text += (
        "-" * 70
        +
        "\n"
    )


    text += (
        f"{'TOTAL':35}"
        f"{total_open:<15}"
        f"{total_sold:<15}"
        f"{total_close:<15}\n"
    )


    text += (
        "-" * 70
        +
        "\n"
    )


    return text


# ==========================================================
# DAILY SALES REPORT EXPORT
# ==========================================================

def save_daily_sales_report(
    report_date,
    generated,
    rows,
    summary
):

    report_date = _format_report_date(
        report_date
    )


    content = ""


    content += (
        "=" * 150
        +
        "\n"
    )


    content += (
        " " * 55
        +
        "DAILY SALES REPORT\n"
    )


    content += (
        "=" * 150
        +
        "\n\n"
    )


    content += (
        f"Report Generated : {generated}\n"
    )


    content += (
        f"Report Date      : {report_date}\n\n"
    )


    content += _format_sales_table(
        rows
    )


    content += "\n"
    content += "DAILY SALES SUMMARY\n"
    content += "\n"


    content += (
        f"Total Products Sold       : "
        f"{summary['products']}\n"
    )


    content += (
        f"Total Quantity Sold       : "
        f"{summary['quantity']} Units\n"
    )


    content += (
        f"Total Cost of Goods Sold  : "
        f"M{summary['cost']:.2f}\n"
    )


    content += (
        f"Gross Sales               : "
        f"M{summary['gross_sales']:.2f}\n"
    )


    content += (
        f"Total Discount            : "
        f"M{summary['discount']:.2f}\n"
    )


    content += (
        f"Net Sales                 : "
        f"M{summary['net_sales']:.2f}\n"
    )


    content += (
        f"Profit/Loss               : "
        f"M{summary['profit']:.2f}\n"
    )


    content += "\n"
    content += "=" * 150
    content += "\n"
    content += "Generated by GeoMaka POS\n"
    content += "=" * 150


    filename = (
        f"daily_sales_{report_date}.txt"
    )


    file_path = _save_text_file(
        filename,
        content
    )


    _audit_report_export()


    return file_path


# ==========================================================
# MONTHLY SALES REPORT EXPORT
# ==========================================================

def save_monthly_sales_report(
    month,
    generated,
    rows,
    summary
):

    month = _format_report_month(
        month
    )


    content = ""


    content += (
        "=" * 150
        +
        "\n"
    )


    content += (
        " " * 55
        +
        "MONTHLY SALES REPORT\n"
    )


    content += (
        "=" * 150
        +
        "\n\n"
    )


    content += (
        f"Report Generated : {generated}\n"
    )


    content += (
        f"Period           : {month}\n\n"
    )


    content += _format_sales_table(
        rows
    )


    content += "\n"
    content += "MONTHLY SALES SUMMARY\n"
    content += "\n"


    content += (
        f"Total Products Sold       : "
        f"{summary['products']}\n"
    )


    content += (
        f"Total Quantity Sold       : "
        f"{summary['quantity']} Units\n"
    )


    content += (
        f"Total Cost of Goods Sold  : "
        f"M{summary['cost']:.2f}\n"
    )


    content += (
        f"Gross Sales               : "
        f"M{summary['gross_sales']:.2f}\n"
    )


    content += (
        f"Total Discount            : "
        f"M{summary['discount']:.2f}\n"
    )


    content += (
        f"Net Sales                 : "
        f"M{summary['net_sales']:.2f}\n"
    )


    content += (
        f"Profit/Loss               : "
        f"M{summary['profit']:.2f}\n"
    )


    content += "\n"
    content += "=" * 150
    content += "\n"
    content += "Generated by GeoMaka POS\n"
    content += "=" * 150


    filename = (
        f"monthly_sales_{month}.txt"
    )


    file_path = _save_text_file(
        filename,
        content
    )


    _audit_report_export()


    return file_path


# ==========================================================
# DAILY STOCK BOOK EXPORT
# ==========================================================

def save_daily_stock_report(
    report_date,
    generated,
    rows
):

    report_date = _format_report_date(
        report_date
    )


    content = ""


    content += (
        "=" * 70
        +
        "\n"
    )


    content += (
        " " * 22
        +
        "DAILY STOCK BOOK\n"
    )


    content += (
        "=" * 70
        +
        "\n\n"
    )


    content += (
        f"Report Generated : {generated}\n"
    )


    content += (
        f"Report Date      : {report_date}\n\n"
    )


    content += _format_stock_table(
        rows
    )


    content += "\n"
    content += "=" * 70
    content += "\n"
    content += "Generated by GeoMaka POS\n"
    content += "=" * 70


    filename = (
        f"daily_stock_{report_date}.txt"
    )


    file_path = _save_text_file(
        filename,
        content
    )


    _audit_report_export()


    return file_path


# ==========================================================
# MONTHLY STOCK BOOK EXPORT
# ==========================================================

def save_monthly_stock_report(
    month,
    generated,
    rows
):

    month = _format_report_month(
        month
    )


    content = ""


    content += (
        "=" * 70
        +
        "\n"
    )


    content += (
        " " * 20
        +
        "MONTHLY STOCK BOOK\n"
    )


    content += (
        "=" * 70
        +
        "\n\n"
    )


    content += (
        f"Report Generated : {generated}\n"
    )


    content += (
        f"Period           : {month}\n\n"
    )


    content += _format_stock_table(
        rows
    )


    content += "\n"
    content += "=" * 70
    content += "\n"
    content += "Generated by GeoMaka POS\n"
    content += "=" * 70


    filename = (
        f"monthly_stock_{month}.txt"
    )


    file_path = _save_text_file(
        filename,
        content
    )


    _audit_report_export()


    return file_path

