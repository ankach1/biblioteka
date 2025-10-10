import tkinter as tk
from tkinter import messagebox
from db import get_connection

def show_admin():
    root = tk.Tk()
    root.title("Panel administratora")
    root.geometry("600x400")

    # sekcja dodawania zasobu
    tk.Label(root, text="Dodaj nową pozycję:", font=("Arial", 12)).pack(pady=5)
    entry_title = tk.Entry(root, width=40)
    entry_author = tk.Entry(root, width=40)
    entry_title.pack()
    entry_author.pack()

    def add_item():
        title = entry_title.get()
        author = entry_author.get()
        if not title:
            messagebox.showerror("Błąd", "Tytuł jest wymagany!")
            return
        conn = get_connection()
        c = conn.cursor()
        c.execute("INSERT INTO items(title, author) VALUES (?, ?)", (title, author))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukces", "Dodano nową pozycję!")

    tk.Button(root, text="Dodaj pozycję", command=add_item).pack(pady=10)

    # sekcja użytkowników
    tk.Label(root, text="Lista użytkowników:", font=("Arial", 12)).pack(pady=10)
    listbox = tk.Listbox(root, width=60)
    listbox.pack()

    def load_users():
        listbox.delete(0, tk.END)
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, username, role FROM users")
        for row in c.fetchall():
            listbox.insert(tk.END, f"{row[0]}. {row[1]} [{row[2]}]")
        conn.close()

    def make_admin():
        selection = listbox.curselection()
        if not selection:
            messagebox.showerror("Błąd", "Wybierz użytkownika!")
            return
        user_id = listbox.get(selection[0]).split(".")[0]
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE users SET role='admin' WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukces", "Nadano uprawnienia administratora.")
        load_users()

    tk.Button(root, text="Odśwież użytkowników", command=load_users).pack()
    tk.Button(root, text="Nadaj rolę admina", command=make_admin).pack()

    load_users()
    root.mainloop()
