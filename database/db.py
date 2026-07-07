import sqlite3


DB_NAME = "pos.db"



def get_connection():

    conn = sqlite3.connect(DB_NAME)

    # Allows accessing columns by name
    # Example:
    # row["business_name"]
    conn.row_factory = sqlite3.Row


    # Enable foreign key relationships
    conn.execute(
        "PRAGMA foreign_keys = ON"
    )


    return conn