from database.db import get_connection
from auth.password_utils import hash_password
from datetime import datetime


def create_tables():

    conn = get_connection()
    cursor = conn.cursor()


    # =====================================
    # USERS TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (

        user_id INTEGER PRIMARY KEY AUTOINCREMENT,

        username TEXT UNIQUE,

        password_hash TEXT,

        role TEXT,

        must_change_password INTEGER DEFAULT 1,

        is_active INTEGER DEFAULT 1,

        created_at TEXT
    )
    """)

    conn.commit()



    # =====================================
    # USER ROLE MIGRATION
    # =====================================

    # Convert old Admin account into Default Admin
    # For existing installations

    cursor.execute("""
        SELECT user_id, role
        FROM users
        WHERE username = ?
    """,
    (
        "admin",
    ))


    old_admin = cursor.fetchone()



    if old_admin:

        if old_admin[1] == "Admin":

            cursor.execute("""
                UPDATE users
                SET role = ?
                WHERE username = ?
            """,
            (
                "Default Admin",
                "admin"
            ))

            conn.commit()



    # =====================================
    # CREATE SYSTEM ADMIN
    # =====================================

    cursor.execute("""
        SELECT user_id
        FROM users
        WHERE role = ?
    """,
    (
        "System Admin",
    ))


    system_admin = cursor.fetchone()



    if not system_admin:


        cursor.execute("""
            INSERT INTO users
            (
                username,
                password_hash,
                role,
                must_change_password,
                is_active,
                created_at
            )

            VALUES (?, ?, ?, ?, ?, ?)

        """,
        (

            "systemadmin",

            hash_password(
                "SystemAdmin@123"
            ),

            "System Admin",

            1,

            1,

            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        ))


        conn.commit()



    # =====================================
    # SUPPLIERS TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS suppliers (

        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,

        supplier_name TEXT NOT NULL,

        phone TEXT,

        address TEXT

    )
    """)

    conn.commit()



    # =====================================
    # PRODUCTS TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (

        product_id INTEGER PRIMARY KEY AUTOINCREMENT,

        product_name TEXT NOT NULL,

        barcode TEXT UNIQUE,

        cost_price REAL NOT NULL,

        selling_price REAL NOT NULL,

        quantity_in_stock INTEGER DEFAULT 0,

        supplier_id INTEGER,

        created_at TEXT DEFAULT CURRENT_TIMESTAMP,


        FOREIGN KEY (supplier_id)

        REFERENCES suppliers(supplier_id)

    )
    """)

    conn.commit()



    # =====================================
    # SALES TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (

        sale_id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER NOT NULL,

        total_amount REAL NOT NULL,

        discount REAL DEFAULT 0,

        final_amount REAL NOT NULL,

        date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


        FOREIGN KEY (user_id)

        REFERENCES users(user_id)

    )
    """)

    conn.commit()



    # =====================================
    # SALES TRANSACTIONS TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales_transactions (

        transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,

        sale_id INTEGER NOT NULL,

        product_id INTEGER NOT NULL,

        quantity INTEGER NOT NULL,

        price REAL NOT NULL,

        discount REAL DEFAULT 0,


        FOREIGN KEY (sale_id)

        REFERENCES sales(sale_id),


        FOREIGN KEY (product_id)

        REFERENCES products(product_id)

    )
    """)

    conn.commit()



    # =====================================
    # SALES TRANSACTIONS MIGRATION
    # =====================================

    cursor.execute("""
        PRAGMA table_info(sales_transactions)
    """)


    columns = [
        column[1]
        for column in cursor.fetchall()
    ]


    if "discount" not in columns:

        cursor.execute("""
            ALTER TABLE sales_transactions
            ADD COLUMN discount REAL DEFAULT 0
        """)

        conn.commit()



    # =====================================
    # SETTINGS TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (

        id INTEGER PRIMARY KEY,

        business_name TEXT DEFAULT '',

        business_address TEXT DEFAULT '',

        business_phone TEXT DEFAULT '',

        business_email TEXT DEFAULT '',

        receipt_header TEXT DEFAULT '',

        receipt_footer TEXT DEFAULT '',

        receipt_number_start INTEGER DEFAULT 1000,

        low_stock_threshold INTEGER DEFAULT 5,

        installed_datetime TEXT,

        last_backup_datetime TEXT DEFAULT NULL,

        automatic_backup_enabled INTEGER DEFAULT 1,

        backup_location TEXT,

        backup_keep_count INTEGER DEFAULT 10,


        automatic_daily_report_enabled INTEGER DEFAULT 0,

        daily_report_time TEXT DEFAULT '18:00',


        automatic_monthly_report_enabled INTEGER DEFAULT 0,

        monthly_report_time TEXT DEFAULT '18:00',


        last_daily_report_date TEXT DEFAULT NULL,

        last_monthly_report_month TEXT DEFAULT NULL

    )
    """)

    conn.commit()



    # =====================================
    # DEFAULT SETTINGS RECORD
    # =====================================

    cursor.execute("""
        SELECT id
        FROM settings
        WHERE id = 1
    """)


    if not cursor.fetchone():

        cursor.execute("""
        INSERT INTO settings (

            id,

            business_name,

            business_address,

            business_phone,

            business_email,

            receipt_header,

            receipt_footer,

            receipt_number_start,

            low_stock_threshold,

            installed_datetime,

            automatic_backup_enabled,

            backup_location,

            backup_keep_count,

            automatic_daily_report_enabled,

            daily_report_time,

            automatic_monthly_report_enabled,

            monthly_report_time,

            last_daily_report_date,

            last_monthly_report_month

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """,

        (

            1,

            "Supermarket",

            "Maseru 100",

            "+266 53239121",

            "business@gmail.com",

            "POS Receipt",

            "Thank You For Shopping With Us!",

            1000,

            5,

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            1,

            "",

            10,

            0,

            "18:00",

            0,

            "18:00",

            "",

            ""

        ))

        conn.commit()

    # =====================================
    # AUDIT LOGS TABLE
    # =====================================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (

        audit_id INTEGER PRIMARY KEY AUTOINCREMENT,

        user_id INTEGER,

        username TEXT,

        role TEXT,

        module TEXT NOT NULL,

        action TEXT NOT NULL,

        description TEXT,

        log_datetime TEXT DEFAULT CURRENT_TIMESTAMP,


        FOREIGN KEY (user_id)

        REFERENCES users(user_id)

    )
    """)

    conn.commit()



    conn.close()