from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Перевірка наявності файлів та їх створення при відсутності
def check_files():
    if not os.path.isfile('compromised_passwords.txt'):
        with open('compromised_passwords.txt', 'w') as file:
            file.write("password1\npassword2\npassword3\n")  # Заповнення за замовчуванням

check_files()

# Маршрут для аутентифікації
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

# Маршрут для перевірки пароля
@app.route('/check_password', methods=['POST'])
def check_password():
    data = request.json
    password = data.get('password')
    compromised_passwords = set()

    # Завантаження скомпрометованих паролів з файлу
    with open('compromised_passwords.txt', 'r') as file:
        for line in file:
            compromised_passwords.add(line.strip())

    # Перевірка, чи є введений пароль серед скомпрометованих паролів
    if password in compromised_passwords:
        return jsonify({"compromised": True})
    else:
        return jsonify({"compromised": False})

# Маршрут для отримання скомпрометованих паролів
@app.route('/compromised_passwords', methods=['GET'])
def compromised_passwords():
    compromised_passwords = []

    # Завантаження скомпрометованих паролів з файлу
    with open('compromised_passwords.txt', 'r') as file:
        for line in file:
            compromised_passwords.append(line.strip())

    return jsonify({"compromised_passwords": compromised_passwords})

if __name__ == '__main__':
    app.run(debug=True)
