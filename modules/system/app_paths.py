"""
GeoMaka POS Application Path Manager

Purpose:
    Manage all application data locations outside
    the application/source-code directory.

Company:
    GeoMaka Technologies
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
    Return the actual Windows Documents directory.

    Uses the Windows Known Folder API so that the application
    also works when Documents is redirected to OneDrive or
    another custom location.

    Falls back to:
        C:/Users/<User>/Documents
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
                "Unable to locate Documents folder."
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
            / "Documents"
        )


# ==========================================================
# APPLICATION DIRECTORY
# ==========================================================

def get_application_directory():
    """
    Return the main GeoMaka POS data directory.

    Example:

        Documents/
            POS System/
    """

    return (
        get_documents_directory()
        / APP_NAME
    )


# ==========================================================
# DATABASE
# ==========================================================

def get_database_path():
    """
    Return the SQLite database path.

    Example:

        Documents/
            POS System/
                pos.db
    """

    return (
        get_application_directory()
        / "pos.db"
    )


# ==========================================================
# BACKUPS
# ==========================================================

def get_backup_directory():
    """
    Return the database backup directory.
    """

    return (
        get_application_directory()
        / "backups"
    )


# ==========================================================
# RECEIPTS
# ==========================================================

def get_receipts_directory():
    """
    Return the receipt storage directory.
    """

    return (
        get_application_directory()
        / "receipts"
    )


# ==========================================================
# REPORTS
# ==========================================================

def get_reports_directory():
    """
    Return the reports directory.
    """

    return (
        get_application_directory()
        / "reports"
    )


# ==========================================================
# AUDIT LOGS
# ==========================================================

def get_audit_directory():
    """
    Return the audit log directory.
    """

    return (
        get_application_directory()
        / "audit_logs"
    )


# ==========================================================
# INITIALIZE APPLICATION STORAGE
# ==========================================================

def initialize_application_directories():
    """
    Create all required application data directories.

    Safe to call every time the application starts.
    """

    application_directory = (
        get_application_directory()
    )

    application_directory.mkdir(
        parents=True,
        exist_ok=True
    )

    get_backup_directory().mkdir(
        exist_ok=True
    )

    get_receipts_directory().mkdir(
        exist_ok=True
    )

    get_reports_directory().mkdir(
        exist_ok=True
    )

    get_audit_directory().mkdir(
        exist_ok=True
    )
    