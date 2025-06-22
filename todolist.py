import csv
import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox

class Task:
    def __init__(self, name, description, priority):
        self.name = name
        self.description = description
        self.priority = priority

    def __str__(self):
        return f"{self.name} | {self.description} | {self.priority}"

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

    def save_tasks(self):
        with open(self.filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Name', 'Description', 'Priority'])
            for task in self.tasks:
                writer.writerow([task.name, task.description, task.priority])

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.tasks = [Task(row['Name'], row['Description'], row['Priority']) for row in reader]
        else:
            self.tasks = []

class ToDoApp:
    def __init__(self, root):
        self.todo = ToDoList()
        self.root = root
        self.root.title("مدیریت لیست کارها")
        self.root.geometry("600x600")

        self.name_var = ttk.StringVar()
        self.desc_var = ttk.StringVar()
        self.priority_var = ttk.StringVar(value='متوسط')

        ttk.Label(root, text="📝 لیست کارها", font=("B Titr", 28)).pack(pady=20)

        form_frame = ttk.Frame(root, padding=10)
        form_frame.pack(pady=10)

        ttk.Label(form_frame, text="نام کار:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.name_entry = ttk.Entry(form_frame, textvariable=self.name_var, width=30)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="توضیح:").grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.desc_entry = ttk.Entry(form_frame, textvariable=self.desc_var, width=30)
        self.desc_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="اولویت:").grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.priority_menu = ttk.Combobox(form_frame, textvariable=self.priority_var, values=['بالا', 'متوسط', 'پایین'], width=28)
        self.priority_menu.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(root, text="➕ اضافه کردن", bootstyle=SUCCESS, command=self.add_task).pack(pady=10)

        self.task_listbox = tk.Listbox(root, width=60, height=15, font=("Arial", 12))
        self.task_listbox.pack(pady=20)

        ttk.Button(root, text="🗑️ حذف کار", bootstyle=DANGER, command=self.remove_task).pack(pady=10)

        self.display_tasks()

    def add_task(self):
        name = self.name_var.get()
        desc = self.desc_var.get()
        priority = self.priority_var.get()

        if not name or not desc:
            messagebox.showwarning("خطا", "لطفاً تمام فیلدها را پر کنید.")
            return

        task = Task(name, desc, priority)
        self.todo.add_task(task)
        self.display_tasks()

        self.name_var.set('')
        self.desc_var.set('')
        self.priority_var.set('متوسط')

    def remove_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            task_text = self.task_listbox.get(selected[0])
            task_name = task_text.split(' | ')[0]
            self.todo.remove_task(task_name)
            self.display_tasks()
        else:
            messagebox.showwarning("خطا", "لطفاً یک کار را انتخاب کنید.")

    def display_tasks(self):
        self.task_listbox.delete(0, 'end')
        for task in self.todo.tasks:
            self.task_listbox.insert('end', str(task))

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = ToDoApp(root)
    root.mainloop()
