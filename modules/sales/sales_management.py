"""
GeoMaka POS Sales Management

File:
modules/sales/sales_management.py

Purpose:
Process POS sales transactions.

Responsibilities:

- Validate sale information.
- Validate cart products.
- Calculate sale totals.
- Apply discounts.
- Check product stock.
- Create sale records.
- Create sale transaction records.
- Deduct stock.
- Commit sales using an ACID transaction.
- Record completed sales in the audit log.
- Never fail an already-completed sale because of an
  audit logging failure.

Company:
GeoMaka Technologies
"""

from database.db import get_connection

from modules.audit.audit_logs import (
    log_activity
)

from utils.validation import (
    validate_quantity,
    validate_price,
    validate_id,
    validate_discount
)


# ==========================================================
# PROCESS SALE
# ==========================================================

def process_sale(
    user_id,
    cart_items,
    discount=0
):
    """
    Processes a complete POS sale.

    cart_items format:

    [
        {
            "product_id": 1,
            "product_name": "Bread",
            "quantity": 2,
            "unit_price": 15,
            "subtotal": 30
        }
    ]

    Returns:

        (True, sale_id)

    when the sale is successfully committed.

    Returns:

        (False, error_message)

    when the sale transaction fails before commitment.

    IMPORTANT:

    Once the sale transaction has been committed,
    an audit-log failure will NOT cause this function
    to report the sale as failed.
    """

    # ======================================================
    # VALIDATE CART
    # ======================================================

    if not cart_items:

        return (
            False,
            "Cart is empty."
        )


    # ======================================================
    # VALIDATE USER ID
    # ======================================================

    valid, message = validate_id(
        user_id,
        "User ID"
    )


    if not valid:

        return (
            False,
            message
        )


    # ======================================================
    # VALIDATE DISCOUNT
    # ======================================================

    valid, message = validate_discount(
        discount
    )


    if not valid:

        return (
            False,
            message
        )


    # ======================================================
    # VALIDATE CART ITEMS
    # ======================================================

    for item in cart_items:

        # --------------------------------------------------
        # PRODUCT ID
        # --------------------------------------------------

        valid, message = validate_id(
            item["product_id"],
            "Product ID"
        )


        if not valid:

            return (
                False,
                message
            )


        # --------------------------------------------------
        # QUANTITY
        # --------------------------------------------------

        valid, message = validate_quantity(
            item["quantity"]
        )


        if not valid:

            return (
                False,
                message
            )


        # --------------------------------------------------
        # UNIT PRICE
        # --------------------------------------------------

        valid, message = validate_price(
            item["unit_price"]
        )


        if not valid:

            return (
                False,
                message
            )


    # ======================================================
    # DATABASE CONNECTION
    # ======================================================

    conn = get_connection()


    try:

        cursor = conn.cursor()


        # ==================================================
        # BEGIN TRANSACTION
        # ==================================================

        conn.execute(
            "BEGIN"
        )


        # ==================================================
        # CALCULATE TOTAL AMOUNT
        # ==================================================

        total_amount = sum(

            item["quantity"]
            *
            item["unit_price"]

            for item in cart_items

        )


        # ==================================================
        # NORMALIZE DISCOUNT
        # ==================================================

        if discount < 0:

            discount = 0


        if discount > total_amount:

            discount = total_amount


        final_amount = (
            total_amount
            -
            discount
        )


        # ==================================================
        # INSERT SALE HEADER
        # ==================================================

        cursor.execute(
            """
            INSERT INTO sales (
                user_id,
                total_amount,
                discount,
                final_amount
            )

            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                total_amount,
                discount,
                final_amount
            )
        )


        # ==================================================
        # GET SALE ID
        # ==================================================

        sale_id = cursor.lastrowid


        # ==================================================
        # DISCOUNT DISTRIBUTION
        # ==================================================

        discount_ratio = (

            discount / total_amount

            if total_amount > 0

            else 0

        )


        allocated_discount = 0


        # ==================================================
        # PROCESS CART ITEMS
        # ==================================================

        for index, item in enumerate(
            cart_items
        ):

            product_id = item[
                "product_id"
            ]

            quantity = item[
                "quantity"
            ]

            unit_price = item[
                "unit_price"
            ]


            # --------------------------------------------------
            # CALCULATE LINE TOTAL
            # --------------------------------------------------

            line_total = (
                quantity
                *
                unit_price
            )


            # --------------------------------------------------
            # ALLOCATE DISCOUNT
            # --------------------------------------------------

            if index == (
                len(cart_items) - 1
            ):

                line_discount = round(

                    discount
                    -
                    allocated_discount,

                    2

                )

            else:

                line_discount = round(

                    line_total
                    *
                    discount_ratio,

                    2

                )

                allocated_discount += (
                    line_discount
                )


            # --------------------------------------------------
            # CHECK PRODUCT STOCK
            # --------------------------------------------------

            cursor.execute(
                """
                SELECT quantity_in_stock

                FROM products

                WHERE product_id = ?
                """,
                (
                    product_id,
                )
            )


            result = cursor.fetchone()


            if not result:

                raise Exception(
                    f"Product {product_id} not found."
                )


            current_stock = result[0]


            # --------------------------------------------------
            # CHECK AVAILABLE STOCK
            # --------------------------------------------------

            if current_stock < quantity:

                raise Exception(
                    (
                        f"Insufficient stock for "
                        f"product ID {product_id}"
                    )
                )


            # --------------------------------------------------
            # INSERT SALE TRANSACTION
            # --------------------------------------------------

            cursor.execute(
                """
                INSERT INTO sales_transactions (
                    sale_id,
                    product_id,
                    quantity,
                    price,
                    discount
                )

                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    sale_id,
                    product_id,
                    quantity,
                    unit_price,
                    line_discount
                )
            )


            # --------------------------------------------------
            # DEDUCT STOCK
            # --------------------------------------------------

            cursor.execute(
                """
                UPDATE products

                SET quantity_in_stock =
                    quantity_in_stock - ?

                WHERE product_id = ?
                """,
                (
                    quantity,
                    product_id
                )
            )


        # ==================================================
        # COMMIT SALE TRANSACTION
        # ==================================================

        conn.commit()


    except Exception as error:

        # ==================================================
        # ROLLBACK SALE TRANSACTION
        # ==================================================

        try:

            conn.rollback()

        except Exception:

            pass


        return (
            False,
            str(error)
        )


    finally:

        # ==================================================
        # CLOSE SALE DATABASE CONNECTION
        # ==================================================

        conn.close()


    # ======================================================
    # AUDIT COMPLETED SALE
    # ======================================================
    #
    # The sale has already been committed.
    #
    # The audit description is intentionally short.
    #
    # ======================================================

    try:

        log_activity(

            module="SALES",

            action="COMPLETE",

            description="Sale completed"

        )


    except Exception:

        # ==================================================
        # AUDIT FAILURE IS NON-FATAL
        # ==================================================
        #
        # The sale has already been committed.
        #
        # Do NOT:
        #
        # - rollback the sale
        # - return False
        # - report the sale as failed
        #
        # ==================================================

        pass


    # ======================================================
    # SALE SUCCESS
    # ======================================================

    return (
        True,
        sale_id
    )