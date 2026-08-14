
"""
GeoMaka POS Reports

File:
modules/reports/reports.py

Purpose:
Generate sales, stock and profit/loss reports.

Responsibilities:

- Generate daily sales reports.
- Generate monthly sales reports.
- Generate daily stock reports.
- Generate monthly stock reports.
- Calculate Cost of Goods Sold.
- Calculate Gross Profit.
- Retrieve operating expenses.
- Calculate Net Profit/Loss.
- Retrieve exact username for expense records.
- Preserve Expense ID internally.
- Never expose Expense ID as a displayed report field.
- Handle empty expense records safely.

Company:
GeoMaka Technologies
"""

from database.db import get_connection


# ==========================================================
# DAILY SALES REPORT
# ==========================================================

def get_daily_sales(
    report_date
):
    """
    Generates the daily sales report.

    Returns:

        rows:
            Product-level sales records.

        summary:
            Sales, gross profit, expenses and
            net profit/loss totals.
    """

    conn = get_connection()

    cursor = conn.cursor()

    # ======================================================
    # GET DAILY SALES
    # ======================================================

    cursor.execute(
        """
        SELECT

            p.product_name,

            p.barcode,

            p.cost_price,

            st.price,

            SUM(
                st.quantity
            ) AS qty_sold,

            SUM(
                st.quantity
                *
                p.cost_price
            ) AS total_cost,

            SUM(
                st.quantity
                *
                st.price
            ) AS gross_sales,

            SUM(
                st.discount
            ) AS total_discount,

            SUM(
                (
                    st.quantity
                    *
                    st.price
                )
                -
                st.discount
            ) AS net_sales,

            SUM(
                (
                    (
                        st.quantity
                        *
                        st.price
                    )
                    -
                    st.discount
                )
                -
                (
                    st.quantity
                    *
                    p.cost_price
                )
            ) AS profit

        FROM sales_transactions st

        JOIN sales s
            ON s.sale_id = st.sale_id

        JOIN products p
            ON p.product_id = st.product_id

        WHERE DATE(
            s.date_time
        ) = ?

        GROUP BY
            p.product_id,
            p.product_name,
            p.barcode,
            p.cost_price,
            st.price

        ORDER BY
            p.product_name
        """,
        (
            report_date,
        )
    )

    rows = cursor.fetchall()

    # ======================================================
    # SALES SUMMARY
    # ======================================================

    quantity = sum(
        r[4] or 0
        for r in rows
    )

    cost = sum(
        r[5] or 0
        for r in rows
    )

    gross_sales = sum(
        r[6] or 0
        for r in rows
    )

    discount = sum(
        r[7] or 0
        for r in rows
    )

    net_sales = sum(
        r[8] or 0
        for r in rows
    )

    gross_profit = sum(
        r[9] or 0
        for r in rows
    )

    # ======================================================
    # GET DAILY EXPENSES
    # ======================================================

    cursor.execute(
        """
        SELECT
            COALESCE(
                SUM(cost_amount),
                0
            )

        FROM expenses

        WHERE DATE(
            expense_date
        ) = ?
        """,
        (
            report_date,
        )
    )

    expense_result = cursor.fetchone()

    expenses = (
        expense_result[0]
        if expense_result
        and expense_result[0] is not None
        else 0
    )

    # ======================================================
    # NET PROFIT / LOSS
    # ======================================================

    net_profit = (
        gross_profit
        -
        expenses
    )

    # ======================================================
    # SUMMARY
    # ======================================================

    summary = {

        "products": len(rows),

        "quantity": quantity,

        "cost": cost,

        "gross_sales": gross_sales,

        "discount": discount,

        "net_sales": net_sales,

        "profit": gross_profit,

        "gross_profit": gross_profit,

        "expenses": expenses,

        "total_expenses": expenses,

        "net_profit": net_profit,

        "net_profit_loss": net_profit

    }

    conn.close()

    return rows, summary


# ==========================================================
# MONTHLY SALES REPORT
# ==========================================================

