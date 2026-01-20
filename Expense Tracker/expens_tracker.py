import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import matplotlib.pyplot as plt
import csv
import os

DB_FILE = 'expenses.db'

def setup_database():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, amount REAL, category TEXT, note TEXT
    )''')
    conn.commit()
    return conn, c

def add_expense(conn, c, date, amount, category, note):
    c.execute("INSERT INTO expenses (date, amount, category, note) VALUES (?, ?, ?, ?)", (date, amount, category, note))
    conn.commit()

def view_expenses(c):
    c.execute("SELECT * FROM expenses")
    rows = c.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Date: {row[1]}, Amount: {row[2]}, Category: {row[3]}, Note: {row[4]}")

def generate_report(c):
    c.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = c.fetchall()
    categories = [item[0] or "Uncategorized" for item in data]
    amounts = [item[1] for item in data]
    if any(amounts):
        plt.figure(figsize=(6,6))
        plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=90)
        plt.title('Category-wise Expense Distribution')
        plt.show()
    else:
        print("No data to display.")

def export_csv(c):
    c.execute("SELECT * FROM expenses")
    rows = c.fetchall()
    with open('expenses_export.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['ID', 'Date', 'Amount', 'Category', 'Note'])
        writer.writerows(rows)
    print("Data exported to expenses_export.csv")

def gui():
    conn, c = setup_database()
    root = tk.Tk()
    root.title("Personal Expense Tracker")
    root.geometry("500x400")

    def add_expense_ui():
        date = simpledialog.askstring("Input", "Enter date (DD-MM-YYYY) or leave blank for today:")
        if not date:
            date = datetime.now().strftime('%d-%m-%Y')
        try:
            amount_str = simpledialog.askstring("Input", "Enter amount:")
            amount = float(amount_str)
        except Exception:
            messagebox.showerror("Error", "Invalid amount.")
            return
        category = simpledialog.askstring("Input", "Enter category:") or "Uncategorized"
        note = simpledialog.askstring("Input", "Enter note:") or ""
        add_expense(conn, c, date, amount, category, note)
        messagebox.showinfo("Success", "Expense added successfully.")

    def view_expenses_ui():
        view_window = tk.Toplevel()
        view_window.title("View Expenses")
        tree = ttk.Treeview(view_window, columns=("ID", "Date", "Amount", "Category", "Note"), show='headings')
        for col in ("ID", "Date", "Amount", "Category", "Note"):
            tree.heading(col, text=col)
            tree.column(col, width=100)
        tree.pack(fill=tk.BOTH, expand=True)
        c.execute("SELECT * FROM expenses")
        for row in c.fetchall():
            tree.insert("", tk.END, values=row)

    def generate_report_ui():
        generate_report(c)

    def export_csv_ui():
        export_csv(c)
        messagebox.showinfo("Export", "Data exported to expenses_export.csv")

    tk.Button(root, text="Add Expense", command=add_expense_ui, width=30).pack(pady=8)
    tk.Button(root, text="View Expenses", command=view_expenses_ui, width=30).pack(pady=8)
    tk.Button(root, text="Generate Report", command=generate_report_ui, width=30).pack(pady=8)
    tk.Button(root, text="Export to CSV", command=export_csv_ui, width=30).pack(pady=8)
    tk.Button(root, text="Exit", command=lambda: (conn.close(), root.destroy()), width=30).pack(pady=8)
    root.mainloop()
    # connection closed when user hits Exit via above lambda

def main():
    conn, c = setup_database()
    try:
        while True:
            print("\n==== Personal Expense Tracker (CLI) ====")
            print("1. Add Expense")
            print("2. View Expenses")
            print("3. Generate Report")
            print("4. Export to CSV")
            print("5. Open GUI")
            print("6. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                date = input("Enter date (DD-MM-YYYY) or leave blank for today: ")
                if not date:
                    date = datetime.now().strftime('%d-%m-%Y')
                try:
                    amount = float(input("Enter amount: "))
                except ValueError:
                    print("Invalid amount.")
                    continue
                category = input("Enter category: ") or "Uncategorized"
                note = input("Enter note: ")
                add_expense(conn, c, date, amount, category, note)
                print("Expense added successfully.")
            elif choice == '2':
                view_expenses(c)
            elif choice == '3':
                generate_report(c)
            elif choice == '4':
                export_csv(c)
            elif choice == '5':
                gui()
            elif choice == '6':
                print("Exiting.")
                break
            else:
                print("Invalid choice.")
    finally:
        conn.close()

if __name__ == "__main__":
    main()
