"""
Application Path Manager

Responsible for managing all user data locations.

The application executable should remain unchanged.
All changing data is stored outside the program folder.

Compatible with:
- Python development environment
- PyInstaller executable
- Windows desktop installation
"""

from pathlib import Path
import ctypes
from uuid import UUID


# ==========================================================
# APPLICATION SETTINGS
# ==========================================================

APP_NAME = "POS System"


# ==========================================================
# WINDOWS DOCUMENTS DIRECTORY
# ==========================================================

def get_documents_directory():
    """
    Returns the actual Windows Documents folder.

    Uses Windows Known Folder API so it works with:
    - OneDrive redirected Documents
    - Custom Documents locations
    - Different Windows configurations

    Falls back to the default Documents folder.
    """

    try:

        class GUID(ctypes.Structure):
            _fields_ = [
                ("Data1", ctypes.c_ulong),
                ("Data2", ctypes.c_ushort),
                ("Data3", ctypes.c_ushort),
                ("Data4", ctypes.c_ubyte * 8)
            ]


        folder_guid = UUID(
            "FDD39AD0-238F-46AF-ADB4-6C85480369C7"
        )


        guid = GUID(
            folder_guid.fields[0],
            folder_guid.fields[1],
            folder_guid.fields[2],
            (ctypes.c_ubyte * 8)(
                *folder_guid.bytes[8:]
            )
        )


        path_pointer = ctypes.c_wchar_p()


        result = ctypes.windll.shell32.SHGetKnownFolderPath(
            ctypes.byref(guid),
            0,
            None,
            ctypes.byref(path_pointer)
        )


        if result != 0:
            raise Exception(
                "Unable to locate Documents folder"
            )


        documents = Path(
            path_pointer.value
        )


        ctypes.windll.ole32.CoTaskMemFree(
            path_pointer
        )


        return documents


    except Exception:

        return (
            Path.home()
            /
            "Documents"
        )


# ==========================================================
# APPLICATION ROOT DIRECTORY
# ==========================================================

def get_application_directory():
    """
    Returns:

    Documents
        |
        POS System
    """

    return (
        get_documents_directory()
        /
        APP_NAME
    )


# ==========================================================
# APPLICATION DATA DIRECTORIES
# ==========================================================

def get_database_path():

    return (
        get_application_directory()
        /
        "pos.db"
    )


def get_backup_directory():

    return (
        get_application_directory()
        /
        "backups"
    )


def get_receipts_directory():

    return (
        get_application_directory()
        /
        "receipts"
    )

def get_reports_directory():

    return (
        get_application_directory()
        /
        "reports"
    )

def get_logs_directory():

    return (
        get_application_directory()
        /
        "logs"
    )

def get_audit_directory():

    return (
        get_application_directory()
        /
        "audit_logs"
    )

def get_settings_path():

    return (
        get_application_directory()
        /
        "settings.json"
    )


# ==========================================================
# INITIALIZE APPLICATION STORAGE
# ==========================================================

def initialize_application_directories():
    """
    Creates all required application folders.

    Safe to run every time the program starts.
    """


    application_directory = (
        get_application_directory()
    )


    backup_directory = (
        get_backup_directory()
    )


    receipts_directory = (
        get_receipts_directory()
    )

    reports_directory = (
        get_reports_directory()
    )

    logs_directory = (
        get_logs_directory()
    )

    audit_directory = (
        get_audit_directory()
    )

    application_directory.mkdir(
        parents=True,
        exist_ok=True
    )


    backup_directory.mkdir(
        exist_ok=True
    )


    receipts_directory.mkdir(
        exist_ok=True
    )

    reports_directory.mkdir(
        exist_ok=True
    )

    logs_directory.mkdir(
        exist_ok=True
    )

    audit_directory.mkdir(
        exist_ok=True
    )

    