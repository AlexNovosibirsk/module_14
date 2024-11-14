import sqlite3


def initiate_db():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("DROP TABLE IF EXISTS Products")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    """)

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


def get_all_products():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT title, description, price FROM Products")
    product_tuple = cursor.fetchall()
    connection.close()
    return product_tuple

if __name__ == "__main__":
    initiate_db()
