import sqlite3


def initiate_db():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS Users")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
    )
    """)

    cursor.execute("DROP TABLE IF EXISTS Products")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products(
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        price INTEGER NOT NULL
    )
    """)


def add_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   ("Яблоко", "Чистый мёд!", 10))
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   ("Огурец", "Молодец", 5))
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   ("Помидор", "Сеньор", 8))
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   ("Вишня", "На торте", 12))
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   ("Калина", "Красная", 4))
    cursor.execute("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)",
                   ("Баклажан", "Лада Седан", 7))
    connection.commit()
    connection.close()


def is_included(user: str):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    name = cursor.execute("SELECT username FROM Users WHERE username = ?", (user,)).fetchone()
    if name is None:
        return False
    else:
        return True


def add_user(username, email, age):
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (username, email, age, 1000))
    connection.commit()
    connection.close()


def get_all_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT title, description, price FROM Products")
    product_tuple = cursor.fetchall()
    connection.close()
    return product_tuple


if __name__ == "__main__":
    initiate_db()
    add_products()
    # add_user("Peter", "Peter@mail.ru", 35)
    # add_user("Ivan", "Ivan@mail.ru", 25)
    # add_user("Peter", "Peter@mail.ru", 35)
    # add_user("Ivan", "Ivan@mail.ru", 25)
