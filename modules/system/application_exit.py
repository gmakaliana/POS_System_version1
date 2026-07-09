"""
Application Exit Manager

Handles clean application shutdown.
"""

import os
import sys


from modules.backup.backup_manager import (
    create_automatic_backup
)



# ==========================================================
# CLOSE APPLICATION
# ==========================================================

def close_application(
        window
):

    """
    Performs clean shutdown.

    Steps:

    1. Create automatic backup
    2. Clear active session
    3. Close application
    """



    # =====================================
    # AUTOMATIC BACKUP
    # =====================================

    try:

        create_automatic_backup()


    except Exception as error:


        print(
            "Automatic backup failed:",
            error
        )



    # =====================================
    # CLEAR SESSION
    # =====================================

    try:

        from auth.session import clear_session


        clear_session()


    except Exception as error:


        print(
            "Session cleanup failed:",
            error
        )



    # =====================================
    # CLOSE GUI
    # =====================================

    window.destroy()



    # =====================================
    # EXIT PYTHON PROCESS
    # =====================================

    sys.exit()