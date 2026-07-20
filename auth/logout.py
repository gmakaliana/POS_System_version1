from auth.session import (
    get_session_user,
    clear_session
)

from modules.audit.audit_logs import log_activity



def logout_user():

    user = get_session_user()


    if user:

        log_activity(
            module="AUTH",
            action="LOGOUT",
            description="User logged out"
        )


    clear_session()