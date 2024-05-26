from flask import Flask, render_template, request, redirect, url_for, flash
import os
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Функція для хешування паролів за допомогою SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Функція перевірки наявності необхідних файлів та їх створення при відсутності
def check_files():
    # Створення файлу з початковими паролями, якщо він не існує
    if not os.path.isfile('compromised_passwords.txt'):
        with open('compromised_passwords.txt', 'w', encoding='utf-8') as file:
            file.write("password1\n")
            file.write("password2\n")
            file.write("password3\n")
            file.write("password4\n")
            file.write("password5\n")
            file.write("password6\n")
            file.write("password7\n")
            file.write("password8\n")

    # Створення файлу з хешованими паролями, якщо він не існує
    if not os.path.isfile('compromised_passwords_hashed.txt'):
        with open('compromised_passwords.txt', 'r', encoding='utf-8') as original_file:
            with open('compromised_passwords_hashed.txt', 'w', encoding='utf-8') as hashed_file:
                for line in original_file:
                    hashed_file.write(hash_password(line.strip()) + "\n")

check_files()

# Функція аутентифікації користувача
def authenticate(username, password):
    return username == "admin" and password == "admin"

# Маршрут для головної сторінки входу
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if authenticate(username, password):
            flash("Вхід успішний!", "success")
            return redirect(url_for('password_checker'))
        else:
            flash("Неправильний логін або пароль.", "danger")

    return render_template('login.html')

# Маршрут для сторінки перевірки паролів
@app.route('/password_checker', methods=['GET', 'POST'])
def password_checker():
    return render_template('password_checker.html')

# Маршрут для сторінки відображення скомпрометованих паролів
@app.route('/display_compromised_passwords')
def display_compromised_passwords():
    compromised_passwords = []

    with open('compromised_passwords_hashed.txt', 'r', encoding='utf-8') as file:
        for line in file:
            compromised_passwords.append(line.strip())

    return render_template('display_compromised_passwords.html', passwords=compromised_passwords)

# Маршрут для отримання хешованих скомпрометованих паролів
@app.route('/get_compromised_passwords_hashed')
def get_compromised_passwords_hashed():
    with open('compromised_passwords_hashed.txt', 'r', encoding='utf-8') as file:
        data = file.read()
    return data, 200, {'Content-Type': 'text/plain'}

# Маршрут для отримання перших семи паролів без хешування
@app.route('/get_first_seven_passwords')
def get_first_seven_passwords():
    passwords = []
    with open('compromised_passwords.txt', 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i < 7:
                passwords.append(line.strip())
            else:
                break
    return {'passwords': passwords}

if __name__ == '__main__':
    app.run(debug=True)
