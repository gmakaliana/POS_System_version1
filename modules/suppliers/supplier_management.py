from database.db import get_connection
from modules.audit.audit_logs import log_activity

# -----------------------------------
# GET ALL SUPPLIERS
# -----------------------------------
def get_all_suppliers():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            supplier_id,
            supplier_name,
            phone,
            address
        FROM suppliers
        ORDER BY supplier_name
    """)

    suppliers = cursor.fetchall()

    conn.close()

    return suppliers


# -----------------------------------
# ADD SUPPLIER
# -----------------------------------
def add_supplier(
        supplier_name,
        phone,
        address
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO suppliers
        (
            supplier_name,
            phone,
            address
        )
        VALUES (?, ?, ?)
    """, (
        supplier_name,
        phone,
        address
    ))

    conn.commit()

    log_activity(
        module="SUPPLIERS",
        action="CREATE",
        description="Supplier added"
    )

    conn.close()


# -----------------------------------
# UPDATE SUPPLIER
# -----------------------------------
def update_supplier(
        supplier_id,
        supplier_name,
        phone,
        address
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE suppliers
        SET
            supplier_name=?,
            phone=?,
            address=?
        WHERE supplier_id=?
    """, (
        supplier_name,
        phone,
        address,
        supplier_id
    ))

    conn.commit()

    log_activity(
        module="SUPPLIERS",
        action="UPDATE",
        description="Supplier edited"
    )

    conn.close()


# -----------------------------------
# DELETE SUPPLIER
# -----------------------------------
def delete_supplier(supplier_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM products
        WHERE supplier_id=?
    """, (supplier_id,))

    count = cursor.fetchone()[0]

    if count > 0:
        conn.close()
        raise Exception(
            "Cannot delete supplier because products are linked to it."
        )

    cursor.execute(
        "DELETE FROM suppliers WHERE supplier_id=?",
        (supplier_id,)
    )

    conn.commit()

    log_activity(
        module="SUPPLIERS",
        action="DELETE",
        description="Supplier deleted"
    )

    conn.close()