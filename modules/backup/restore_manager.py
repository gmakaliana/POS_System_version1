"""
Restore Manager

Handles:
- Database restore
- Validation of backup files
- Safety backup before restore
"""

import shutil
import sqlite3

from datetime import datetime
from pathlib import Path


from modules.system.app_paths import (
    get_database_path,
    get_backup_directory
)



# ==========================================================
# CREATE SAFETY BACKUP NAME
# ==========================================================

def create_safety_backup_filename():

    """
    Creates backup name before restore.

    Example:

    before_restore_2026-07-09_17-00-00.db
    """


    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )


    return (
        f"before_restore_{timestamp}.db"
    )



# ==========================================================
# VALIDATE BACKUP FILE
# ==========================================================

def validate_backup_file(
        backup_file
):

    """
    Checks whether selected file
    is a valid SQLite database.
    """


    backup_path = Path(
        backup_file
    )


    if not backup_path.exists():

        return False



    try:


        connection = sqlite3.connect(
            backup_path
        )


        cursor = connection.cursor()



        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            """
        )


        tables = cursor.fetchall()


        connection.close()



        # Database should contain tables

        if len(tables) == 0:

            return False



        return True



    except Exception:


        return False



# ==========================================================
# CREATE SAFETY BACKUP
# ==========================================================

def create_before_restore_backup():

    """
    Saves current database before restore.
    """


    database_file = (
        get_database_path()
    )


    if not database_file.exists():

        return None



    backup_folder = (
        get_backup_directory()
    )


    backup_folder.mkdir(
        parents=True,
        exist_ok=True
    )



    safety_backup = (

        backup_folder
        /
        create_safety_backup_filename()

    )



    shutil.copy2(

        database_file,

        safety_backup

    )



    return safety_backup



# ==========================================================
# RESTORE DATABASE
# ==========================================================

def restore_database(
        backup_file
):

    """
    Restores selected backup.

    Returns:

    True  = success
    False = failed
    """



    backup_path = Path(
        backup_file
    )



    # Validate selected backup

    if not validate_backup_file(
        backup_path
    ):

        return False



    database_file = (
        get_database_path()
    )



    try:


        # Safety backup first

        create_before_restore_backup()



        # Replace current database

        shutil.copy2(

            backup_path,

            database_file

        )



        return True



    except Exception as error:


        print(
            "Restore failed:",
            error
        )


        return False