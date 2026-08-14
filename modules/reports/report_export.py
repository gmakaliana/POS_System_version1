
"""
GeoMaka POS Report Export

File:
modules/reports/report_export.py

Purpose:
Export sales, stock, and expense reports to text files.

Responsibilities:

- Save report text files.
- Format sales reports.
- Format stock reports.
- Format expense reports.
- Export daily sales reports.
- Export monthly sales reports.
- Export daily stock reports.
- Export monthly stock reports.
- Export daily expense reports.
- Export monthly expense reports.
- Export gross profit.
- Export operating expenses.
- Export net profit/loss.
- Use YYYY-MM-DD date format for daily reports.
- Use YYYY-MM date format for monthly reports.
- Record successful report exports in the audit log.
- Record the exact report type exported.
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
# SAFE MONEY VALUE
# ==========================================================

def _money(
    value
):
    """
    Safely formats a numeric value as Lesotho Maloti.

    Returns:

        M0.00
    """

    try:

        return (
            f"M{float(value or 0):.2f}"
        )

    except (
        TypeError,
        ValueError
    ):

        return "M0.00"


# ==========================================================
# SAVE TEXT FILE
# ==========================================================

def _save_text_file(
    filename,
    content
):
    """
    Saves report content to the reports directory.

    Returns:
        Path to the saved file.
    """

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

        file.write(
            content
        )

    return file_path


# ==========================================================
# AUDIT REPORT EXPORT
# ==========================================================

def _audit_report_export(
    description
):
    """
    Records a successful report export.

    Audit logging is non-fatal and will never cause
    a successfully exported report to be reported
    as failed.
    """

    try:

        log_activity(
            module="REPORTS",
            action="EXPORT",
            description=description
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
    """
    Formats product-level sales records.

    Expected row structure:

        0 = Product
        1 = Barcode
        2 = Unit Cost
        3 = Unit Price
        4 = Quantity
        5 = Total Cost
        6 = Gross Sales
        7 = Discount
        8 = Net Sales
        9 = Gross Profit
    """

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
            f"{float(row[2] or 0):15.2f}"
            f"{float(row[3] or 0):15.2f}"
            f"{row[4] or 0:10}"
            f"{float(row[5] or 0):15.2f}"
            f"{float(row[6] or 0):15.2f}"
            f"{float(row[7] or 0):15.2f}"
            f"{float(row[8] or 0):15.2f}"
            f"{float(row[9] or 0):15.2f}\n"
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
    """
    Formats stock report records.

    Expected row structure:

        0 = Product
        1 = Quantity Sold
        2 = Closing Stock
        3 = Opening Stock
    """

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

        opening = (
            opening or 0
        )

        sold = (
            sold or 0
        )

        closing = (
            closing or 0
        )

        text += (
            f"{str(product):35}"
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
# EXPENSE TABLE FORMATTER
# ==========================================================

def _format_expense_table(
    rows
):
    """
    Formats expense report records.

    Expected row structure:

        0 = Expense Name
        1 = Description
        2 = Amount
        3 = Expense Date
        4 = Created At
        5 = Entered By
        6 = Expense ID

    Expense ID is intentionally NOT exported.
    """

    text = ""

    text += (
        "-" * 125
        +
        "\n"
    )

    text += (
        f"{'Expense Name':25}"
        f"{'Description':35}"
        f"{'Amount(M)':15}"
        f"{'Expense Date':15}"
        f"{'Created At':20}"
        f"{'Entered By':15}\n"
    )

    text += (
        "-" * 125
        +
        "\n"
    )

    total_expenses = 0

    for row in rows:

        expense_name = (
            row[0]
            if len(row) > 0
            else ""
        )

        description = (
            row[1]
            if len(row) > 1
            else ""
        )

        amount = (
            row[2]
            if len(row) > 2
            else 0
        )

        expense_date = (
            row[3]
            if len(row) > 3
            else ""
        )

        created_at = (
            row[4]
            if len(row) > 4
            else ""
        )

        entered_by = (
            row[5]
            if len(row) > 5
            else ""
        )

        try:

            amount_value = float(
                amount or 0
            )

        except (
            TypeError,
            ValueError
        ):

            amount_value = 0

        total_expenses += (
            amount_value
        )

        expense_date = str(
            expense_date or ""
        )

        created_at = str(
            created_at or ""
        )

        entered_by = str(
            entered_by or ""
        )

        expense_name = str(
            expense_name or ""
        )

        description = str(
            description or ""
        )

        # --------------------------------------------------
        # Prevent long text from destroying table layout.
        # --------------------------------------------------

        expense_name = (
            expense_name[:24]
        )

        description = (
            description[:34]
        )

        entered_by = (
            entered_by[:14]
        )

        expense_date = (
            expense_date[:14]
        )

        created_at = (
            created_at[:19]
        )

        text += (
            f"{expense_name:25}"
            f"{description:35}"
            f"{amount_value:15.2f}"
            f"{expense_date:15}"
            f"{created_at:20}"
            f"{entered_by:15}\n"
        )

    text += (
        "-" * 125
        +
        "\n"
    )

    text += (
        f"{'TOTAL EXPENSES':60}"
        f"{_money(total_expenses):15}\n"
    )

    text += (
        "-" * 125
        +
        "\n"
    )

    return text


# ==========================================================
# SALES SUMMARY FORMATTER
# ==========================================================

def _format_sales_summary(
    summary
):
    """
    Formats the complete sales financial summary.

    Includes:

    - Products sold
    - Quantity sold
    - Cost of Goods Sold
    - Gross Sales
    - Discount
    - Net Sales
    - Gross Profit
    - Operating Expenses
    - Net Profit/Loss
    """

    products = summary.get(
        "products",
        0
    )

    quantity = summary.get(
        "quantity",
        0
    )

    cost = summary.get(
        "cost",
        0
    )

    gross_sales = summary.get(
        "gross_sales",
        0
    )

    discount = summary.get(
        "discount",
        0
    )

    net_sales = summary.get(
        "net_sales",
        0
    )

    # ------------------------------------------------------
    # Existing "profit" remains gross profit for compatibility.
    # ------------------------------------------------------

    gross_profit = summary.get(
        "gross_profit",
        summary.get(
            "profit",
            0
        )
    )

    total_expenses = summary.get(
        "total_expenses",
        summary.get(
            "expenses",
            0
        )
    )

    net_profit = summary.get(
        "net_profit",
        summary.get(
            "net_profit_loss",
            (
                float(gross_profit or 0)
                -
                float(total_expenses or 0)
            )
        )
    )

    text = ""

    text += (
        "Total Products Sold       : "
        f"{products}\n"
    )

    text += (
        "Total Quantity Sold       : "
        f"{quantity} Units\n"
    )

    text += (
        "Total Cost of Goods Sold  : "
        f"{_money(cost)}\n"
    )

    text += (
        "Gross Sales               : "
        f"{_money(gross_sales)}\n"
    )

    text += (
        "Total Discount            : "
        f"{_money(discount)}\n"
    )

    text += (
        "Net Sales                 : "
        f"{_money(net_sales)}\n"
    )

    text += (
        "Gross Profit              : "
        f"{_money(gross_profit)}\n"
    )

    text += (
        "Operating Expenses        : "
        f"{_money(total_expenses)}\n"
    )

    text += (
        "Net Profit/Loss           : "
        f"{_money(net_profit)}\n"
    )

    text += "\n"

    # ------------------------------------------------------
    # Profit/Loss status
    # ------------------------------------------------------

    try:

        net_profit_value = float(
            net_profit or 0
        )

    except (
        TypeError,
        ValueError
    ):

        net_profit_value = 0

    if net_profit_value >= 0:

        text += (
            f"RESULT                    : "
            f"NET PROFIT {_money(net_profit_value)}\n"
        )

    else:

        text += (
            f"RESULT                    : "
            f"NET LOSS {_money(abs(net_profit_value))}\n"
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
    """
    Exports the daily sales report.

    Includes:

    - Sales
    - Cost of Goods Sold
    - Gross Profit
    - Operating Expenses
    - Net Profit/Loss
    """

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

    content += (
        "DAILY PROFIT/LOSS SUMMARY\n"
    )

    content += (
        "-" * 70
        +
        "\n"
    )

    content += _format_sales_summary(
        summary
    )

    content += (
        "-" * 70
        +
        "\n"
    )

    content += "\n"

    content += (
        "=" * 150
        +
        "\n"
    )

    content += (
        "Generated by GeoMaka POS\n"
    )

    content += (
        "=" * 150
    )

    filename = (
        f"daily_sales_{report_date}.txt"
    )

    file_path = _save_text_file(
        filename,
        content
    )

    _audit_report_export(
        "Exported daily sales report"
    )

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
    """
    Exports the monthly sales report.

    Includes:

    - Sales
    - Cost of Goods Sold
    - Gross Profit
    - Operating Expenses
    - Net Profit/Loss
    """

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

    content += (
        "MONTHLY PROFIT/LOSS SUMMARY\n"
    )

    content += (
        "-" * 70
        +
        "\n"
    )

    content += _format_sales_summary(
        summary
    )

    content += (
        "-" * 70
        +
        "\n"
    )

    content += "\n"

    content += (
        "=" * 150
        +
        "\n"
    )

    content += (
        "Generated by GeoMaka POS\n"
    )

    content += (
        "=" * 150
    )

    filename = (
        f"monthly_sales_{month}.txt"
    )

    file_path = _save_text_file(
        filename,
        content
    )

    _audit_report_export(
        "Exported monthly sales report"
    )

    return file_path


# ==========================================================
# DAILY STOCK BOOK EXPORT
# ==========================================================

def save_daily_stock_report(
    report_date,
    generated,
    rows
):
    """
    Exports the daily stock book.
    """

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

    content += (
        "=" * 70
        +
        "\n"
    )

    content += (
        "Generated by GeoMaka POS\n"
    )

    content += (
        "=" * 70
    )

    filename = (
        f"daily_stock_{report_date}.txt"
    )

    file_path = _save_text_file(
        filename,
        content
    )

    _audit_report_export(
        "Exported daily stock book"
    )

    return file_path


# ==========================================================
# MONTHLY STOCK BOOK EXPORT
# ==========================================================

def save_monthly_stock_report(
    month,
    generated,
    rows
):
    """
    Exports the monthly stock book.
    """

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

    content += (
        "=" * 70
        +
        "\n"
    )

    content += (
        "Generated by GeoMaka POS\n"
    )

    content += (
        "=" * 70
    )

    filename = (
        f"monthly_stock_{month}.txt"
    )

    file_path = _save_text_file(
        filename,
        content
    )

    _audit_report_export(
        "Exported monthly stock book"
    )

    return file_path


# ==========================================================
# DAILY EXPENSES REPORT EXPORT
# ==========================================================

def save_daily_expenses_report(
    report_date,
    generated,
    rows
):
    """
    Exports the daily expenses report.

    Expected row structure:

        0 = Expense Name
        1 = Description
        2 = Amount
        3 = Expense Date
        4 = Created At
        5 = Entered By
        6 = Expense ID

    Expense ID is not included in the exported document.
    """

    report_date = _format_report_date(
        report_date
    )

    content = ""

    content += (
        "=" * 125
        +
        "\n"
    )

    content += (
        " " * 45
        +
        "DAILY EXPENSES REPORT\n"
    )

    content += (
        "=" * 125
        +
        "\n\n"
    )

    content += (
        f"Report Generated : {generated}\n"
    )

    content += (
        f"Report Date      : {report_date}\n\n"
    )

    content += _format_expense_table(
        rows
    )

    content += "\n"

    content += (
        "=" * 125
        +
        "\n"
    )

    content += (
        "Generated by GeoMaka POS\n"
    )

    content += (
        "=" * 125
    )

    filename = (
        f"daily_expenses_{report_date}.txt"
    )

    file_path = _save_text_file(
        filename,
        content
    )

    _audit_report_export(
        "Exported daily expenses report"
    )

    return file_path


# ==========================================================
# MONTHLY EXPENSES REPORT EXPORT
# ==========================================================

def save_monthly_expenses_report(
    month,
    generated,
    rows
):
    """
    Exports the monthly expenses report.

    Expected row structure:

        0 = Expense Name
        1 = Description
        2 = Amount
        3 = Expense Date
        4 = Created At
        5 = Entered By
        6 = Expense ID

    Expense ID is not included in the exported document.
    """

    month = _format_report_month(
        month
    )

    content = ""

    content += (
        "=" * 125
        +
        "\n"
    )

    content += (
        " " * 43
        +
        "MONTHLY EXPENSES REPORT\n"
    )

    content += (
        "=" * 125
        +
        "\n\n"
    )

    content += (
        f"Report Generated : {generated}\n"
    )

    content += (
        f"Period           : {month}\n\n"
    )

    content += _format_expense_table(
        rows
    )

    content += "\n"

    content += (
        "=" * 125
        +
        "\n"
    )

    content += (
        "Generated by GeoMaka POS\n"
    )

    content += (
        "=" * 125
    )

    filename = (
        f"monthly_expenses_{month}.txt"
    )

    file_path = _save_text_file(
        filename,
        content
    )

    _audit_report_export(
        "Exported monthly expenses report"
    )

    return file_path

