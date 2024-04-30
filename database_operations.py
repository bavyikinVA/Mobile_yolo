import sqlite3


def create_local_db():
    # Устанавливаем соединение с базой данных
    connection = sqlite3.connect('Glucocheck.db')
    cursor = connection.cursor()
    # Создаем таблицу Users на устройстве
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Users (
    id INTEGER PRIMARY KEY,
    User_first_name TEXT NOT NULL,
    User_last_name TEXT NOT NULL,
    Password TEXT NOT NULL,
    Email TEXT NOT NULL,
    Age INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Data_dimensions (
    id INTEGER PRIMARY KEY,
    date TEXT NOT NULL,
    time TEXT NOT NULL,
    dimension REAL
    )
    ''')
    connection.commit()
    connection.close()


def check_personal(first_name, last_name, password):
    connection = sqlite3.connect('Glucocheck.db')
    cursor = connection.cursor()
    cursor.execute('SELECT User_first_name, User_last_name, Password FROM Users')
    users = cursor.fetchall()

    for fname, lname, pw in users:
        if first_name == fname and lname == last_name and password == pw:
            return "Успешно"
        else:
            return "Ошибка ввода данных"


def register_in_db(fname, lname, email_input, age_input, password_input):
    connection = sqlite3.connect('Glucocheck.db')
    cursor = connection.cursor()
    # Добавляем нового пользователя
    cursor.execute('INSERT INTO Users (User_first_name, User_last_name, Password, email, age) VALUES (?, ?, ?, ?, ?)',
                   (fname, lname, password_input, email_input, age_input))

    connection.commit()
    connection.close()
    return "Успешно"


def add_data_in_dimens_table(date, time, dimension):
    connection = sqlite3.connect('Glucocheck.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Data_dimensions (date, time, dimension) VALUES (?, ?, ?)',
                   (date, time, dimension))
    connection.commit()
    connection.close()
    return "Сохранено"
