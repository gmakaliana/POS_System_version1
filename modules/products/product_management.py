from database.db import get_connection
from modules.audit.audit_logs import log_activity

# -----------------------------------
# LOW STOCK LIMIT
# -----------------------------------
LOW_STOCK_LIMIT = 5


# -----------------------------------
# GET ALL PRODUCTS
# -----------------------------------
def get_all_products():

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
            s.supplier_id,
            s.supplier_name
        FROM products p
        LEFT JOIN suppliers s
            ON p.supplier_id = s.supplier_id
        ORDER BY p.product_name
    """)

    products = cursor.fetchall()

    conn.close()

    return products


# -----------------------------------
# GET LOW STOCK PRODUCTS
# -----------------------------------
def get_low_stock_products():

    """
    Returns products whose quantity is less
    than or equal to LOW_STOCK_LIMIT.
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
            s.supplier_id,
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
# ADD PRODUCT
# -----------------------------------
def add_product(
        product_name,
        barcode,
        cost_price,
        selling_price,
        quantity,
        supplier_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO products
        (
            product_name,
            barcode,
            cost_price,
            selling_price,
            quantity_in_stock,
            supplier_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        product_name,
        barcode,
        cost_price,
        selling_price,
        quantity,
        supplier_id
    ))

    conn.commit()

    log_activity(
        module="PRODUCTS",
        action="CREATE",
        description="Product added"
    )

    conn.close()


# -----------------------------------
# UPDATE PRODUCT
# -----------------------------------
def update_product(
        product_id,
        product_name,
        barcode,
        cost_price,
        selling_price,
        quantity,
        supplier_id
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET
            product_name=?,
            barcode=?,
            cost_price=?,
            selling_price=?,
            quantity_in_stock=?,
            supplier_id=?
        WHERE product_id=?
    """, (
        product_name,
        barcode,
        cost_price,
        selling_price,
        quantity,
        supplier_id,
        product_id
    ))

    conn.commit()

    log_activity(
        module="PRODUCTS",
        action="UPDATE",
        description="Product edited"
    )

    conn.close()


# -----------------------------------
# DELETE PRODUCT
# -----------------------------------
def delete_product(product_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM products WHERE product_id=?",
        (product_id,)
    )

    conn.commit()

    log_activity(
        module="PRODUCTS",
        action="DELETE",
        description="Product deleted"
    )

    conn.close()


# -----------------------------------
# GET PRODUCT BY ID
# -----------------------------------
def get_product_by_id(product_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            product_id,
            product_name,
            barcode,
            cost_price,
            selling_price,
            quantity_in_stock
        FROM products
        WHERE product_id = ?
    """, (product_id,))

    product = cursor.fetchone()

    conn.close()

    return product


# -----------------------------------
# GET PRODUCT BY BARCODE
# -----------------------------------
def get_product_by_barcode(barcode):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            product_id,
            product_name,
            barcode,
            cost_price,
            selling_price,
            quantity_in_stock
        FROM products
        WHERE barcode = ?
    """, (barcode,))

    product = cursor.fetchone()

    conn.close()

    return product


# -----------------------------------
# SEARCH PRODUCTS
# -----------------------------------
def search_products(search_text):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            product_id,
            product_name,
            barcode,
            selling_price,
            quantity_in_stock
        FROM products
        WHERE product_name LIKE ?
        ORDER BY product_name
    """, (f"%{search_text}%",))

    products = cursor.fetchall()

    conn.close()

    return products


# -----------------------------------
# GET PRODUCT STOCK
# -----------------------------------
def get_product_stock(product_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT quantity_in_stock
        FROM products
        WHERE product_id = ?
    """, (product_id,))

    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]

    return 0


# -----------------------------------
# UPDATE PRODUCT STOCK
# -----------------------------------
def update_product_stock(product_id, quantity):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE products
        SET quantity_in_stock = ?
        WHERE product_id = ?
    """, (
        quantity,
        product_id
    ))

    conn.commit()
    conn.close()


# -----------------------------------
# CHECK STOCK AVAILABLE
# -----------------------------------
def has_sufficient_stock(product_id, quantity_needed):

    current_stock = get_product_stock(product_id)

    return current_stock >= quantity_needed