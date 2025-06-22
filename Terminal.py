import csv

class Task:
    def __init__(self, name, description, priority):
        self.name = name
        self.description = description
        self.priority = priority

    def __str__(self):
        return f"نام: {self.name} | توضیح: {self.description} | اولویت: {self.priority}"


class ToDoList:
    def __init__(self, filename='tasks.csv'):
        self.tasks = []
        self.filename = filename
        self.load_tasks()

    def add_task(self, task):
        self.tasks.append(task)
        self.save_tasks()

    def remove_task(self, task_name):
        for task in self.tasks:
            if task.name == task_name:
                self.tasks.remove(task)
                self.save_tasks()
                return True
        return False

    def display_tasks(self):
        if not self.tasks:
            print("لیست کارها خالی است.")
        else:
            print("🔹 لیست کارها:")
            for idx, task in enumerate(self.tasks, start=1):
                print(f"{idx}. {task}")

    def save_tasks(self):
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Description', 'Priority'])
            for task in self.tasks:
                writer.writerow([task.name, task.description, task.priority])

    def load_tasks(self):
        try:
            with open(self.filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.tasks = [
                    Task(row['Name'], row['Description'], row['Priority'])
                    for row in reader
                ]
        except FileNotFoundError:
            self.tasks = []


def main_menu():
    todo = ToDoList()

    while True:
        print("\n=== منوی مدیریت لیست کارها ===")
        print("1. اضافه کردن کار جدید")
        print("2. حذف کار")
        print("3. مشاهده لیست کارها")
        print("4. خروج")

        choice = input("انتخاب شما: ")

        if choice == '1':
            name = input("نام کار: ")
            description = input("توضیح: ")
            priority = input("اولویت (بالا/متوسط/پایین): ")
            task = Task(name, description, priority)
            todo.add_task(task)
            print("✅ کار اضافه شد.")

        elif choice == '2':
            name = input("نام کاری که می‌خواهید حذف کنید: ")
            if todo.remove_task(name):
                print("🗑️ کار حذف شد.")
            else:
                print("❌ کار پیدا نشد.")

        elif choice == '3':
            todo.display_tasks()

        elif choice == '4':
            print("خروج از برنامه. خداحافظ!")
            break

        else:
            print("لطفاً یک گزینه معتبر وارد کنید.")


if __name__ == '__main__':
    main_menu()

