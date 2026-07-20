"""
Automatic Backup Manager

Handles:
- Automatic database backup
- Backup retention
- Removing old backups
- Backup settings
- Last backup date/time tracking
"""

import shutil

from datetime import datetime
from pathlib import Path


from modules.system.app_paths import (
    get_database_path,
    get_backup_directory
)


from modules.settings.settings import (
    get_backup_settings,
    update_last_backup_datetime
)

from modules.audit.audit_logs import log_activity

# ==========================================================
# CREATE BACKUP FILE NAME
# ==========================================================

def create_backup_filename():

    """
    Creates timestamped backup name.

    Example:

    backup_2026-07-09_21-30-00.db
    """


    now = datetime.now()


    timestamp = now.strftime(
        "%Y-%m-%d_%H-%M-%S"
    )


    return (
        f"backup_{timestamp}.db"
    )



# ==========================================================
# GET BACKUP LOCATION
# ==========================================================

def get_automatic_backup_location():

    """
    Returns automatic backup location.

    Uses saved location from settings.

    If no location exists,
    uses default POS backup folder.
    """


    settings = get_backup_settings()


    if settings:

        location = settings["backup_location"]


        if location:

            return Path(
                location
            )


    return get_backup_directory()



# ==========================================================
# GET BACKUP RETENTION COUNT
# ==========================================================

def get_backup_keep_count():

    """
    Returns number of backups to keep.
    """


    settings = get_backup_settings()


    if settings:

        keep_count = settings["backup_keep_count"]


        if keep_count:

            return int(
                keep_count
            )


    # Default

    return 10



# ==========================================================
# CHECK AUTOMATIC BACKUP STATUS
# ==========================================================

def is_automatic_backup_enabled():

    """
    Checks whether automatic backup
    is enabled.
    """


    settings = get_backup_settings()


    if settings:

        return (
            settings["automatic_backup_enabled"]
            == 1
        )


    # Default enabled

    return True



# ==========================================================
# CREATE AUTOMATIC BACKUP
# ==========================================================

def create_automatic_backup():

    """
    Creates automatic database backup.

    Runs during clean application exit.
    """


    # Check if user disabled backup

    if not is_automatic_backup_enabled():

        return None



    database_file = (
        get_database_path()
    )


    # Database does not exist

    if not database_file.exists():

        return None



    backup_folder = (
        get_automatic_backup_location()
    )



    backup_folder.mkdir(
        parents=True,
        exist_ok=True
    )



    backup_file = (

        backup_folder
        /
        create_backup_filename()

    )



    shutil.copy2(

        database_file,

        backup_file

    )

    log_activity(
        module="BACKUP",
        action="CREATE",
        description="Automatic database backup created"
    )



    # Update last backup time

    update_last_backup_datetime(

        datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    )



    delete_old_backups()



    return backup_file



# ==========================================================
# DELETE OLD BACKUPS
# ==========================================================

def delete_old_backups():

    """
    Keeps only the latest number
    of backups defined by user.
    """


    backup_folder = (
        get_automatic_backup_location()
    )


    keep_count = (
        get_backup_keep_count()
    )


    backups = list(

        backup_folder.glob(
            "backup_*.db"
        )

    )



    backups.sort(

        key=lambda file:
        file.stat().st_mtime,

        reverse=True

    )



    old_backups = (

        backups[keep_count:]

    )



    for backup in old_backups:


        backup.unlink()



# ==========================================================
# GET AVAILABLE BACKUPS
# ==========================================================

def get_backup_files():

    """
    Returns available automatic backups.
    """


    backup_folder = (
        get_automatic_backup_location()
    )


    backups = list(

        backup_folder.glob(
            "backup_*.db"
        )

    )



    backups.sort(

        key=lambda file:
        file.stat().st_mtime,

        reverse=True

    )



    return backups