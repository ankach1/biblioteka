import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection
import gui_login

def show_admin():
    root = tk.Tk()
    root.title("Panel administratora")
    root.geometry("1400x800")
    root.minsize(1200, 700)
    root.configure(bg="#eceff1")

    # Ustawienia stylu
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TButton", padding=6, font=('Helvetica', 10, 'bold'))
    style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'))

    #
    def logout():
        root.destroy()
        gui_login.show_login()

    #
    def load_users():
        tree_users.delete(*tree_users.get_children())
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, username, role FROM users")
        for row in c.fetchall():
            tree_users.insert("", "end", iid=row[0], values=(row[1], row[2]))
        conn.close()

    def make_admin():
        sel = tree_users.selection()
        if not sel:
            messagebox.showerror("Błąd", "Wybierz użytkownika!")
            return
        uid = sel[0]
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE users SET role='admin' WHERE id=?", (uid,))
        conn.commit()
        conn.close()
        load_users()
        messagebox.showinfo("OK", "Użytkownik został adminem.")

    def delete_user():
        sel = tree_users.selection()
        if not sel:
            messagebox.showerror("Błąd", "Wybierz użytkownika!")
            return
        uid = sel[0]
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (uid,))
        conn.commit()
        conn.close()
        load_users()
        messagebox.showinfo("OK", "Usunięto użytkownika.")

    # --- Funkcje książek ---
    def load_items():
        tree_items.delete(*tree_items.get_children())
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, title, author, available FROM items")
        for row in c.fetchall():
            tree_items.insert("", "end", iid=row[0],
                values=(row[1], row[2], "Dostępny" if row[3] == 1 else "Wypożyczony"))
        conn.close()

    def search_items():
        query = entry_search.get().lower()
        tree_items.delete(*tree_items.get_children())
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, title, author, available FROM items")
        for row in c.fetchall():
            if query in row[1].lower():
                tree_items.insert("", "end", iid=row[0],
                    values=(row[1], row[2], "Dostępny" if row[3] == 1 else "Wypożyczony"))
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
        entry_title.delete(0, tk.END)
        entry_author.delete(0, tk.END)
        load_items()

    def delete_item():
        sel = tree_items.selection()
        if not sel:
            messagebox.showerror("Błąd", "Wybierz książkę!")
            return
        item_id = sel[0]
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM items WHERE id=?", (item_id,))
        conn.commit()
        conn.close()
        load_items()

    def edit_item():
        sel = tree_items.selection()
        if not sel:
            messagebox.showerror("Błąd", "Wybierz książkę!")
            return

        item_id = sel[0]
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT title, author, available FROM items WHERE id=?", (item_id,))
        book = c.fetchone()
        conn.close()

        if not book:
            return

        edit = tk.Toplevel(root)
        edit.title("Edytuj książkę")
        edit.geometry("380x220")
        edit.configure(bg="#eceff1")

        tk.Label(edit, text="Tytuł:", bg="#eceff1").grid(row=0, column=0, padx=5, pady=5)
        et = tk.Entry(edit, width=40)
        et.grid(row=0, column=1)
        et.insert(0, book[0])

        tk.Label(edit, text="Autor:", bg="#eceff1").grid(row=1, column=0, padx=5, pady=5)
        ea = tk.Entry(edit, width=40)
        ea.grid(row=1, column=1)
        ea.insert(0, book[1])

        tk.Label(edit, text="Status:", bg="#eceff1").grid(row=2, column=0, padx=5, pady=5)
        st = tk.StringVar(value="Dostępny" if book[2] == 1 else "Wypożyczony")
        ttk.Combobox(edit, textvariable=st, values=["Dostępny", "Wypożyczony"],
                     state="readonly").grid(row=2, column=1, padx=5)

        def save_changes():
            conn = get_connection()
            c = conn.cursor()
            c.execute("UPDATE items SET title=?, author=?, available=? WHERE id=?",
                      (et.get(), ea.get(), 1 if st.get() == "Dostępny" else 0, item_id))
            conn.commit()
            conn.close()
            load_items()
            edit.destroy()

        tk.Button(edit, text="Zapisz", bg="#4caf50", fg="white",
                  command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)


    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=3)
    root.grid_rowconfigure(0, weight=1)

    # kolumna użytkownicy

    frame_users = tk.LabelFrame(root, text="Użytkownicy", bg="#eceff1", padx=10, pady=10)
    frame_users.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    frame_users.grid_rowconfigure(1, weight=1)

    tree_users = ttk.Treeview(frame_users, columns=("u", "r"), show="headings")
    tree_users.heading("u", text="Nazwa")
    tree_users.heading("r", text="Rola")
    tree_users.grid(row=1, column=0, sticky="nsew", pady=5)


    user_buttons = tk.Frame(frame_users, bg="#eceff1")
    user_buttons.grid(row=2, column=0, pady=5, sticky="ew")

    ttk.Button(user_buttons, text="Odśwież", command=load_users).pack(side="left", padx=5)
    ttk.Button(user_buttons, text="Nadaj admina", command=make_admin).pack(side="left", padx=5)
    ttk.Button(user_buttons, text="Usuń", command=delete_user).pack(side="left", padx=5)

    # prawa kolummna ksiązki

    frame_items = tk.LabelFrame(root, text="Książki", bg="#eceff1", padx=10, pady=10)
    frame_items.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    frame_items.grid_rowconfigure(2, weight=1)

    # wyszukiwarka
    search_frame = tk.Frame(frame_items, bg="#eceff1")
    search_frame.grid(row=0, column=0, sticky="ew")
    entry_search = tk.Entry(search_frame, width=30)
    entry_search.pack(side="left", padx=5)
    tk.Button(search_frame, text="Szukaj", bg="#2196f3", fg="white",
              command=search_items).pack(side="left", padx=5)

    # drzewko
    tree_items = ttk.Treeview(frame_items, columns=("t", "a", "s"), show="headings")
    tree_items.heading("t", text="Tytuł")
    tree_items.heading("a", text="Autor")
    tree_items.heading("s", text="Status")
    tree_items.grid(row=2, column=0, sticky="nsew", pady=5)

    # dodawanie książki
    add_frame = tk.Frame(frame_items, bg="#eceff1")
    add_frame.grid(row=1, column=0, pady=5)
    tk.Label(add_frame, text="Tytuł:", bg="#eceff1").grid(row=0, column=0)
    entry_title = tk.Entry(add_frame, width=22)
    entry_title.grid(row=0, column=1)
    tk.Label(add_frame, text="Autor:", bg="#eceff1").grid(row=1, column=0)
    entry_author = tk.Entry(add_frame, width=22)
    entry_author.grid(row=1, column=1)
    tk.Button(add_frame, text="Dodaj", bg="#4caf50", fg="white",
              command=add_item).grid(row=2, column=0, columnspan=2, pady=5)

    # przyciski zarządzania
    item_btns = tk.Frame(frame_items, bg="#eceff1")
    item_btns.grid(row=3, column=0, pady=5)
    tk.Button(item_btns, text="Odśwież", bg="#607d8b", fg="white",
              command=load_items).pack(side="left", padx=4)
    tk.Button(item_btns, text="Usuń", bg="#f44336", fg="white",
              command=delete_item).pack(side="left", padx=4)
    tk.Button(item_btns, text="Edytuj", bg="#ff9800", fg="white",
              command=edit_item).pack(side="left", padx=4)
    tk.Button(item_btns, text="Wyloguj", bg="#9c27b0", fg="white",
              command=logout).pack(side="left", padx=4)

    load_users()
    load_items()
    root.mainloop()