def get_monthly_sales(
    month
):
    """
    Generates the monthly sales report.

    Expected month format:

        YYYY-MM
    """

    conn = get_connection()

    cursor = conn.cursor()

    # ======================================================
    # GET MONTHLY SALES
    # ======================================================

    cursor.execute(
        """
        SELECT

            p.product_name,

            p.barcode,

            p.cost_price,

            st.price,

            SUM(
                st.quantity
            ) AS qty_sold,

            SUM(
                st.quantity
                *
                p.cost_price
            ) AS total_cost,

            SUM(
                st.quantity
                *
                st.price
            ) AS gross_sales,

            SUM(
                st.discount
            ) AS total_discount,

            SUM(
                (
                    st.quantity
                    *
                    st.price
                )
                -
                st.discount
            ) AS net_sales,

            SUM(
                (
                    (
                        st.quantity
                        *
                        st.price
                    )
                    -
                    st.discount
                )
                -
                (
                    st.quantity
                    *
                    p.cost_price
                )
            ) AS profit

        FROM sales_transactions st

        JOIN sales s
            ON s.sale_id = st.sale_id

        JOIN products p
            ON p.product_id = st.product_id

        WHERE strftime(
            '%Y-%m',
            s.date_time
        ) = ?

        GROUP BY
            p.product_id,
            p.product_name,
            p.barcode,
            p.cost_price,
            st.price

        ORDER BY
            p.product_name
        """,
        (
            month,
        )
    )

    rows = cursor.fetchall()

    # ======================================================
    # SALES SUMMARY
    # ======================================================

    quantity = sum(
        r[4] or 0
        for r in rows
    )

    cost = sum(
        r[5] or 0
        for r in rows
    )

    gross_sales = sum(
        r[6] or 0
        for r in rows
    )

    discount = sum(
        r[7] or 0
        for r in rows
    )

    net_sales = sum(
        r[8] or 0
        for r in rows
    )

    gross_profit = sum(
        r[9] or 0
        for r in rows
    )

    # ======================================================
    # GET MONTHLY EXPENSES
    # ======================================================

    cursor.execute(
        """
        SELECT
            COALESCE(
                SUM(cost_amount),
                0
            )

        FROM expenses

        WHERE strftime(
            '%Y-%m',
            expense_date
        ) = ?
        """,
        (
            month,
        )
    )

    expense_result = cursor.fetchone()

    expenses = (
        expense_result[0]
        if expense_result
        and expense_result[0] is not None
        else 0
    )

    # ======================================================
    # NET PROFIT / LOSS
    # ======================================================

    net_profit = (
        gross_profit
        -
        expenses
    )

    # ======================================================
    # SUMMARY
    # ======================================================

    summary = {

        "products": len(rows),

        "quantity": quantity,

        "cost": cost,

        "gross_sales": gross_sales,

        "discount": discount,

        "net_sales": net_sales,

        "profit": gross_profit,

        "gross_profit": gross_profit,

        "expenses": expenses,

        "total_expenses": expenses,

        "net_profit": net_profit,

        "net_profit_loss": net_profit

    }

    conn.close()

    return rows, summary


# ==========================================================
# DAILY EXPENSES
# ==========================================================

def get_daily_expenses(
    report_date
):
    """
    Retrieves expenses recorded for a specific date.

    Returned tuple structure:

        index 0 = expense_name
        index 1 = description
        index 2 = cost_amount
        index 3 = expense_date
        index 4 = created_at
        index 5 = entered_by_username
        index 6 = expense_id

    IMPORTANT:

        The GUI displays indexes 0 through 5.

        Therefore:

            Expense ID is NOT displayed.

            Exact username is displayed.

        Expense ID is retained internally at index 6.
    """

    conn = get_connection()

    cursor = conn.cursor()

    # ======================================================
    # GET EXPENSES WITH EXACT USERNAME
    # ======================================================

    cursor.execute(
        """
        SELECT

            e.expense_name,

            e.description,

            e.cost_amount,

            e.expense_date,

            e.created_at,

            COALESCE(
                u.username,
                'Unknown User'
            ) AS entered_by_username,

            e.expense_id

        FROM expenses e

        LEFT JOIN users u
            ON u.user_id = e.entered_by

        WHERE DATE(
            e.expense_date
        ) = ?

        ORDER BY
            e.expense_id DESC
        """,
        (
            report_date,
        )
    )

    database_rows = cursor.fetchall()

    # ======================================================
    # PREPARE REPORT ROWS
    # ======================================================

    rows = []

    for row in database_rows:

        rows.append(
            (
                row[0],  # Expense Name
                row[1],  # Description
                row[2],  # Amount
                row[3],  # Expense Date
                row[4],  # Created At
                row[5],  # Exact Username
                row[6]   # Expense ID - internal only
            )
        )

    conn.close()

    return rows


