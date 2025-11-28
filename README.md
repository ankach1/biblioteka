# Dokumentacja projektu: Wypożyczalnia

## 1. Struktura projektu

```
wypozyczalnia/
│── main.py            # Punkt startowy aplikacji
│── db.py              # Obsługa bazy danych (3 tabele + relacje)
│── gui_login.py       # Formatka logowania/rejestracji (Tkinter)
│── gui_main.py        # Panel główny użytkownika
│── gui_admin.py       # Panel administratora
│── utils.py           # Pomocnicze funkcje (np. hashowanie haseł)
│── docs/
│    └── README.md     # Dokumentacja projektu
```

---

## 2. Opis modułów

### **main.py**

Główna część aplikacji. Odpowiada za:

* inicjalizację bazy danych,
* obsługę logowania,
* uruchamianie odpowiednich paneli (użytkownika lub administratora),
* główną pętlę aplikacji.

---

### **db.py**

Moduł odpowiedzialny za połączenie z bazą danych oraz obsługę trzech tabel:

1. **users** -- dane użytkowników
2. **items** -- lista książek dostępnych do wypożyczenia
3. **rentals** -- informacja o wypożyczeniach

Zawiera relacje:

* użytkownik → wypożyczenia (1:N)
* przedmiot → wypożyczenia (1:N)

---

### **gui_login.py**

Formularz logowania przygotowany przy pomocy Tkinter.
Funkcje:

* logowanie użytkownika,
* rejestracja nowego konta (walidacja danych),
* obsługa błędów logowania.

---

### **gui_main.py**

Panel główny użytkownika:

* lista dostępnych książek,
* możliwość wypożyczania,
* przegląd swoich wypożyczeń,
* zwroty książek.

---

### **gui_admin.py**

Panel administratora:

* zarządzanie książkami (dodawanie/edycja/usuwanie),
* podgląd aktywnych wypożyczeń,
* zarządzanie użytkownikami,
* statystyki.

---

### **utils.py**

Zbiór funkcji pomocniczych, m.in.:

* bezpieczne hashowanie haseł (SHA-256),
* walidacje danych,
* funkcje wielokrotnego użytku.

---

## 3. Technologia

### Język

* **Python**

### Biblioteki

* **Tkinter** -- interfejs graficzny
* **sqlite3** -- baza danych
* **hashlib** -- hashowanie haseł

---

## 4. Logika działania

1. Użytkownik uruchamia aplikację → ładuje się `main.py`
2. Pojawia się okno logowania `gui_login.py`
3. Po zalogowaniu:

   * jeśli zwykły użytkownik → `gui_main.py`
   * jeśli admin → `gui_admin.py`
4. Wszystkie operacje (rejestracje, wypożyczenia, zmiany) zapisują dane przez `db.py`.

---

## 5. Baza danych -- przykładowa struktura

### users

| id | username | password_hash | role |
| -- | -------- | ------------- | ---- |

### items

| id | title | author | available |
| -- | ----- | ------ | --------- |

### rentals

| id | user_id | item_id | rent_date | return_date |
| -- | ------- | ------- | --------- | ----------- |

---

## 6. Plan rozwoju (opcjonalne)

* eksport danych do PDF,
* system powiadomień o zaległych zwrotach,
* logi aktywności administracyjnej,
* integracja z API zewnętrznym.

---

## 7. Autor i licencja

Miejsce na dane autora i typ licencji projektu.
