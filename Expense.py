import os  # to check that file isn't empty before reading 
import csv


class Expense:
    def __init__(self, category, amount, date):
        self.category = category
        self.amount = amount
        self.date = date

    def __str__(self):
        return f"{self.date} | {self.category} | {self.amount} |"


class Category:
    def __init__(self, name):
        self.name = name
        self.total_spent = 0

    def update_spent(self, amount):
        self.total_spent += amount


class User:
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget
        self.expenses = []

    def add_expense(self, expense):
        self.expenses.append(expense)

    def total_spent(self):
        total = 0
        for expense in self.expenses:
            total += expense.amount
        return total

    def check_budget(self):
        money_left = self.budget - self.total_spent()
        if money_left < 0:
            print(f"Over budget!! by Rs.{abs(money_left)}")
        else:
            print(f"Remaining budget: Rs.{money_left}")


class ExpenseTracking:
    FILE_NAME = "expenses.csv"

    def __init__(self, user):
        self.user = user
        self.categories = {}
        self.load_expenses()

    def add_category(self, name):
        if name not in self.categories:
            self.categories[name] = Category(name)

    def add_expense(self, date, category, amount):
        if category not in self.categories:
            print("Category doesn't exist!!! Add category first.")
            return
        expense = Expense(category, amount, date)
        self.user.add_expense(expense)
        self.categories[category].update_spent(amount)
        self.save_expense(expense)
        print("Expense Added.")

    def display_expenses(self):
        if not self.user.expenses:
            print("No expenses found!")
            return
        print("Expense list:")
        for expense in self.user.expenses:
            print(expense)

    def display_summary(self):
        print("\nExpense Summary:")
        for category, cat_obj in self.categories.items():
            print(f"{category}: ₹{cat_obj.total_spent}")
        self.user.check_budget()

    def save_expense(self, expense):
        with open(self.FILE_NAME, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([expense.date, expense.category, expense.amount])

    def load_expenses(self):
        if not os.path.exists(self.FILE_NAME):
            return
        with open(self.FILE_NAME, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                date, category, amount = row
                amount = int(amount)
                self.add_category(category)
                expense = Expense(category, amount, date)
                self.user.add_expense(expense)
                self.categories[category].update_spent(amount)


def main():
    print("====Welcome to Expense Tracker====")
    name = input("Enter your name: ")
    budget = int(input("Enter your monthly budget: "))
    user = User(name, budget)
    tracker = ExpenseTracking(user)

    while True:
        print("1. Add expense")
        print("2. View expenses")
        print("3. View summary")
        print("4. Add expense category")
        print("5. Exit")

        choice = int(input("Enter a valid choice: "))
        if choice == 1:
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category: ")
            amount = int(input("Enter amount: "))
            tracker.add_expense(date, category, amount)
        elif choice == 2:
            tracker.display_expenses()
        elif choice == 3:
            tracker.display_summary()
        elif choice == 4:
            category = input("Enter new category name: ")
            tracker.add_category(category)
            print(f"Category {category} is added!")
        elif choice == 5:
            print("Goodbye!! Have a nice day.")
            break
        else:
            print("Invalid choice!! Please enter a valid choice.")


if __name__ == "__main__":
    main()