# ==========================================================
# MONTHLY EXPENSES
# ==========================================================

def get_monthly_expenses(
    month
):
    """
    Retrieves expenses recorded during a month.

    Expected month format:

        YYYY-MM

    Returned tuple structure:

        index 0 = expense_name
        index 1 = description
        index 2 = cost_amount
        index 3 = expense_date
        index 4 = created_at
        index 5 = entered_by_username
        index 6 = expense_id

    IMPORTANT:

        Expense ID remains available internally.

        The GUI must display only indexes 0 through 5.

        The exact username is returned at index 5.
    """

    conn = get_connection()

    cursor = conn.cursor()

    # ======================================================
    # GET MONTHLY EXPENSES WITH EXACT USERNAME
    # ======================================================

    cursor.execute(
        """
        SELECT

            e.expense_name,

            e.description,

            e.cost_amount,

            e.expense_date,

            e.created_at,

            COALESCE(
                u.username,
                'Unknown User'
            ) AS entered_by_username,

            e.expense_id

        FROM expenses e

        LEFT JOIN users u
            ON u.user_id = e.entered_by

        WHERE strftime(
            '%Y-%m',
            e.expense_date
        ) = ?

        ORDER BY
            e.expense_id DESC
        """,
        (
            month,
        )
    )

    database_rows = cursor.fetchall()

    # ======================================================
    # PREPARE REPORT ROWS
    # ======================================================

    rows = []

    for row in database_rows:

        rows.append(
            (
                row[0],  # Expense Name
                row[1],  # Description
                row[2],  # Amount
                row[3],  # Expense Date
                row[4],  # Created At
                row[5],  # Exact Username
                row[6]   # Expense ID - internal only
            )
        )

    conn.close()

    return rows


# ==========================================================
# DAILY STOCK BOOK
# ==========================================================

def get_daily_stock_report(
    report_date
):
    """
    Generates the daily stock book.

    Returns:

        (
            product_name,
            quantity_sold,
            closing_stock,
            opening_stock
        )
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            p.product_name,

            COALESCE(
                SUM(st.quantity),
                0
            ) AS sold,

            p.quantity_in_stock AS closing,

            (
                p.quantity_in_stock
                +
                COALESCE(
                    SUM(st.quantity),
                    0
                )
            ) AS opening

        FROM products p

        LEFT JOIN (

            sales_transactions st

            JOIN sales s
                ON s.sale_id = st.sale_id

                AND DATE(
                    s.date_time
                ) = ?

        )

            ON p.product_id =
               st.product_id

        GROUP BY
            p.product_id

        ORDER BY
            p.product_name
        """,
        (
            report_date,
        )
    )

    rows = cursor.fetchall()

    conn.close()

    return rows


# ==========================================================
# MONTHLY STOCK BOOK
# ==========================================================

def get_monthly_stock_report(
    month
):
    """
    Generates the monthly stock book.

    Expected month format:

        YYYY-MM
    """

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            p.product_name,

            COALESCE(
                SUM(st.quantity),
                0
            ) AS sold,

            p.quantity_in_stock AS closing,

            (
                p.quantity_in_stock
                +
                COALESCE(
                    SUM(st.quantity),
                    0
                )
            ) AS opening

        FROM products p

        LEFT JOIN (

            sales_transactions st

            JOIN sales s
                ON s.sale_id = st.sale_id

                AND strftime(
                    '%Y-%m',
                    s.date_time
                ) = ?

        )

            ON p.product_id =
               st.product_id

        GROUP BY
            p.product_id

        ORDER BY
            p.product_name
        """,
        (
            month,
        )
    )

    rows = cursor.fetchall()

    conn.close()

    return rows

