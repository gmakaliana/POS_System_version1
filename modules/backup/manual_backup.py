"""
Manual Backup Manager

Handles:
- User selected backup destination
- USB/external/network backup
- Destination validation
- Duplicate filename protection
"""


import shutil

from datetime import datetime
from pathlib import Path


from modules.system.app_paths import (
    get_database_path
)

from modules.audit.audit_logs import log_activity


# ==========================================================
# CREATE MANUAL BACKUP NAME
# ==========================================================

def create_manual_backup_filename():

    """
    Creates timestamped backup name.

    Example:

    POS_Backup_2026-07-09_16-30-20.db
    """


    now = datetime.now()


    timestamp = now.strftime(
        "%Y-%m-%d_%H-%M-%S"
    )


    return (
        f"POS_Backup_{timestamp}.db"
    )



# ==========================================================
# CHECK DESTINATION WRITABILITY
# ==========================================================

def validate_backup_destination(
        destination_folder
):

    """
    Checks whether the selected folder
    can accept backup files.
    """


    try:

        destination_folder.mkdir(
            parents=True,
            exist_ok=True
        )


        test_file = (
            destination_folder
            /
            ".pos_backup_test"
        )


        with open(
            test_file,
            "w"
        ) as file:

            file.write(
                "test"
            )


        test_file.unlink()



        return True



    except Exception:


        return False



# ==========================================================
# CREATE UNIQUE BACKUP PATH
# ==========================================================

def create_unique_backup_path(
        destination_folder
):

    """
    Prevents overwriting existing backups.
    """


    backup_file = (

        destination_folder
        /
        create_manual_backup_filename()

    )


    counter = 1



    while backup_file.exists():


        backup_file = (

            destination_folder
            /
            f"POS_Backup_{counter}.db"

        )


        counter += 1



    return backup_file



# ==========================================================
# CREATE MANUAL BACKUP
# ==========================================================

def create_manual_backup(
        destination
):

    """
    Creates a manual database backup.

    Destination examples:

    USB:
        E:\\

    External drive:
        F:\\POS Backup

    Network:
        \\\\SERVER\\POS_BACKUPS
    """



    database_file = (
        get_database_path()
    )



    # Database missing

    if not database_file.exists():

        return None



    destination_folder = Path(
        destination
    )



    # Validate destination

    if not validate_backup_destination(
        destination_folder
    ):


        raise PermissionError(

            "Backup destination is not writable."

        )



    # Create unique filename

    backup_file = create_unique_backup_path(
        destination_folder
    )



    shutil.copy2(

        database_file,

        backup_file

    )

    log_activity(
        module="BACKUP",
        action="CREATE",
        description="Backup created"
    )

    return backup_file