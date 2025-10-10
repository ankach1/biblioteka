from db import init_db
import gui_login

if __name__ == "__main__":
    init_db()
    gui_login.show_login()
