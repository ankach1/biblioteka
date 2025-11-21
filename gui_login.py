import tkinter as tk
from tkinter import messagebox
from db import get_connection
from utils import hash_password
import gui_main
import gui_admin

def show_login():
    root = tk.Tk()
    root.title("Logowanie - Wypożyczalnia")
    root.geometry("350x250")
    root.minsize(300, 220)   # <<< MINIMALNY ROZMIAR OKNA
    root.configure(bg="#eceff1")

    tk.Label(root, text="Wypożyczalnia książek", font=("Helvetica", 14, 'bold'), bg="#eceff1").pack(pady=10)

    frame = tk.Frame(root, bg="#eceff1")
    frame.pack(pady=5)

    tk.Label(frame, text="Login:", bg="#eceff1").grid(row=0, column=0, sticky="e", pady=5, padx=5)
    entry_user = tk.Entry(frame, width=25)
    entry_user.grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Hasło:", bg="#eceff1").grid(row=1, column=0, sticky="e", pady=5, padx=5)
    entry_pass = tk.Entry(frame, show="*", width=25)
    entry_pass.grid(row=1, column=1, pady=5)

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

    btn_frame = tk.Frame(root, bg="#eceff1")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Zaloguj", bg="#4caf50", fg="white", width=12, command=login).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Rejestruj", bg="#2196f3", fg="white", width=12, command=register).pack(side="left", padx=5)

    root.mainloop()
