from database.db import get_connection
from modules.audit.audit_logs import log_activity

from utils.validation import (
    validate_business_name,
    validate_address,
    validate_phone,
    validate_email,
    validate_receipt_text,
    validate_receipt_number,
    validate_threshold,
    validate_backup_keep_count,
    validate_report_time
)


# =====================================
# ALLOWED SETTINGS COLUMNS
# =====================================

ALLOWED_SETTINGS = {

    "business_name",

    "business_address",

    "business_phone",

    "business_email",

    "receipt_header",

    "receipt_footer",

    "receipt_number_start",

    "low_stock_threshold",

    "last_backup_datetime",

    "automatic_backup_enabled",

    "backup_location",

    "backup_keep_count",

    "automatic_daily_report_enabled",

    "daily_report_time",

    "automatic_monthly_report_enabled",

    "monthly_report_time",

    "last_daily_report_date",

    "last_monthly_report_month",

    "installed_datetime"

}

# =====================================
# VALIDATE BUSINESS INFORMATION
# =====================================

def validate_business_information(
        business_name,
        business_address,
        business_phone,
        business_email,
        receipt_header,
        receipt_footer
):

    checks = [

        validate_business_name(business_name),

        validate_address(business_address),

        validate_phone(business_phone),

        validate_email(business_email),

        validate_receipt_text(receipt_header),

        validate_receipt_text(receipt_footer)

    ]

    for valid, message in checks:

        if not valid:

            raise Exception(message)

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


    if column_name not in ALLOWED_SETTINGS:

        raise ValueError(
            "Invalid settings field."
        )


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
        receipt_header,
        receipt_footer
):
    
    validate_business_information(
        business_name,
        business_address,
        business_phone,
        business_email,
        receipt_header,
        receipt_footer
    )

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    UPDATE settings

    SET

        business_name = ?,

        business_address = ?,

        business_phone = ?,

        business_email = ?,

        receipt_header = ?,

        receipt_footer = ?

    WHERE id = 1

    """,
    (
        business_name,
        business_address,
        business_phone,
        business_email,
        receipt_header,
        receipt_footer
    ))


    conn.commit()

    log_activity(
        module="SETTINGS",
        action="UPDATE",
        description="Business information updated"
    )

    conn.close()



# =====================================
# UPDATE SALES SETTINGS
# =====================================

def update_sales_settings(receipt_number_start):

    valid, message = validate_receipt_number(
        receipt_number_start
    )

    if not valid:

        raise Exception(message)

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

    log_activity(
        module="SETTINGS",
        action="UPDATE",
        description="Receipt number start changed"
    )

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

    valid, message = validate_threshold(value)

    if not valid:

        raise Exception(message)

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


    cursor.execute(
        """
        UPDATE settings

        SET last_backup_datetime = ?

        WHERE id = 1

        """,
        (
            datetime_value,
        )
    )


    conn.commit()

    conn.close()



# =====================================
# BACKUP SETTINGS
# =====================================

def get_backup_settings():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        SELECT

        automatic_backup_enabled,

        last_backup_datetime,

        backup_location,

        backup_keep_count

        FROM settings

        WHERE id = 1
        """
    )


    result = cursor.fetchone()


    conn.close()


    return result



# =====================================
# UPDATE BACKUP SETTINGS
# =====================================

def update_backup_settings(
        enabled,
        backup_location,
        keep_count
):

    valid, message = validate_backup_keep_count(
        keep_count
    )

    if not valid:

        raise Exception(message)
    
    if enabled not in (0, 1):

        raise Exception(
            "Invalid backup setting."
        )

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE settings

        SET

        automatic_backup_enabled = ?,

        backup_location = ?,

        backup_keep_count = ?

        WHERE id = 1

        """,

        (
            enabled,
            backup_location,
            keep_count
        )
    )


    conn.commit()

    log_activity(
        module="SETTINGS",
        action="UPDATE",
        description="Backup settings changed"
    )

    conn.close()



# =====================================
# UPDATE LAST AUTOMATIC BACKUP DATETIME
# =====================================

def update_last_backup_datetime(
        datetime_value
):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute(
        """
        UPDATE settings

        SET last_backup_datetime = ?

        WHERE id = 1

        """,

        (
            datetime_value,
        )
    )


    conn.commit()

    conn.close()

# =====================================
# REPORT SCHEDULER SETTINGS
# =====================================


def get_report_scheduler_settings():

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    SELECT

        automatic_daily_report_enabled,

        daily_report_time,

        automatic_monthly_report_enabled,

        monthly_report_time,

        last_daily_report_date,

        last_monthly_report_month

    FROM settings

    WHERE id = 1

    """)


    result = cursor.fetchone()


    conn.close()


    return result



def update_report_scheduler_settings(
        daily_enabled,
        daily_time,
        monthly_enabled,
        monthly_time
):

    if daily_enabled not in (0, 1):

        raise Exception(
            "Invalid daily report setting."
        )

    if monthly_enabled not in (0, 1):

        raise Exception(
            "Invalid monthly report setting."
        )

    valid, message = validate_report_time(
        daily_time
    )

    if not valid:

        raise Exception(message)


    valid, message = validate_report_time(
        monthly_time
    )

    if not valid:

        raise Exception(message)

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    UPDATE settings

    SET

    automatic_daily_report_enabled = ?,

    daily_report_time = ?,

    automatic_monthly_report_enabled = ?,

    monthly_report_time = ?

    WHERE id = 1

    """,
    (
        daily_enabled,
        daily_time,
        monthly_enabled,
        monthly_time
    ))


    conn.commit()

    log_activity(
        module="SETTINGS",
        action="UPDATE",
        description="Report settings changed"
    )

    conn.close()



def update_last_daily_report_date(report_date):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    UPDATE settings

    SET last_daily_report_date = ?

    WHERE id = 1

    """,
    (
        report_date,
    ))


    conn.commit()

    conn.close()



def update_last_monthly_report_month(month):

    conn = get_connection()

    cursor = conn.cursor()


    cursor.execute("""
    UPDATE settings

    SET last_monthly_report_month = ?

    WHERE id = 1

    """,
    (
        month,
    ))


    conn.commit()

    conn.close()