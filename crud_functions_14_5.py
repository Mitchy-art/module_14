import sqlite3

connection = sqlite3.connect('initiate_14_5.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER NOT NULL,
balance INTEGER NOT NULL
)
''')

cursor.execute('CREATE INDEX IF NOT EXISTS idx_email ON Users(email)')


def add_user(username, email, age):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)',
                       (f'{username}', f'{email}', age, 1000))


def is_included(username):
    users = cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    if users.fetchone() is None:
        return True
    else:
        return False


connection.commit()
#connection.close()
