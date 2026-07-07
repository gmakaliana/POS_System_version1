# main.py

from database.create_tables import create_tables



def initialize_system():

    create_tables()



if __name__ == "__main__":


    # =====================================
    # DATABASE INITIALIZATION FIRST
    # =====================================

    initialize_system()



    # =====================================
    # IMPORT GUI AFTER DATABASE EXISTS
    # =====================================

    from gui.login_window import create_login_window


    create_login_window()