from database.db import get_connection



# =====================================
# LOAD ALL SETTINGS
# =====================================

def get_settings():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    SELECT *
    FROM settings
    WHERE id = 1
    """)


    settings = cursor.fetchone()


    conn.close()


    return settings



# =====================================
# GET SINGLE SETTING VALUE
# =====================================

def get_setting_value(column_name):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        f"""
        SELECT {column_name}
        FROM settings
        WHERE id = 1
        """
    )


    result = cursor.fetchone()


    conn.close()


    if result:

        return result[0]


    return None



# =====================================
# UPDATE BUSINESS INFORMATION
# =====================================

def update_business_information(
        business_name,
        business_address,
        business_phone,
        business_email,
        company_logo,
        receipt_header,
        receipt_footer
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    UPDATE settings

    SET

        business_name = ?,

        business_address = ?,

        business_phone = ?,

        business_email = ?,

        company_logo = ?,

        receipt_header = ?,

        receipt_footer = ?

    WHERE id = 1

    """,
    (
        business_name,
        business_address,
        business_phone,
        business_email,
        company_logo,
        receipt_header,
        receipt_footer
    ))


    conn.commit()

    conn.close()



# =====================================
# UPDATE SALES SETTINGS
# =====================================

def update_sales_settings(receipt_number_start):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    UPDATE settings

    SET

        receipt_number_start = ?

    WHERE id = 1

    """,
    (
        receipt_number_start,
    ))


    conn.commit()

    conn.close()



# =====================================
# GET CURRENT RECEIPT NUMBER
# =====================================

def get_next_receipt_number():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    SELECT receipt_number_start

    FROM settings

    WHERE id = 1
    """)


    result = cursor.fetchone()


    conn.close()


    if result:

        return result[0]


    return 1000



# =====================================
# INCREASE RECEIPT NUMBER AFTER SALE
# =====================================

def increase_receipt_number():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    UPDATE settings

    SET receipt_number_start =
        receipt_number_start + 1

    WHERE id = 1

    """)


    conn.commit()

    conn.close()

# =====================================
# GET LOW STOCK THRESHOLD
# =====================================

def get_low_stock_threshold():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT low_stock_threshold
        FROM settings
        WHERE id = 1
        """
    )


    result = cursor.fetchone()

    conn.close()


    if result:

        return result[0]


    return 5

# =====================================
# UPDATE LOW STOCK THRESHOLD
# =====================================

def update_low_stock_threshold(value):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE settings
        SET low_stock_threshold = ?
        WHERE id = 1
        """,
        (value,)
    )


    conn.commit()

    conn.close()



# =====================================
# UPDATE LAST BACKUP DATE
# =====================================

def update_last_backup(datetime_value):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    UPDATE settings

    SET last_backup_datetime = ?

    WHERE id = 1

    """,
    (
        datetime_value,
    ))


    conn.commit()

    conn.close()