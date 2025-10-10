import tkinter as tk
from tkinter import messagebox
from db import get_connection
from utils import hash_password
import gui_main
import gui_admin

def show_login():
    root = tk.Tk()
    root.title("Logowanie - Wypożyczalnia")
    root.geometry("300x200")
    root.resizable(True, True)

    tk.Label(root, text="Login:").pack(pady=5)
    entry_user = tk.Entry(root)
    entry_user.pack()

    tk.Label(root, text="Hasło:").pack(pady=5)
    entry_pass = tk.Entry(root, show="*")
    entry_pass.pack()

    def login():
        user = entry_user.get()
        pw = hash_password(entry_pass.get())

        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT username, role FROM users WHERE username=? AND password=?", (user, pw))
        result = c.fetchone()
        conn.close()

        if result:
            messagebox.showinfo("Sukces", f"Witaj {user}!")
            root.destroy()
            if result[1] == "admin":
                gui_admin.show_admin()
            else:
                gui_main.show_main(user)
        else:
            messagebox.showerror("Błąd", "Niepoprawny login lub hasło!")

    def register():
        user = entry_user.get()
        pw = hash_password(entry_pass.get())

        if not user or not pw:
            messagebox.showerror("Błąd", "Uzupełnij wszystkie pola!")
            return

        conn = get_connection()
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users(username, password) VALUES (?, ?)", (user, pw))
            conn.commit()
            messagebox.showinfo("Sukces", "Użytkownik zarejestrowany!")
        except Exception as e:
            messagebox.showerror("Błąd", f"Rejestracja nieudana: {e}")
        finally:
            conn.close()

    tk.Button(root, text="Zaloguj", command=login).pack(pady=10)
    tk.Button(root, text="Rejestruj", command=register).pack()

    root.mainloop()
.