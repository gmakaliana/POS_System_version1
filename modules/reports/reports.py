from database.db import get_connection


# ==========================================================
# DAILY SALES REPORT
# ==========================================================
def get_daily_sales(report_date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.product_name,
            p.barcode,
            p.cost_price,
            st.price,
            SUM(st.quantity) AS qty_sold,

            SUM(st.quantity * p.cost_price) AS total_cost,

            SUM(st.quantity * st.price) AS gross_sales,

            SUM(st.discount) AS total_discount,

            SUM((st.quantity * st.price) - st.discount) AS net_sales,

            SUM(
                ((st.quantity * st.price) - st.discount)
                -
                (st.quantity * p.cost_price)
            ) AS profit

        FROM sales_transactions st

        JOIN sales s
            ON s.sale_id = st.sale_id

        JOIN products p
            ON p.product_id = st.product_id

        WHERE DATE(s.date_time) = ?

        GROUP BY p.product_id

        ORDER BY p.product_name
    """, (report_date,))

    rows = cursor.fetchall()

    summary = {

        "products": len(rows),

        "quantity": sum(r[4] or 0 for r in rows),

        "cost": sum(r[5] or 0 for r in rows),

        "gross_sales": sum(r[6] or 0 for r in rows),

        "discount": sum(r[7] or 0 for r in rows),

        "net_sales": sum(r[8] or 0 for r in rows),

        "profit": sum(r[9] or 0 for r in rows)

    }

    conn.close()

    return rows, summary


# ==========================================================
# MONTHLY SALES REPORT
# ==========================================================
def get_monthly_sales(month):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.product_name,
            p.barcode,
            p.cost_price,
            st.price,
            SUM(st.quantity) AS qty_sold,

            SUM(st.quantity * p.cost_price) AS total_cost,

            SUM(st.quantity * st.price) AS gross_sales,

            SUM(st.discount) AS total_discount,

            SUM((st.quantity * st.price) - st.discount) AS net_sales,

            SUM(
                ((st.quantity * st.price) - st.discount)
                -
                (st.quantity * p.cost_price)
            ) AS profit

        FROM sales_transactions st

        JOIN sales s
            ON s.sale_id = st.sale_id

        JOIN products p
            ON p.product_id = st.product_id

        WHERE strftime('%Y-%m', s.date_time) = ?

        GROUP BY p.product_id

        ORDER BY p.product_name
    """, (month,))

    rows = cursor.fetchall()

    summary = {

        "products": len(rows),

        "quantity": sum(r[4] or 0 for r in rows),

        "cost": sum(r[5] or 0 for r in rows),

        "gross_sales": sum(r[6] or 0 for r in rows),

        "discount": sum(r[7] or 0 for r in rows),

        "net_sales": sum(r[8] or 0 for r in rows),

        "profit": sum(r[9] or 0 for r in rows)

    }

    conn.close()

    return rows, summary


# ==========================================================
# DAILY STOCK BOOK (FIXED)
# ==========================================================
def get_daily_stock_report(report_date):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.product_name,

            COALESCE(SUM(st.quantity), 0) AS sold,

            p.quantity_in_stock AS closing,

            (
                p.quantity_in_stock
                +
                COALESCE(SUM(st.quantity), 0)
            ) AS opening

        FROM products p

        LEFT JOIN (
            sales_transactions st

            JOIN sales s
                ON s.sale_id = st.sale_id
                AND DATE(s.date_time) = ?

        )
            ON p.product_id = st.product_id


        GROUP BY p.product_id

        ORDER BY p.product_name

    """, (report_date,))


    rows = cursor.fetchall()

    conn.close()

    return rows



# ==========================================================
# MONTHLY STOCK BOOK (FIXED)
# ==========================================================
def get_monthly_stock_report(month):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.product_name,

            COALESCE(SUM(st.quantity), 0) AS sold,

            p.quantity_in_stock AS closing,

            (
                p.quantity_in_stock
                +
                COALESCE(SUM(st.quantity), 0)
            ) AS opening

        FROM products p


        LEFT JOIN (
            sales_transactions st

            JOIN sales s
                ON s.sale_id = st.sale_id
                AND strftime('%Y-%m', s.date_time) = ?

        )
            ON p.product_id = st.product_id


        GROUP BY p.product_id

        ORDER BY p.product_name

    """, (month,))


    rows = cursor.fetchall()

    conn.close()

    return rows