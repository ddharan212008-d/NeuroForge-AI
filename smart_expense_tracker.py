
import json
import csv
from pathlib import Path
from datetime import datetime
from collections import defaultdict

DATA_FILE = Path("expenses.json")
CSV_FILE = Path("expenses_report.csv")

CATEGORIES = [
    "Food",
    "Travel",
    "Education",
    "Shopping",
    "Bills",
    "Other"
]


def load_expenses():
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved data.")
        return []


def save_expenses(expenses):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=4)


def get_amount():
    while True:
        try:
            amount = float(input("Enter amount (Rs.): "))
            if amount > 0 and amount != float("inf"):
                return round(amount, 2)
            print("Amount must be greater than zero.")
        except ValueError:
            print("Enter a valid number.")


def add_expense(expenses):
    title = input("Expense name: ").strip()

    if not title:
        print("Expense name cannot be empty.")
        return

    print("\nCategories:")
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")

    try:
        choice = int(input("Choose category number: "))
        category = CATEGORIES[choice - 1]
    except (ValueError, IndexError):
        print("Invalid category.")
        return

    amount = get_amount()

    expense = {
        "title": title,
        "category": category,
        "amount": amount,
        "date": datetime.now().strftime("%Y-%m-%d")
    }

    expenses.append(expense)
    save_expenses(expenses)
    print("Expense saved successfully!")


def view_expenses(expenses):
    if not expenses:
        print("No expenses recorded yet.")
        return

    print("\n--- EXPENSE HISTORY ---")
    for number, expense in enumerate(expenses, start=1):
        print(
            f"{number}. {expense['date']} | "
            f"{expense['title']} | {expense['category']} | "
            f"Rs. {expense['amount']:.2f}"
        )


def show_summary(expenses):
    if not expenses:
        print("Add an expense first.")
        return

    totals = defaultdict(float)
    overall = 0.0

    for expense in expenses:
        totals[expense["category"]] += expense["amount"]
        overall += expense["amount"]

    current_month = datetime.now().strftime("%Y-%m")
    monthly_total = sum(
        item["amount"]
        for item in expenses
        if item["date"].startswith(current_month)
    )

    print("\n--- SPENDING SUMMARY ---")
    print(f"Total recorded spending: Rs. {overall:.2f}")
    print(f"This month's spending: Rs. {monthly_total:.2f}")

    print("\nCategory-wise spending:")
    for category, amount in sorted(totals.items()):
        percentage = amount / overall * 100
        print(f"{category}: Rs. {amount:.2f} ({percentage:.1f}%)")


def set_monthly_budget():
    while True:
        try:
            budget = float(input("Enter monthly budget (Rs.): "))
            if 0 < budget < float("inf"):
                return budget
            print("Budget must be greater than zero.")
        except ValueError:
            print("Enter a valid number.")


def check_budget(expenses, budget):
    month = datetime.now().strftime("%Y-%m")
    spent = sum(
        item["amount"]
        for item in expenses
        if item["date"].startswith(month)
    )

    print(f"This month's spending: Rs. {spent:.2f}")
    print(f"Monthly budget: Rs. {budget:.2f}")
    print(f"Remaining budget: Rs. {budget - spent:.2f}")

    if spent > budget:
        print("WARNING: Monthly budget exceeded!")
    elif spent == budget:
        print("You have reached your monthly budget.")
    else:
        print("You are within your monthly budget.")


def export_csv(expenses):
    if not expenses:
        print("No data available to export.")
        return

    fields = ["date", "title", "category", "amount"]

    with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(expenses)

    print(f"Report exported to {CSV_FILE.name}")


def main():
    expenses = load_expenses()
    budget = None

    while True:
        print("\n===== SMART EXPENSE TRACKER =====")
        print("1. Add expense")
        print("2. View expense history")
        print("3. Spending summary")
        print("4. Set monthly budget")
        print("5. Check monthly budget")
        print("6. Export CSV report")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        try:
            if choice == "1":
                add_expense(expenses)

            elif choice == "2":
                view_expenses(expenses)

            elif choice == "3":
                show_summary(expenses)

            elif choice == "4":
                budget = set_monthly_budget()

            elif choice == "5":
                if budget is None:
                    print("Set your budget first using option 4.")
                else:
                    check_budget(expenses, budget)

            elif choice == "6":
                export_csv(expenses)

            elif choice == "7":
                print("Your expenses are saved. Goodbye!")
                break

            else:
                print("Invalid option. Choose 1 to 7.")

        except (OSError, KeyError, TypeError) as error:
            print(f"An operation failed: {error}")


if __name__ == "__main__":
    main()
