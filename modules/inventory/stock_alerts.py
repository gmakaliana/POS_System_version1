from tkinter import messagebox
from database.db import get_connection


# -----------------------------------
# LOW STOCK LIMIT
# -----------------------------------
LOW_STOCK_LIMIT = 5


# -----------------------------------
# GET LOW STOCK PRODUCTS
# (For popup alert)
# -----------------------------------
def get_low_stock_products():
    """
    Returns:
        product_id,
        product_name,
        quantity_in_stock
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            product_id,
            product_name,
            quantity_in_stock
        FROM products
        WHERE quantity_in_stock <= ?
        ORDER BY
            quantity_in_stock ASC,
            product_name ASC
    """, (LOW_STOCK_LIMIT,))

    products = cursor.fetchall()

    conn.close()

    return products


# -----------------------------------
# GET LOW STOCK PRODUCT DETAILS
# (For Low Stock Window)
# -----------------------------------
def get_low_stock_product_details():
    """
    Returns complete information required by
    the Low Stock Products window.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            p.product_id,
            p.product_name,
            p.barcode,
            p.cost_price,
            p.selling_price,
            p.quantity_in_stock,
            s.supplier_name
        FROM products p

        LEFT JOIN suppliers s
            ON p.supplier_id = s.supplier_id

        WHERE p.quantity_in_stock <= ?

        ORDER BY
            p.quantity_in_stock ASC,
            p.product_name ASC
    """, (LOW_STOCK_LIMIT,))

    products = cursor.fetchall()

    conn.close()

    return products


# -----------------------------------
# SHOW LOW STOCK ALERT
# -----------------------------------
def show_low_stock_alert():
    """
    Displays a warning message listing
    all low-stock products.
    """

    products = get_low_stock_products()

    if not products:
        return

    message = "The following products need restocking:\n\n"

    for product in products:

        product_name = product[1]
        quantity = product[2]

        message += f"• {product_name} ({quantity} left)\n"

    messagebox.showwarning(
        "Low Stock Alert",
        message
    )


# -----------------------------------
# CHECK IF LOW STOCK EXISTS
# -----------------------------------
def has_low_stock_products():
    """
    Returns True if there are products
    below the stock limit.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM products
        WHERE quantity_in_stock <= ?
    """, (LOW_STOCK_LIMIT,))

    count = cursor.fetchone()[0]

    conn.close()

    return count > 0