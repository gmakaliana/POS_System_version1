"""
Database Connection Manager

Handles:
- SQLite connection
- Database location
- Migration of old database files
"""

import sqlite3
import shutil
from pathlib import Path


from modules.system.app_paths import (
    get_database_path
)


# ==========================================================
# OLD DATABASE LOCATION
# ==========================================================

def get_old_database_path():

    """
    Returns the old development database location.

    Used only during migration.
    """

    project_directory = Path(__file__).parent.parent

    return (
        project_directory
        /
        "pos.db"
    )


# ==========================================================
# DATABASE MIGRATION
# ==========================================================

def migrate_database():

    """
    Moves existing pos.db from the project folder
    into the new application data folder.

    Runs only when:
    - new location does not exist
    - old database exists
    """

    new_database = get_database_path()

    old_database = get_old_database_path()


    if new_database.exists():

        return


    if old_database.exists():

        new_database.parent.mkdir(
            parents=True,
            exist_ok=True
        )


        shutil.copy2(
            old_database,
            new_database
        )



# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    """
    Returns SQLite database connection.
    """

    migrate_database()


    database_path = (
        get_database_path()
    )


    connection = sqlite3.connect(
        database_path
    )


    connection.row_factory = sqlite3.Row


    return connection