from flask import Flask, request, jsonify
import os
import hashlib

app = Flask(__name__)

# Функція для хешування паролів за допомогою SHA-256
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Функція перевірки наявності необхідних файлів та їх створення при відсутності
def check_files():
    # Створення файлу з хешованими паролями, якщо він не існує
    if not os.path.isfile('compromised_passwords_hashed.txt'):
        with open('compromised_passwords_hashed.txt', 'w', encoding='utf-8') as file:
            file.write(hash_password("password1") + "\n")
            file.write(hash_password("password2") + "\n")
            file.write(hash_password("password3") + "\n")

check_files()

# Маршрут для аутентифікації користувача
@app.route('/authenticate', methods=['POST'])
def authenticate():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Перевірка логіна та пароля
    if username == "admin" and password == "admin":
        return jsonify({"authenticated": True})
    else:
        return jsonify({"authenticated": False})

# Маршрут для перевірки пароля на скомпрометованість
@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.json
    password = data.get('password')
    hashed_password = hash_password(password)
    compromised_passwords = set()

    # Завантаження скомпрометованих паролів з файлу
    with open('compromised_passwords_hashed.txt', 'r', encoding='utf-8') as file:
        for line in file:
            compromised_passwords.add(line.strip())

    # Перевірка, чи є введений пароль серед скомпрометованих паролів
    if hashed_password in compromised_passwords:
        return jsonify({"compromised": True})
    else:
        return jsonify({"compromised": False})

# Маршрут для отримання хешованих скомпрометованих паролів
@app.route('/compromised_passwords', methods=['GET'])
def compromised_passwords():
    compromised_passwords = []

    # Завантаження скомпрометованих паролів з файлу
    with open('compromised_passwords_hashed.txt', 'r', encoding='utf-8') as file:
        for line in file:
            compromised_passwords.append(line.strip())

    return jsonify({"compromised_passwords": compromised_passwords})

if __name__ == '__main__':
    app.run(debug=True)
