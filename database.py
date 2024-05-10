import psycopg2


def create_db():
    conn = psycopg2.connect(dbname="mobile", user="postgres", password="1234", host="localhost", port="5432",
                            options="-c client_encoding=UTF8")

    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            First_name VARCHAR(255) NOT NULL,
            Last_name VARCHAR(255) NOT NULL,
            Email VARCHAR(255) NOT NULL,
            Age INTEGER,
            Password VARCHAR(255) NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_new_user_to_db(first_name, last_name, email, age, password):
    conn = psycopg2.connect(dbname="mobile", user="postgres", password="1234", host="localhost", port="5432")
    cur = conn.cursor()
    # Вставка нового пользователя в таблицу
    cur.execute("INSERT INTO users (First_name, Last_name, Email, Age, Password) VALUES (%s, %s, %s, %s, %s) "
                "RETURNING id", (first_name, last_name, email, age, password))
    user_id = cur.fetchone()[0]
    conn.commit()

    # Создание таблицы для пользователя с идентификатором user_id
    cur.execute(
        "CREATE TABLE IF NOT EXISTS user_{} "
        "(id SERIAL PRIMARY KEY, Date DATE, Time TIME, Measurement NUMERIC(3,1))".format(user_id))
    conn.commit()
    conn.close()

    return "Успешно", user_id


def insert_data(user_id, date, time, measurement):
    success = False
    try:
        conn = psycopg2.connect(dbname="mobile", user="postgres", password="1234", host="localhost", port="5432")
        cur = conn.cursor()
        cur.execute("INSERT INTO user_{} (Date, Time, Measurement) VALUES (%s, %s, %s)".format(str(user_id)),
                    (date, time, measurement))
        conn.commit()
        success = True
    except Exception as e:
        print(f"Error inserting data: {e}")
    finally:
        conn.close()

    return success


def authenticate_user(first_name, last_name, password):
    conn = psycopg2.connect(dbname="mobile", user="postgres", password="1234", host="localhost", port="5432")
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE First_name=%s AND Last_name=%s AND Password=%s",
                (first_name, last_name, password))
    result = cur.fetchone()

    conn.close()

    if result is None:
        return "Неудача", None
    else:
        return "Успешно", result[0]
