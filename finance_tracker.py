import csv
import os
import shutil
from datetime import datetime

#file name for storing records
INCOME_FILE = 'income.csv'
EXPENSES_FILE = 'expenses.csv'
BUDGET_FILE = 'budget.csv'
BACKUP_FOLDER = 'backup'

#file setup
def setup_files():
    if not os.path.exists(INCOME_FILE):
        with open(INCOME_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Amount', 'Source', 'Date'])

    if not os.path.exists(EXPENSES_FILE):
        with open(EXPENSES_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Amount', 'Category', 'Date'])

    if not os.path.exists(BUDGET_FILE):
        with open(BUDGET_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Category', 'Budget'])


#input validation
def get_amount():
    while True:
        try:
            amount = float(input("Enter the amount: "))
            if amount <= 0:
                print("Amount must be greater than 0. Please try again.")
            else:
                return amount

        except ValueError:
            print("Invalid input. Please enter a valid number.")

def get_text(message):
    while True:
        value = input(message).strip()

        if value == "":
            print("This field cannot be empty.")
        else:
            return value

def get_date():
    while True:
        date = input("Enter date (YYYY-MM-DD): ").strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date

        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")


def get_month():
    while True:
        month = input("Enter month (YYYY-MM): ").strip()
        try:
            datetime.strptime(month, "%Y-%m")
            return month

        except ValueError:
            print("Invalid month. Please use YYYY-MM.")


#add income
def add_income():
    print("\n========== ADD INCOME ==========")

    amount = get_amount()
    source = get_text("Enter the source of income: ")
    date = get_date()

    try:
        with open(INCOME_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([amount, source, date])

        print("Income record added successfully.")

    except OSError as error:
        print("Error saving income:", error)


#add expense
def add_expense():
    print("\n========== ADD EXPENSE ==========")

    amount = get_amount()
    category = get_text("Enter the category of expense: ")
    date = get_date()

    try:
        with open(EXPENSES_FILE, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([amount, category, date])

        print("Expense record added successfully.")

    except OSError as error:
        print("Error saving expense:", error)


#view income
def view_income():
    print("\n========== VIEW INCOME ==========")

    try:
        with open(INCOME_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader)  #Skip header
            records = list(reader)

            if not records:
                print("No income records found.")
                return

            for record in records:
                print(f"Amount: {record[0]}, Source: {record[1]}, Date: {record[2]}")

    except OSError as error:
        print("Error reading income:", error)

#view expenses
def view_expenses():
    print("\n========== EXPENSE RECORDS ==========")

    try:
        with open(EXPENSES_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            records = list(reader)

            if not records:
                print("No expense records found.")
                return

            print(f"{'Date':<15}{'Category':<20}{'Amount':>10}")
            print("-" * 45)

            for record in records:
                print(
                    f"{record['date']:<15}"
                    f"{record['category']:<20}"
                    f"{float(record['amount']):>10.2f}"
                )

    except (OSError, ValueError) as error:
        print("Error reading expense records:", error)


#view all records
def view_all_records():
    print("\n========== VIEW ALL RECORDS ==========")

    view_income()
    view_expenses()

#calculate total income
def get_total_income():
    total_income = 0.0

    try:
        with open(INCOME_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader)  
            for record in reader:
                total_income += float(record[0])

    except OSError as error:
        print("Error reading income:", error)

    return total_income

#calculate total expenses
def get_total_expenses(): 
    total_expenses = 0.0

    try:
        with open(EXPENSES_FILE, 'r') as file:
            reader = csv.reader(file)
            next(reader)  
            for record in reader:
                total_expenses += float(record[0])

    except OSError as error:
        print("Error reading expenses:", error)

    return total_expenses


#show summary
def show_summary():
    print("\n========== SUMMARY ==========")

    total_income = get_total_income()
    total_expenses = get_total_expenses()
    balance = total_income - total_expenses

    print(f"Total Income: {total_income:.2f}")
    print(f"Total Expenses: {total_expenses:.2f}")
    print(f"Balance: {balance:.2f}")

#set budget
def set_budget():
    print("\n========== SET BUDGET ==========")

    category = get_text("Enter category: ")
    budget = get_amount()

    budgets = []

    try:
        with open(BUDGET_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            for record in reader:
                budgets.append(record)

    except OSError as error:
        print("Error reading budgets:", error)
        return

    category_found = False

    for record in budgets:
        if record["category"].lower() == category.lower():
            record["category"] = category
            record["budget"] = budget
            category_found = True

    if not category_found:
        budgets.append({
            "category": category,
            "budget": budget
        })

    try:
        with open(BUDGET_FILE, "w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(["category", "budget"])

            for record in budgets:
                writer.writerow([
                    record["category"],
                    record["budget"]
                ])

        print("Budget saved successfully.")

    except OSError as error:
        print("Error saving budget:", error)


#view budgets
def view_budgets():
    print("\n========== BUDGET REPORT ==========")

    category_totals = get_expenses_by_category()

    try:
        with open(BUDGET_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            records = list(reader)

            if not records:
                print("No budgets have been set.")
                return

            print(
                f"{'Category':<20}"
                f"{'Budget':>12}"
                f"{'Spent':>12}"
                f"{'Remaining':>15}"
            )

            print("-" * 60)

            for record in records:

                category = record["category"]
                budget = float(record["budget"])
                spent = category_totals.get(category, 0)

                remaining = budget - spent

                print(
                    f"{category:<20}"
                    f"{budget:>12.2f}"
                    f"{spent:>12.2f}"
                    f"{remaining:>15.2f}"
                )

                if spent > budget:
                    print(
                        f"WARNING: You exceeded your "
                        f"{category} budget!"
                    )

    except (OSError) as error:
        print("Error reading budgets:", error)


#get expenses by category
def get_expenses_by_category():
    category_totals = {}

    try:
        with open(EXPENSES_FILE, "r", newline="") as file:
            reader = csv.DictReader(file)

            for record in reader:
                category = record["category"]
                amount = float(record["amount"])

                if category in category_totals:
                    category_totals[category] += amount

                else:
                    category_totals[category] = amount

    except (OSError) as error:
        print("Error reading expenses:", error)

    return category_totals


#pie chart of expenses by category
def expense_pie_chart():
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        print("\nMatplotlib is not installed.")
        return

    category_totals = get_expenses_by_category()

    if not category_totals:
        print("No expenses available for the chart.")
        return

    categories = list(category_totals.keys())
    amounts = list(category_totals.values())

    plt.figure(figsize=(7, 7))

    plt.pie(
        amounts,
        labels=categories,
        autopct="%1.1f%%"
    )

    plt.title("Expenses by Category")


#backup data
def backup_data():
    print("\n========== BACKUP DATA ==========")

    try:
        if not os.path.exists(BACKUP_FOLDER):
            os.makedirs(BACKUP_FOLDER)

        files = [
            INCOME_FILE,
            EXPENSES_FILE,
            BUDGET_FILE
        ]

        for file_name in files:

            if os.path.exists(file_name):
                destination = os.path.join(
                    BACKUP_FOLDER,
                    file_name
                )

                shutil.copy(file_name, destination)

        print("Backup completed successfully.")

    except OSError as error:
        print("Error creating backup:", error)



#main menu
def show_menu():
    print("\n")
    print("=" * 15)
    print("       PERSONAL FINANCE TRACKER")
    print("=" * 15)

    print("1. Add Income")
    print("2. Add Expense")
    print("3. View Records")
    print("4. Show Summary")
    print("5. Set Budget")
    print("6. View Budget Report")
    print("7. Expense Pie Chart")
    print("8. Backup Data")
    print("9. Exit")

    print("=" * 15)

#main program
def main():

    setup_files()

    while True:

        show_menu()

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_income()

        elif choice == "2":
            add_expense()

        elif choice == "3":
            view_all_records()

        elif choice == "4":
            show_summary()

        elif choice == "5":
            set_budget()

        elif choice == "6":
            view_budgets()

        elif choice == "7":
            expense_pie_chart()

        elif choice == "8":
            backup_data()

        elif choice == "9":
            print("\nThank you for using Personal Finance Tracker.")
            break

        else:
            print("\nInvalid choice. Please select a number from 1 to 9.")

#start program
if __name__ == "__main__":
    main()