import tkinter as tk
from tkinter import messagebox
from db import get_connection
import gui_login  # import do funkcji logout

def show_main(username):
    root = tk.Tk()
    root.title("Panel główny - Wypożyczalnia")
    root.geometry("600x400")

    tk.Label(root, text=f"Witaj, {username}!", font=("Arial", 14)).pack(pady=10)

    listbox = tk.Listbox(root, width=80)
    listbox.pack(pady=10, expand=True, fill="both")

    def load_items():
        listbox.delete(0, tk.END)
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT id, title, author, available FROM items")
        for row in c.fetchall():
            status = "Dostępny" if row[3] == 1 else "Wypożyczony"
            listbox.insert(tk.END, f"{row[0]}. {row[1]} - {row[2]} [{status}]")
        conn.close()

    def rent_item():
        selection = listbox.curselection()
        if not selection:
            messagebox.showerror("Błąd", "Wybierz pozycję!")
            return
        item_id = listbox.get(selection[0]).split(".")[0]

        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT available FROM items WHERE id=?", (item_id,))
        available = c.fetchone()[0]
        if available == 0:
            messagebox.showerror("Błąd", "Ta pozycja jest już wypożyczona!")
        else:
            c.execute("SELECT id FROM users WHERE username=?", (username,))
            user_id = c.fetchone()[0]
            c.execute("INSERT INTO rentals(user_id, item_id) VALUES (?, ?)", (user_id, item_id))
            c.execute("UPDATE items SET available=0 WHERE id=?", (item_id,))
            conn.commit()
            messagebox.showinfo("Sukces", "Wypożyczono!")
        conn.close()
        load_items()

    def return_item():
        selection = listbox.curselection()
        if not selection:
            messagebox.showerror("Błąd", "Wybierz pozycję!")
            return
        item_id = listbox.get(selection[0]).split(".")[0]

        conn = get_connection()
        c = conn.cursor()
        c.execute("""
        SELECT r.id FROM rentals r
        JOIN users u ON r.user_id=u.id
        WHERE r.item_id=? AND u.username=? AND r.return_date IS NULL
        """, (item_id, username))
        rental = c.fetchone()
        if not rental:
            messagebox.showerror("Błąd", "Nie wypożyczyłeś tej pozycji!")
        else:
            rental_id = rental[0]
            c.execute("UPDATE rentals SET return_date=CURRENT_TIMESTAMP WHERE id=?", (rental_id,))
            c.execute("UPDATE items SET available=1 WHERE id=?", (item_id,))
            conn.commit()
            messagebox.showinfo("Sukces", "Zwrócono pozycję!")
        conn.close()
        load_items()

    def logout():
        root.destroy()
        gui_login.show_login()

    tk.Button(root, text="Odśwież listę", command=load_items).pack()
    tk.Button(root, text="Wypożycz", command=rent_item).pack()
    tk.Button(root, text="Zwróć", command=return_item).pack()
    tk.Button(root, text="Wyloguj", command=logout).pack(pady=5)

    load_items()
    root.mainloop()
