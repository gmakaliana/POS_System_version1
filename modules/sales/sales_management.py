from database.db import get_connection


def process_sale(user_id, cart_items, discount=0):

    """
    cart_items format (from cart.py):

    [
        {
            "product_id": 1,
            "product_name": "Bread",
            "quantity": 2,
            "unit_price": 15,
            "subtotal": 30
        }
    ]
    """

    if not cart_items:
        return False, "Cart is empty."

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # ==========================
        # BEGIN TRANSACTION (ACID)
        # ==========================
        conn.execute("BEGIN")

        # ==========================
        # CALCULATE TOTAL
        # ==========================
        total_amount = sum(
            item["quantity"] * item["unit_price"]
            for item in cart_items
        )

        final_amount = total_amount - discount
        if final_amount < 0:
            final_amount = 0

        # ==========================
        # INSERT SALE HEADER
        # ==========================
        cursor.execute("""
            INSERT INTO sales (
                user_id,
                total_amount,
                discount,
                final_amount
            )
            VALUES (?, ?, ?, ?)
        """, (
            user_id,
            total_amount,
            discount,
            final_amount
        ))

        sale_id = cursor.lastrowid

        # ==========================
        # PROCESS EACH CART ITEM
        # ==========================
        for item in cart_items:

            product_id = item["product_id"]
            quantity = item["quantity"]
            unit_price = item["unit_price"]

            # --------------------------------
            # CHECK STOCK
            # --------------------------------
            cursor.execute("""
                SELECT quantity_in_stock
                FROM products
                WHERE product_id = ?
            """, (product_id,))

            result = cursor.fetchone()

            if not result:
                raise Exception(f"Product {product_id} not found.")

            current_stock = result[0]

            if current_stock < quantity:
                raise Exception(
                    f"Insufficient stock for product ID {product_id}"
                )

            # --------------------------------
            # INSERT TRANSACTION
            # --------------------------------
            cursor.execute("""
                INSERT INTO sales_transactions (
                    sale_id,
                    product_id,
                    quantity,
                    price
                )
                VALUES (?, ?, ?, ?)
            """, (
                sale_id,
                product_id,
                quantity,
                unit_price
            ))

            # --------------------------------
            # DEDUCT STOCK
            # --------------------------------
            cursor.execute("""
                UPDATE products
                SET quantity_in_stock = quantity_in_stock - ?
                WHERE product_id = ?
            """, (
                quantity,
                product_id
            ))

        # ==========================
        # COMMIT TRANSACTION
        # ==========================
        conn.commit()

        return True, sale_id

    except Exception as e:

        # ==========================
        # ROLLBACK ON FAILURE
        # ==========================
        conn.rollback()

        return False, str(e)

    finally:
        conn.close()