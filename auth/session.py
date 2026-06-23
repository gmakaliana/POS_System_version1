CURRENT_USER = None


def create_session(user):
    global CURRENT_USER
    CURRENT_USER = user


def get_session_user():
    return CURRENT_USER


def clear_session():
    global CURRENT_USER
    CURRENT_USER = None