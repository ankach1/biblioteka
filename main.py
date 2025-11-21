import gui_login
from db import init_db
init_db()

if __name__ == "__main__":
    gui_login.show_login()
