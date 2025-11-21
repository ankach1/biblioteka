import tkinter as tk
from tkinter import ttk, messagebox
from db import get_connection
import gui_login

def show_main(username):
    root = tk.Tk()
    root.title("Panel użytkownika - Wypożyczalnia")
    root.geometry("700x500")
    root.minsize(650, 450)
    root.configure(bg="#eceff1")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TButton", padding=6, relief="flat", font=('Helvetica', 10, 'bold'))
    style.configure("TLabel", background="#eceff1", font=('Helvetica', 12))
    style.configure("Treeview", font=('Helvetica', 10))
    style.configure("Treeview.Heading", font=('Helvetica', 11, 'bold'))

    tk.Label(root, text=f"Witaj, {username}!", font=("Helvetica", 14, 'bold'), bg="#eceff1").pack(pady=10)

    # --- Wyszukiwanie ---
    search_frame = tk.Frame(root, bg="#eceff1")
    search_frame.pack(pady=5)
    tk.Label(search_frame, text="Szukaj książki:", bg="#eceff1").pack(side="left", padx=5)
    entry_search = tk.Entry(search_frame, width=30)
    entry_search.pack(side="left", padx=5)

    # --- Treeview dla książek ---
    tree_items = ttk.Treeview(root, columns=("Tytuł", "Autor", "Status"), show="headings")
    tree_items.heading("Tytuł", text="Tytuł")
    tree_items.heading("Autor", text="Autor")
    tree_items.heading("Status", text="Status")
    tree_items.pack(fill="both", expand=True, pady=10)

    # --- Funkcje ---
    def load_items():
        tree_items.delete(*tree_items.get_children())
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, title, author, available FROM items")
        for row in c.fetchall():
            status = "Dostępny" if row[3] == 1 else "Wypożyczony"
            tree_items.insert("", "end", iid=row[0], values=(row[1], row[2], status))
        conn.close()

    def search_items():
        query = entry_search.get().lower()
        tree_items.delete(*tree_items.get_children())
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, title, author, available FROM items")
        for row in c.fetchall():
            if query in row[1].lower():
                status = "Dostępny" if row[3] == 1 else "Wypożyczony"
                tree_items.insert("", "end", iid=row[0], values=(row[1], row[2], status))
        conn.close()

    def rent_item():
        selected = tree_items.selection()
        if not selected:
            messagebox.showerror("Błąd", "Wybierz książkę!")
            return
        item_id = selected[0]
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT available FROM items WHERE id=?", (item_id,))
        if c.fetchone()[0] == 0:
            messagebox.showerror("Błąd", "Ta książka jest już wypożyczona!")
        else:
            c.execute("SELECT id FROM users WHERE username=?", (username,))
            user_id = c.fetchone()[0]
            c.execute("INSERT INTO rentals(user_id, item_id) VALUES (?, ?)", (user_id, item_id))
            c.execute("UPDATE items SET available=0 WHERE id=?", (item_id,))
            conn.commit()
            messagebox.showinfo("Sukces", "Wypożyczono książkę!")
        conn.close()
        load_items()

    def return_item():
        selected = tree_items.selection()
        if not selected:
            messagebox.showerror("Błąd", "Wybierz książkę!")
            return
        item_id = selected[0]
        conn = get_connection()
        c = conn.cursor()
        c.execute("""
        SELECT r.id FROM rentals r
        JOIN users u ON r.user_id=u.id
        WHERE r.item_id=? AND u.username=? AND r.return_date IS NULL
        """, (item_id, username))
        rental = c.fetchone()
        if not rental:
            messagebox.showerror("Błąd", "Nie wypożyczyłeś tej książki!")
        else:
            rental_id = rental[0]
            c.execute("UPDATE rentals SET return_date=CURRENT_TIMESTAMP WHERE id=?", (rental_id,))
            c.execute("UPDATE items SET available=1 WHERE id=?", (item_id,))
            conn.commit()
            messagebox.showinfo("Sukces", "Zwrócono książkę!")
        conn.close()
        load_items()

    def logout():
        root.destroy()
        gui_login.show_login()

    # --- Przyciski ---
    button_frame = tk.Frame(root, bg="#eceff1")
    button_frame.pack(pady=5)
    tk.Button(button_frame, text="Odśwież", bg="#607d8b", fg="white", width=12, command=load_items).pack(side="left", padx=5)
    tk.Button(button_frame, text="Szukaj", bg="#2196f3", fg="white", width=12, command=search_items).pack(side="left", padx=5)
    tk.Button(button_frame, text="Wypożycz", bg="#4caf50", fg="white", width=12, command=rent_item).pack(side="left", padx=5)
    tk.Button(button_frame, text="Zwróć", bg="#ff9800", fg="white", width=12, command=return_item).pack(side="left", padx=5)
    tk.Button(button_frame, text="Wyloguj", bg="#9c27b0", fg="white", width=12, command=logout).pack(side="left", padx=5)

    load_items()
    root.mainloop()
