import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

# -------------------------------
# File where expenses are stored
# -------------------------------
DATA_FILE = "expenses.json"

# -------------------------------
# Categories and Subcategories
# -------------------------------
CATEGORIES = {
    "Transport": ["Petrol", "Diesel", "Taxi", "Bus", "Train", "Other"],
    "Food": ["Groceries", "Restaurants", "Coffee", "Snacks", "Other"],
    "Bills": ["Electricity", "Water", "Internet", "Rent", "Other"],
    "Entertainment": ["Movies", "Games", "Subscriptions", "Other"],
    "Health": ["Doctor", "Medicine", "Gym", "Other"],
    "Shopping": ["Clothes", "Electronics", "Other"],
    "Education": ["Books", "Courses", "Supplies", "Other"],
    "Others": ["Miscellaneous"]
}

# -------------------------------
# Load and save functions
# -------------------------------
def load_expenses():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(DATA_FILE, "w") as f:
        json.dump(expenses, f, indent=4)

# -------------------------------
# Add expense
# -------------------------------
def add_expense():
    date = date_entry.get()
    category = category_var.get()
    subcategory = subcategory_var.get()
    amount = amount_entry.get()
    notes = notes_entry.get()
    
    # Validation
    if not category or not subcategory or not amount:
        messagebox.showerror("Error", "Please fill all required fields (Category, Subcategory, Amount)")
        return
    try:
        amount_val = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number")
        return
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Date must be in YYYY-MM-DD format")
        return
    
    expense = {
        "date": date,
        "category": category,
        "subcategory": subcategory,
        "amount": amount_val,
        "notes": notes
    }
    
    expenses.append(expense)
    save_expenses(expenses)
    update_treeview()
    clear_inputs()

# -------------------------------
# Delete selected expense
# -------------------------------
def delete_expense():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select an expense to delete")
        return
    index = int(selected[0])
    del expenses[index]
    save_expenses(expenses)
    update_treeview()

# -------------------------------
# Clear input fields
# -------------------------------
def clear_inputs():
    amount_entry.delete(0, tk.END)
    notes_entry.delete(0, tk.END)
    # reset date to today
    date_entry.delete(0, tk.END)
    date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))

# -------------------------------
# Update subcategories when category changes
# -------------------------------
def update_subcategories(*args):
    subcategory_menu["menu"].delete(0, "end")
    subcats = CATEGORIES.get(category_var.get(), [])
    for sub in subcats:
        subcategory_menu["menu"].add_command(label=sub, command=tk._setit(subcategory_var, sub))
    if subcats:
        subcategory_var.set(subcats[0])
    else:
        subcategory_var.set("")

# -------------------------------
# Update treeview table
# -------------------------------
def update_treeview():
    tree.delete(*tree.get_children())
    for i, exp in enumerate(expenses):
        tree.insert("", "end", iid=i, values=(exp["date"], exp["category"], exp["subcategory"], f"{exp['amount']:.2f}", exp["notes"]))
    update_summary()

# -------------------------------
# Summary per category
# -------------------------------
def update_summary():
    summary_text.delete(1.0, tk.END)
    totals = {}
    for exp in expenses:
        cat = exp["category"]
        totals[cat] = totals.get(cat, 0) + exp["amount"]
    summary_lines = [f"{cat}: {totals[cat]:.2f}" for cat in totals]
    summary_text.insert(tk.END, "\n".join(summary_lines))

# -------------------------------
# Initialize expenses list
# -------------------------------
expenses = load_expenses()

# -------------------------------
# GUI Setup
# -------------------------------
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("900x600")

# -------------------------------
# Input frame
# -------------------------------
input_frame = tk.Frame(root, padx=10, pady=10)
input_frame.pack(fill="x")

tk.Label(input_frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
date_entry = tk.Entry(input_frame)
date_entry.grid(row=0, column=1, sticky="w")
date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))

tk.Label(input_frame, text="Category:").grid(row=0, column=2, sticky="w")
category_var = tk.StringVar()
category_var.trace("w", update_subcategories)
category_menu = tk.OptionMenu(input_frame, category_var, *CATEGORIES.keys())
category_menu.grid(row=0, column=3, sticky="w")

tk.Label(input_frame, text="Subcategory:").grid(row=0, column=4, sticky="w")
subcategory_var = tk.StringVar()
subcategory_menu = tk.OptionMenu(input_frame, subcategory_var, "")
subcategory_menu.grid(row=0, column=5, sticky="w")

tk.Label(input_frame, text="Amount:").grid(row=1, column=0, sticky="w")
amount_entry = tk.Entry(input_frame)
amount_entry.grid(row=1, column=1, sticky="w")

tk.Label(input_frame, text="Notes:").grid(row=1, column=2, sticky="w")
notes_entry = tk.Entry(input_frame, width=50)
notes_entry.grid(row=1, column=3, columnspan=3, sticky="w")

tk.Button(input_frame, text="Add Expense", command=add_expense, bg="green", fg="white").grid(row=2, column=0, pady=10)
tk.Button(input_frame, text="Delete Selected", command=delete_expense, bg="red", fg="white").grid(row=2, column=1, pady=10)

# -------------------------------
# Treeview frame
# -------------------------------
tree_frame = tk.Frame(root, padx=10, pady=10)
tree_frame.pack(fill="both", expand=True)

columns = ("Date", "Category", "Subcategory", "Amount", "Notes")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.pack(fill="both", expand=True)

# -------------------------------
# Summary frame
# -------------------------------
summary_frame = tk.Frame(root, padx=10, pady=10)
summary_frame.pack(fill="x")

tk.Label(summary_frame, text="Summary by Category:").pack(anchor="w")
summary_text = tk.Text(summary_frame, height=6)
summary_text.pack(fill="x")

# Initialize GUI
update_treeview()

root.mainloop()