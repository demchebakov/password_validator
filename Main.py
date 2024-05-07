import tkinter as tk
from tkinter import messagebox
import os

# Перевірка наявності файлів та їх створення при відсутності
def check_files():
    if not os.path.isfile('compromised_passwords.txt'):
        with open('compromised_passwords.txt', 'w') as file:
            file.write("password1\npassword2\npassword3\n")  # Заповнення за замовчуванням

# Функція для перевірки логіна та пароля користувача
def authenticate(username, password):
    # Перевірка логіна та пароля
    if username == "admin" and password == "admin":
        return True
    else:
        return False

# Функція для обробки події натискання кнопки "Увійти"
def login():
    username = username_entry.get()
    password = password_entry.get()

    # Перевірка логіна та пароля користувача
    if authenticate(username, password):
        messagebox.showinfo("Успіх", "Вхід успішний!")
        open_password_checker_window()
    else:
        messagebox.showerror("Помилка", "Неправильний логін або пароль.")

# Функція для відкриття вікна перевірки паролів
def open_password_checker_window():
    password_checker_window = tk.Toplevel(root)
    password_checker_window.title("Перевірка паролів")

    # Поля для введення паролю та виводу результату
    password_label = tk.Label(password_checker_window, text="Введіть пароль:")
    password_label.pack()

    password_entry = tk.Entry(password_checker_window, show="*")
    password_entry.pack()

    result_label = tk.Label(password_checker_window, text="")
    result_label.pack()

    # Функція для перевірки пароля
    def check_password():
        entered_password = password_entry.get()
        compromised_passwords = set()

        # Завантаження скомпрометованих паролів з файлу
        with open('compromised_passwords.txt', 'r') as file:
            for line in file:
                compromised_passwords.add(line.strip())

        # Перевірка, чи є введений пароль серед скомпрометованих паролів
        if entered_password in compromised_passwords:
            result_label.config(text="Ваш пароль небезпечний. Змініть його!")
        else:
            result_label.config(text="Ваш пароль безпечний.")

    check_button = tk.Button(password_checker_window, text="Перевірити", command=check_password)
    check_button.pack()

    # Кнопка для виведення скомпрометованих паролів
    display_button = tk.Button(password_checker_window, text="Вивести скомпрометовані паролі", command=display_compromised_passwords)
    display_button.pack()

# Функція для виведення скомпрометованих паролів
def display_compromised_passwords():
    compromised_passwords = []

    # Завантаження скомпрометованих паролів з файлу
    with open('compromised_passwords.txt', 'r') as file:
        for line in file:
            compromised_passwords.append(line.strip())

    # Виведення списку скомпрометованих паролів
    messagebox.showinfo("Скомпрометовані паролі", "\n".join(compromised_passwords))

# Створення головного графічного інтерфейсу
root = tk.Tk()
root.title("Авторизація")

# Перевірка наявності файлів та їх створення
check_files()

# Поля для введення логіна та пароля
username_label = tk.Label(root, text="Логін:")
username_label.grid(row=0, column=0, sticky="e")
username_entry = tk.Entry(root)
username_entry.grid(row=0, column=1)

password_label = tk.Label(root, text="Пароль:")
password_label.grid(row=1, column=0, sticky="e")
password_entry = tk.Entry(root, show="*")
password_entry.grid(row=1, column=1)

# Кнопка "Увійти"
login_button = tk.Button(root, text="Увійти", command=login)
login_button.grid(row=2, column=1, pady=5)

root.mainloop()