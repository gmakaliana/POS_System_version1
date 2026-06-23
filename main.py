# main.py

from database.create_tables import (
    create_tables,
    
)

from gui.login_window import (
    create_login_window
)


def initialize_system():

    create_tables()

    


if __name__ == "__main__":

    initialize_system()

    create_login_window()