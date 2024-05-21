from flask import Flask, render_template, request, redirect, url_for, flash
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Перевірка наявності файлів та їх створення при відсутності
def check_files():
    if not os.path.isfile('compromised_passwords.txt'):
        with open('compromised_passwords.txt', 'w') as file:
            file.write("password1\npassword2\npassword3\n")  # Заповнення за замовчуванням

check_files()

# Функція для перевірки логіна та пароля користувача
def authenticate(username, password):
    # Перевірка логіна та пароля
    return username == "admin" and password == "admin"

# Головна сторінка
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

# Сторінка перевірки паролів
@app.route('/password_checker', methods=['GET', 'POST'])
def password_checker():
    result = ''
    if request.method == 'POST':
        entered_password = request.form['password']
        compromised_passwords = set()

        with open('compromised_passwords.txt', 'r') as file:
            for line in file:
                compromised_passwords.add(line.strip())

        if entered_password in compromised_passwords:
            result = "Ваш пароль небезпечний. Змініть його!"
        else:
            result = "Ваш пароль безпечний."

    return render_template('password_checker.html', result=result)

# Сторінка виведення скомпрометованих паролів
@app.route('/display_compromised_passwords')
def display_compromised_passwords():
    compromised_passwords = []

    with open('compromised_passwords.txt', 'r') as file:
        for line in file:
            compromised_passwords.append(line.strip())

    return render_template('display_compromised_passwords.html', passwords=compromised_passwords)

if __name__ == '__main__':
    app.run(debug=True)