import csv
import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from datetime import datetime

class Task:
    def __init__(self, name, description, priority, timestamp=None):
        self.name = name
        self.description = description
        self.priority = priority
        self.timestamp = timestamp if timestamp else datetime.now().strftime('%Y-%m-%d %H:%M')

    def __str__(self):
        return f"{self.name} | {self.description} | {self.priority} | {self.timestamp}"

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
            writer.writerow(['Name', 'Description', 'Priority', 'Timestamp'])
            for task in self.tasks:
                writer.writerow([task.name, task.description, task.priority, task.timestamp])

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                self.tasks = [
                    Task(row['Name'], row['Description'], row['Priority'], row['Timestamp'])
                    for row in reader
                ]
        else:
            self.tasks = []

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.current_theme = 'flatly'  # تم پیشفرض
        self.style = ttk.Style()
        self.style.theme_use(self.current_theme)

        self.todo = ToDoList()

        self.root.title("✨ لیست کارهای من")
        self.root.geometry("850x700")
        self.root.resizable(False, False)

        # Variables
        self.name_var = ttk.StringVar()
        self.desc_var = ttk.StringVar()
        self.priority_var = ttk.StringVar(value='متوسط')
        self.theme_var = ttk.StringVar(value=self.current_theme)

        # Theme selector
        theme_frame = ttk.Frame(root)
        theme_frame.pack(pady=10, padx=15, fill='x', anchor='e')

        ttk.Label(theme_frame, text="🎨 انتخاب تم:", font=("Vazir", 13)).pack(side='right')
        self.theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var,
                                        values=['flatly', 'superhero', 'cyborg', 'darkly', 'solar', 'litera'],
                                        width=15, font=("Vazir", 12), state='readonly')
        self.theme_combo.pack(side='right', padx=10)
        self.theme_combo.bind("<<ComboboxSelected>>", self.change_theme)

        # Title
        ttk.Label(root, text="📝 لیست کارهای من", font=("B Titr", 30), bootstyle=INFO).pack(pady=10)

        # Form frame
        self.form_frame = ttk.Frame(root, padding=15, bootstyle=INFO, borderwidth=1, relief="ridge")
        self.form_frame.pack(pady=10, padx=20, fill='x')

        # Name input
        ttk.Label(self.form_frame, text="نام کار:", font=("Vazir", 14)).grid(row=0, column=0, padx=8, pady=8, sticky='w')
        self.name_entry = ttk.Entry(self.form_frame, textvariable=self.name_var, width=35, font=("Vazir", 13))
        self.name_entry.grid(row=0, column=1, padx=8, pady=8)

        # Description input
        ttk.Label(self.form_frame, text="توضیح:", font=("Vazir", 14)).grid(row=1, column=0, padx=8, pady=8, sticky='w')
        self.desc_entry = ttk.Entry(self.form_frame, textvariable=self.desc_var, width=35, font=("Vazir", 13))
        self.desc_entry.grid(row=1, column=1, padx=8, pady=8)

        # Priority input
        ttk.Label(self.form_frame, text="اولویت:", font=("Vazir", 14)).grid(row=2, column=0, padx=8, pady=8, sticky='w')
        self.priority_menu = ttk.Combobox(self.form_frame, textvariable=self.priority_var,
                                          values=['بالا', 'متوسط', 'پایین'], width=33, font=("Vazir", 13))
        self.priority_menu.grid(row=2, column=1, padx=8, pady=8)

        # Buttons frame (add + remove)
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        self.add_button = ttk.Button(btn_frame, text="➕ اضافه کردن", bootstyle="success-outline", command=self.add_task, width=18)
        self.add_button.grid(row=0, column=0, padx=12)

        self.remove_button = ttk.Button(btn_frame, text="🗑️ حذف کار", bootstyle="danger-outline", command=self.remove_task, width=18)
        self.remove_button.grid(row=0, column=1, padx=12)

        # Listbox container frame
        listbox_container = ttk.Frame(root, padding=5, bootstyle=SECONDARY)
        listbox_container.pack(padx=20, pady=10, fill='both', expand=True)

        self.scrollbar = ttk.Scrollbar(listbox_container)
        self.scrollbar.pack(side='right', fill='y')

        bg_color = self.style.lookup('TFrame', 'background')

        self.task_listbox = tk.Listbox(
            listbox_container, width=90, height=15, font=("Vazir", 14),
            yscrollcommand=self.scrollbar.set,
            selectbackground='#4CAF50',
            activestyle='none',
            bd=0,
            highlightthickness=0,
            bg=bg_color,
            fg="#222"
        )
        self.task_listbox.pack(side='left', fill='both', expand=True)
        self.scrollbar.config(command=self.task_listbox.yview)

        # Task counter
        self.counter_label = ttk.Label(root, text="تعداد کارها: 0", font=("Vazir", 16), bootstyle=SECONDARY)
        self.counter_label.pack(pady=10)

        self.display_tasks()

    def change_theme(self, event=None):
        new_theme = self.theme_var.get()
        self.style.theme_use(new_theme)
        self.current_theme = new_theme
        bg_color = self.style.lookup('TFrame', 'background')
        self.task_listbox.config(bg=bg_color)

    def add_task(self):
        name = self.name_var.get().strip()
        desc = self.desc_var.get().strip()
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

        messagebox.showinfo("موفق", "✅ کار با موفقیت اضافه شد.")

    def remove_task(self):
        selected = self.task_listbox.curselection()
        if selected:
            task_text = self.task_listbox.get(selected[0])
            task_name = task_text.split(' | ')[0]
            if self.todo.remove_task(task_name):
                self.display_tasks()
                messagebox.showinfo("موفق", "🗑️ کار با موفقیت حذف شد.")
            else:
                messagebox.showerror("خطا", "حذف کار موفقیت‌آمیز نبود.")
        else:
            messagebox.showwarning("خطا", "لطفاً یک کار را انتخاب کنید.")

    def display_tasks(self):
        self.task_listbox.delete(0, 'end')
        for task in self.todo.tasks:
            display_text = f"{task.name} | {task.description} | {task.priority} | {task.timestamp}"
            self.task_listbox.insert('end', display_text)

            index = self.task_listbox.size() - 1
            # رنگ متن اولویت‌ها
            if task.priority == 'بالا':
                self.task_listbox.itemconfig(index, fg='red')
            elif task.priority == 'متوسط':
                self.task_listbox.itemconfig(index, fg='orange')
            elif task.priority == 'پایین':
                self.task_listbox.itemconfig(index, fg='green')

        self.counter_label.config(text=f"تعداد کارها: {len(self.todo.tasks)}")

if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = ToDoApp(root)
    root.mainloop()
