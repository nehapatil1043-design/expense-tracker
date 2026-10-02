"""
Project 1 (Basic): Expense Tracker
Tech: Python + SQLite (command line app)
"""
import sqlite3
from datetime import datetime

DB_NAME = "expenses.db"


def connect():
    return sqlite3.connect(DB_NAME)


def init_db():
    """Create the table if it does not exist."""
    with connect() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS expenses (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   date TEXT NOT NULL,
                   category TEXT NOT NULL,
                   description TEXT,
                   amount REAL NOT NULL)"""
        )


def add_expense(date, category, description, amount):
    with connect() as conn:
        conn.execute(
            "INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
            (date, category, description, amount),
        )


def get_expenses():
    with connect() as conn:
        return conn.execute(
            "SELECT id, date, category, description, amount FROM expenses ORDER BY date"
        ).fetchall()


def delete_expense(expense_id):
    with connect() as conn:
        cur = conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        return cur.rowcount  # 1 if deleted, 0 if id not found


def total_by_category():
    with connect() as conn:
        return conn.execute(
            "SELECT category, SUM(amount) FROM expenses GROUP BY category ORDER BY SUM(amount) DESC"
        ).fetchall()


def monthly_total(month):
    """month format: YYYY-MM"""
    with connect() as conn:
        row = conn.execute(
            "SELECT SUM(amount) FROM expenses WHERE date LIKE ?", (month + "%",)
        ).fetchone()
        return row[0] or 0


# ---------- input helpers (validation) ----------
def ask_amount():
    while True:
        try:
            amount = float(input("Amount: "))
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return amount
        except ValueError:
            print("Please enter a valid number.")


def ask_date():
    while True:
        text = input("Date (YYYY-MM-DD, press Enter for today): ").strip()
        if text == "":
            return datetime.today().strftime("%Y-%m-%d")
        try:
            datetime.strptime(text, "%Y-%m-%d")
            return text
        except ValueError:
            print("Wrong format. Example: 2026-09-30")


def show_table(rows):
    if not rows:
        print("No expenses found.")
        return
    print(f"\n{'ID':<4}{'Date':<12}{'Category':<14}{'Description':<20}{'Amount':>10}")
    print("-" * 60)
    for r in rows:
        print(f"{r[0]:<4}{r[1]:<12}{r[2]:<14}{(r[3] or ''):<20}{r[4]:>10.2f}")


def main():
    init_db()
    while True:
        print("\n===== EXPENSE TRACKER =====")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Delete an expense")
        print("4. Total by category")
        print("5. Monthly total")
        print("6. Exit")
        choice = input("Choose (1-6): ").strip()

        if choice == "1":
            date = ask_date()
            category = input("Category (Food/Travel/Bills...): ").strip().title() or "Other"
            description = input("Description: ").strip()
            amount = ask_amount()
            add_expense(date, category, description, amount)
            print("Expense added.")
        elif choice == "2":
            show_table(get_expenses())
        elif choice == "3":
            try:
                expense_id = int(input("Enter expense ID to delete: "))
            except ValueError:
                print("ID must be a number.")
                continue
            print("Deleted." if delete_expense(expense_id) else "ID not found.")
        elif choice == "4":
            for category, total in total_by_category():
                print(f"{category:<14}{total:>10.2f}")
        elif choice == "5":
            month = input("Month (YYYY-MM): ").strip()
            print(f"Total for {month}: {monthly_total(month):.2f}")
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1-6.")


if __name__ == "__main__":
    main()
