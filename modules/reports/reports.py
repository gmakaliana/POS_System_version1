from database.db import get_connection


def get_daily_sales(date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sale_id, total_amount, final_amount, date_time
        FROM sales
        WHERE DATE(date_time) = ?
    """, (date,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_monthly_sales(month):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT sale_id, total_amount, final_amount, date_time
        FROM sales
        WHERE strftime('%Y-%m', date_time) = ?
    """, (month,))

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_stock_report():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product_id, product_name, quantity_in_stock
        FROM products
        ORDER BY product_name
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_daily_profit_loss(date):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            s.sale_id,
            SUM(st.quantity * (st.price - p.cost_price)) AS profit
        FROM sales s
        JOIN sales_transactions st ON s.sale_id = st.sale_id
        JOIN products p ON p.product_id = st.product_id
        WHERE DATE(s.date_time) = ?
        GROUP BY s.sale_id
    """, (date,))

    rows = cursor.fetchall()
    conn.close()

    total = sum(r[1] or 0 for r in rows)
    return rows, total


def get_monthly_profit_loss(month):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT 
            s.sale_id,
            SUM(st.quantity * (st.price - p.cost_price)) AS profit
        FROM sales s
        JOIN sales_transactions st ON s.sale_id = st.sale_id
        JOIN products p ON p.product_id = st.product_id
        WHERE strftime('%Y-%m', s.date_time) = ?
        GROUP BY s.sale_id
    """, (month,))

    rows = cursor.fetchall()
    conn.close()

    total = sum(r[1] or 0 for r in rows)
    return rows, total