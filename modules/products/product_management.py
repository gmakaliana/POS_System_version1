from database.db import get_connection


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
    conn.close()