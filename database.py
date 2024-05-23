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

    cur.execute("INSERT INTO users (First_name, Last_name, Email, Age, Password) VALUES (%s, %s, %s, %s, %s) "
                "RETURNING id", (first_name, last_name, email, age, password))
    user_id = cur.fetchone()[0]
    conn.commit()

    last_name_initial = last_name.upper()
    first_name_initial = first_name[0].upper()
    table_name = f"{last_name_initial}_{first_name_initial}"

    cur.execute(
        f"CREATE TABLE IF NOT EXISTS {table_name}"
        "(id SERIAL PRIMARY KEY, Date DATE, Time TIME, Measurement NUMERIC(3,1))")
    conn.commit()
    conn.close()

    return "Успешно", user_id


def insert_data(user_id, date, time, measurement):
    success = False
    try:
        conn = psycopg2.connect(dbname="mobile", user="postgres", password="1234", host="localhost", port="5432")
        cur = conn.cursor()

        cur.execute("SELECT first_name, last_name FROM users WHERE id = %s", (user_id,))
        first_name, last_name = cur.fetchone()
        first_name_initial = first_name[0].upper()
        last_name_initial = last_name.upper()
        table_name = f"{last_name_initial}_{first_name_initial}"

        cur.execute(f"INSERT INTO {table_name} (Date, Time, Measurement) VALUES (%s, %s, %s)",
                    (date, time, measurement))
        conn.commit()
        success = True
        conn.close()
    except Exception as e:
        print(f"Error inserting data: {e}")
        success = False

    return success


def authenticate_user(first_name, last_name, password):
    conn = psycopg2.connect(dbname="mobile", user="postgres", password="1234", host="localhost", port="5432")
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE First_name=%s AND Last_name=%s AND Password=%s",
                (first_name, last_name, password))
    result = cur.fetchone()

    conn.close()

    if result is not None:
        return "success"
    else:
        return "error"
