import sqlite3
from utils import hash_password

DB_NAME = "wypozyczalnia.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    # Tabela użytkowników
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user'
    )
    """)

    # Tabela zasobów
    c.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT,
        available INTEGER DEFAULT 1
    )
    """)

    # Tabela wypożyczeń
    c.execute("""
    CREATE TABLE IF NOT EXISTS rentals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        rent_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        return_date TIMESTAMP,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(item_id) REFERENCES items(id)
    )
    """)

    #  Dodanie konta administratora (jeśli nie istnieje)
    admin_user = "admin"
    admin_pass = hash_password("admin")
    c.execute("SELECT * FROM users WHERE username=?", (admin_user,))
    if not c.fetchone():
        c.execute(
            "INSERT INTO users(username, password, role) VALUES (?, ?, 'admin')",
            (admin_user, admin_pass)
        )
        print("✔ Utworzono domyślne konto admin (login: admin, hasło: admin)")

    #  Dodanie przykładowych książek (tylko jeśli tabela jest pusta)
    c.execute("SELECT COUNT(*) FROM items")
    if c.fetchone()[0] == 0:
        sample_books = [
            ("Pan Tadeusz", "Adam Mickiewicz"),
            ("Lalka", "Bolesław Prus"),
            ("Quo Vadis", "Henryk Sienkiewicz"),
            ("Krzyżacy", "Henryk Sienkiewicz"),
            ("Wesele", "Stanisław Wyspiański"),
            ("Ferdydurke", "Witold Gombrowicz"),
            ("Solaris", "Stanisław Lem")
        ]
        c.executemany("INSERT INTO items(title, author) VALUES (?, ?)", sample_books)
        print("✔ Dodano przykładowe polskie książki do bazy.")

    conn.commit()
    conn.close()

def get_connection():
    return sqlite3.connect(DB_NAME)
