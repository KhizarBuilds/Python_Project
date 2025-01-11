import tkinter as tk
from tkinter import messagebox
import os

# Global dictionary to store accounts
accounts = {}

# File to save transactions
TRANSACTION_FILE = "transactions.txt"

# Function to create an account
def create_account(name):
    if name in accounts:
        messagebox.showerror("Error", "Account already exists.")
        return

    accounts[name] = {
        "balance": 0.0,
        "transactions": []
    }
    messagebox.showinfo("Success", f"Account for {name} created with balance $0.0.")

# Function to deposit money
def deposit_money(name, amount):
    if name not in accounts:
        messagebox.showerror("Error", "Account does not exist.")
        return

    if amount <= 0:
        messagebox.showerror("Error", "Deposit amount must be positive.")
        return

    accounts[name]["balance"] += amount
    accounts[name]["transactions"].append(f"Deposit: ${amount}")
    save_transaction(name, f"Deposit: ${amount}")
    messagebox.showinfo("Success", f"Deposited ${amount}. New balance: ${accounts[name]['balance']:.2f}.")

# Function to withdraw money
def withdraw_money(name, amount):
    if name not in accounts:
        messagebox.showerror("Error", "Account does not exist.")
        return

    if amount <= 0:
        messagebox.showerror("Error", "Withdrawal amount must be positive.")
        return

    if accounts[name]["balance"] < amount:
        messagebox.showerror("Error", "Insufficient balance.")
        return

    accounts[name]["balance"] -= amount
    accounts[name]["transactions"].append(f"Withdrawal: ${amount}")
    save_transaction(name, f"Withdrawal: ${amount}")
    messagebox.showinfo("Success", f"Withdrew ${amount}. New balance: ${accounts[name]['balance']:.2f}.")

# Function to check balance
def check_balance(name):
    if name not in accounts:
        messagebox.showerror("Error", "Account does not exist.")
        return

    balance = accounts[name]["balance"]
    messagebox.showinfo("Balance", f"Current balance: ${balance:.2f}.")

# Function to print statement
def print_statement(name):
    if name not in accounts:
        messagebox.showerror("Error", "Account does not exist.")
        return

    transactions = accounts[name]["transactions"]
    if not transactions:
        messagebox.showinfo("Statement", "No transactions available.")
        return

    statement = f"Account statement for {name}:\n"
    for transaction in transactions:
        statement += f"- {transaction}\n"
    messagebox.showinfo("Statement", statement)

# Function to save transactions to file
def save_transaction(name, transaction):
    with open(TRANSACTION_FILE, "a") as file:
        file.write(f"{name}: {transaction}\n")

# Function to transfer money
def transfer_money(from_name, to_name, amount):
    if from_name not in accounts:
        messagebox.showerror("Error", f"Sender account ({from_name}) does not exist.")
        return

    if to_name not in accounts:
        messagebox.showerror("Error", f"Recipient account ({to_name}) does not exist.")
        return

    if amount <= 0:
        messagebox.showerror("Error", "Transfer amount must be positive.")
        return

    if accounts[from_name]["balance"] < amount:
        messagebox.showerror("Error", "Insufficient balance in sender's account.")
        return

    accounts[from_name]["balance"] -= amount
    accounts[to_name]["balance"] += amount

    accounts[from_name]["transactions"].append(f"Transfer to {to_name}: ${amount}")
    accounts[to_name]["transactions"].append(f"Transfer from {from_name}: ${amount}")

    save_transaction(from_name, f"Transfer to {to_name}: ${amount}")
    save_transaction(to_name, f"Transfer from {from_name}: ${amount}")

    messagebox.showinfo("Success", f"Transferred ${amount} from {from_name} to {to_name}.")

# Function to delete an account
def delete_account(name):
    if name not in accounts:
        messagebox.showerror("Error", "Account does not exist.")
        return

    del accounts[name]
    messagebox.showinfo("Success", f"Account for {name} has been deleted.")

# GUI Setup
def main():
    root = tk.Tk()
    root.title("Banking System")

    tk.Label(root, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(root)
    name_entry.grid(row=0, column=1)

    tk.Label(root, text="Amount:").grid(row=1, column=0)
    amount_entry = tk.Entry(root)
    amount_entry.grid(row=1, column=1)

    tk.Label(root, text="Recipient Name:").grid(row=2, column=0)
    recipient_entry = tk.Entry(root)
    recipient_entry.grid(row=2, column=1)

    tk.Button(root, text="Create Account", command=lambda: create_account(name_entry.get())).grid(row=3, column=0)
    tk.Button(root, text="Deposit", command=lambda: deposit_money(name_entry.get(), float(amount_entry.get()))).grid(row=3, column=1)
    tk.Button(root, text="Withdraw", command=lambda: withdraw_money(name_entry.get(), float(amount_entry.get()))).grid(row=4, column=0)
    tk.Button(root, text="Check Balance", command=lambda: check_balance(name_entry.get())).grid(row=4, column=1)
    tk.Button(root, text="Print Statement", command=lambda: print_statement(name_entry.get())).grid(row=5, column=0, columnspan=2)
    tk.Button(root, text="Transfer Money", command=lambda: transfer_money(name_entry.get(), recipient_entry.get(), float(amount_entry.get()))).grid(row=6, column=0, columnspan=2)
    tk.Button(root, text="Delete Account", command=lambda: delete_account(name_entry.get())).grid(row=7, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main()
