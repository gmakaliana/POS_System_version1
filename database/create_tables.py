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
    # DEFAULT ADMIN
    # =====================================

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        ("admin",)
    )


    if not cursor.fetchone():

        cursor.execute("""
        INSERT INTO users (

            username,

            password_hash,

            role,

            must_change_password,

            created_at

        )

        VALUES (?, ?, ?, ?, ?)

        """,
        (
            "admin",

            hash_password("admin123"),

            "Admin",

            1,

            datetime.now().strftime("%Y-%m-%d %H:%M:%S")

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


        FOREIGN KEY (sale_id)

        REFERENCES sales(sale_id),


        FOREIGN KEY (product_id)

        REFERENCES products(product_id)

    )
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


        company_logo TEXT DEFAULT '',


        receipt_header TEXT DEFAULT '',


        receipt_footer TEXT DEFAULT '',


        receipt_number_start INTEGER DEFAULT 1000,

        low_stock_threshold INTEGER DEFAULT 5,


        installed_datetime TEXT,


        last_backup_datetime TEXT DEFAULT NULL

    )
    """)

    conn.commit()



    # =====================================
    # DEFAULT SETTINGS RECORD
    # =====================================

    cursor.execute(
        "SELECT id FROM settings WHERE id = 1"
    )


    if not cursor.fetchone():


        cursor.execute("""
        INSERT INTO settings (

            id,

            business_name,

            business_address,

            business_phone,

            business_email,

            company_logo,

            receipt_header,

            receipt_footer,

            receipt_number_start,

            low_stock_threshold,

            installed_datetime,

            last_backup_datetime

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """,

        (

            1,

            "Supermarket",

            "Maseru 100",

            "+266 53239121",

            "business@gmail.com",

            "",

            "POS Receipt",

            "Thank You For Shopping With Us!",

            1000,

            5,

            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

            None

        ))


        conn.commit()



    conn.close()