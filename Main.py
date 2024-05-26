from flask import Flask, render_template, request, redirect, url_for, flash
import os
import hashlib
import mmap

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# Функція для хешування паролів за допомогою SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# Функція перевірки та створення необхідних файлів, якщо вони не існують
def check_files():
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

    if not os.path.isfile('compromised_passwords_hashed.txt'):
        with open('compromised_passwords.txt', 'r', encoding='utf-8') as original_file:
            with open('compromised_passwords_hashed.txt', 'w', encoding='utf-8') as hashed_file:
                for line in original_file:
                    hashed_file.write(hash_password(line.strip()) + "\n")


check_files()


# Функція для автентифікації користувача
def authenticate(username, password):
    return username == "admin" and password == "admin"


# Функція для завантаження хешованих паролів у набір з використанням mmap для ефективного зчитування
def load_hashed_passwords(file_path):
    hashed_passwords_set = set()
    with open(file_path, 'r+b') as f:
        mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        for line in iter(mmapped_file.readline, b""):
            hashed_passwords_set.add(line.decode('utf-8').strip())
        mmapped_file.close()
    return hashed_passwords_set


# Функція перевірки наявності хешованого паролю в наборі
def is_password_compromised(hashed_password, hashed_passwords_set):
    return hashed_password in hashed_passwords_set


# Основний маршрут для сторінки входу в систему
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


# Маршрут до сторінки перевірки пароля
@app.route('/password_checker', methods=['GET', 'POST'])
def password_checker():
    if request.method == 'POST':
        password_to_check = request.form['password']
        hashed_password = hash_password(password_to_check)
        hashed_passwords_set = load_hashed_passwords('compromised_passwords_hashed.txt')

        if is_password_compromised(hashed_password, hashed_passwords_set):
            flash("Пароль скомпрометований!", "danger")
        else:
            flash("Пароль безпечний.", "success")

    return render_template('password_checker.html')


# Маршрут для відображення скомпрометованих паролів
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


# Маршрут для отримання десятки найгірших паролів 2024 року
@app.route('/get_top_ten_worst_passwords')
def get_top_ten_worst_passwords():
    worst_passwords = [
        "123456",
        "password",
        "123456789",
        "12345678",
        "12345",
        "1234567",
        "111111",
        "123123",
        "qwerty",
        "abc123"
    ]
    return {'passwords': worst_passwords}


if __name__ == '__main__':
    app.run(debug=True)
