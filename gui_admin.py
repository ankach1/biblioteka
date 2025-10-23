import tkinter as tk
from tkinter import messagebox
from db import get_connection
import gui_login

def show_admin():
    root = tk.Tk()
    root.title("Panel administratora")
    root.geometry("900x500")
    root.minsize(800, 600)  # minimalny rozmiar
    root.resizable(True, True)

    # --- Funkcje ---
    def logout():
        root.destroy()
        gui_login.show_login()

    # --- Funkcje użytkowników ---
    def load_users():
        listbox_users.delete(0, tk.END)
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, username, role FROM users")
        for row in c.fetchall():
            listbox_users.insert(tk.END, f"{row[0]}. {row[1]} [{row[2]}]")
        conn.close()

    def make_admin():
        selection = listbox_users.curselection()
        if not selection:
            messagebox.showerror("Błąd", "Wybierz użytkownika!")
            return
        user_id = listbox_users.get(selection[0]).split(".")[0]
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE users SET role='admin' WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukces", "Nadano uprawnienia administratora.")
        load_users()

    def delete_user():
        selection = listbox_users.curselection()
        if not selection:
            messagebox.showerror("Błąd", "Wybierz użytkownika!")
            return
        user_id = listbox_users.get(selection[0]).split(".")[0]
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (user_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukces", "Usunięto użytkownika.")
        load_users()

    # --- Funkcje książek ---
    def load_items():
        listbox_items.delete(0, tk.END)
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, title, author, available FROM items")
        for row in c.fetchall():
            status = "Dostępny" if row[3] == 1 else "Wypożyczony"
            listbox_items.insert(tk.END, f"{row[0]}. {row[1]} - {row[2]} [{status}]")
        conn.close()

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
        entry_title.delete(0, tk.END)
        entry_author.delete(0, tk.END)
        load_items()

    def delete_item():
        selection = listbox_items.curselection()
        if not selection:
            messagebox.showerror("Błąd", "Wybierz książkę!")
            return
        item_id = listbox_items.get(selection[0]).split(".")[0]
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM items WHERE id=?", (item_id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Sukces", "Usunięto książkę.")
        load_items()

    # --- Układ GUI ---

    # Górny frame dla dodawania książek
    frame_add = tk.Frame(root, padx=10, pady=10)
    frame_add.pack(fill="x")

    tk.Label(frame_add, text="Dodaj książkę:", font=("Arial", 12)).grid(row=0, column=0, columnspan=2, sticky="w")
    tk.Label(frame_add, text="Tytuł:").grid(row=1, column=0, sticky="e", pady=2)
    entry_title = tk.Entry(frame_add, width=40)
    entry_title.grid(row=1, column=1, sticky="w", pady=2)
    tk.Label(frame_add, text="Autor:").grid(row=2, column=0, sticky="e", pady=2)
    entry_author = tk.Entry(frame_add, width=40)
    entry_author.grid(row=2, column=1, sticky="w", pady=2)
    tk.Button(frame_add, text="Dodaj książkę", command=add_item).grid(row=3, column=0, columnspan=2, pady=5)

    # Środkowy frame dla list użytkowników i książek
    frame_middle = tk.Frame(root, padx=10, pady=10)
    frame_middle.pack(fill="both", expand=True)

    # Lista użytkowników po lewej
    frame_users = tk.Frame(frame_middle)
    frame_users.pack(side="left", fill="y", padx=(0, 20))
    tk.Label(frame_users, text="Użytkownicy:", font=("Arial", 12)).pack()
    listbox_users = tk.Listbox(frame_users, width=40)
    listbox_users.pack(fill="y", expand=True)

    # Przyciski dla użytkowników po prawej
    frame_user_buttons = tk.Frame(frame_middle)
    frame_user_buttons.pack(side="left", fill="y")
    tk.Button(frame_user_buttons, text="Odśwież", width=20, command=load_users).pack(pady=5)
    tk.Button(frame_user_buttons, text="Nadaj admina", width=20, command=make_admin).pack(pady=5)
    tk.Button(frame_user_buttons, text="Usuń użytkownika", width=20, command=delete_user).pack(pady=5)

    # Lista książek poniżej
    frame_items = tk.Frame(root, padx=10, pady=10)
    frame_items.pack(fill="both", expand=True)
    tk.Label(frame_items, text="Książki:", font=("Arial", 12)).pack()
    listbox_items = tk.Listbox(frame_items)
    listbox_items.pack(fill="both", expand=True)
    frame_item_buttons = tk.Frame(frame_items)
    frame_item_buttons.pack(pady=5)
    tk.Button(frame_item_buttons, text="Odśwież listę książek", command=load_items).pack(side="left", padx=5)
    tk.Button(frame_item_buttons, text="Usuń książkę", command=delete_item).pack(side="left", padx=5)
    tk.Button(frame_item_buttons, text="Wyloguj", command=logout).pack(side="left", padx=5)

    # --- Inicjalne ładowanie danych ---
    load_users()
    load_items()

    root.mainloop()
