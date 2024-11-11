import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()

# будем создавать таблицу заново при каждом запуске программы, так удобнее
cursor.execute("DROP TABLE IF EXISTS Users")

# "Создание БД, добавление, выбор и удаление элементов." Предыдущая задача

# Создайте таблицу Users, если она ещё не создана.
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
""")

cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")

# Заполните её 10 записями:
for i in range(1, 11):
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)",
                   (f"User{i}", f"example{i}@gmail.com", i*10, 1000))

# Обновите balance у каждой 2ой записи начиная с 1ой на 500:
for i in range(1, 11, 2):
    cursor.execute("UPDATE Users SET balance = ? WHERE username = ?", (500, f"User{i}"))

# Удалите каждую 3ую запись в таблице начиная с 1ой:
for i in range(1, 11, 3):
    cursor.execute("DELETE FROM Users WHERE username=?", (f"User{i}", ))

# Сделайте выборку всех записей при помощи fetchall(), где возраст не равен 60
# и выведите их в консоль в следующем формате (без id):
# Имя: <username> | Почта: <email> | Возраст: <age> | Баланс: <balance>
cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != ?", (60,))
users = cursor.fetchall()
for user_tuple in users:
    print(f"Имя: {user_tuple[0]} | Почта: {user_tuple[1]} | Возраст: {user_tuple[2]} | Баланс: {user_tuple[3]}")

# "Выбор элементов и функции в SQL запросах" Текущая задача

# Удалите из базы данных not_telegram.db запись с id = 6.
cursor.execute("DELETE FROM Users WHERE id=?", (6, ))

# Подсчитать общее количество записей.
cursor.execute("SELECT COUNT(*) FROM Users")
total_users = cursor.fetchone()[0]
print(total_users)

# Посчитать сумму всех балансов.
cursor.execute("SELECT SUM(balance) FROM Users")
all_balances = cursor.fetchone()[0]
print(all_balances)

# Вывести в консоль средний баланс всех пользователей.
cursor.execute("SELECT AVG(balance) FROM Users")
avg_balances = cursor.fetchone()[0]
print(avg_balances, all_balances/total_users)

connection.commit()
connection.close()