import sqlite3;

def connection():
    conn = sqlite3.connect("crypto_bot.db")
    return conn


def add_profile_in_db(user_id, user_name, full_name): 
    """Функция для добавления новых пользователей в базу"""  
    conn = connection()  # Создаем соединение
    cursor = conn.cursor()  # Создаем курсор
    profile = (user_id, user_name, full_name)
    # добавляем строку в таблицу profiles
    cursor.execute("""INSERT INTO profiles ('user_id', 'user_name', 'full_name') VALUES (?, ?, ?);""", profile)
    # выполняем транзакцию
    conn.commit()   

def get_user_id():
    """Функция возвращает все user_id из базы
    в виде списка кортежей"""
    conn = connection()  # Создаем соединение
    cursor = conn.cursor()  # Создаем курсор
    cursor.execute("""SELECT user_id FROM profiles;""")
    return cursor.fetchall()

def get_exchanges():
    """Функция возвращает все exchanges из базы
    в виде списка кортежей, эти exchange будут 
    отображаться на кнопках из которых будет 
    выбирать пользователь"""
    conn = connection()  # Создаем соединение
    cursor = conn.cursor()  # Создаем курсор
    cursor.execute("""SELECT * FROM exchanges;""")
    return cursor.fetchall()



def add_selected_exchanges_in_db(exchange_id, exchange_name):
    """Функция добавления выбранных бирж во временную таблицу"""
    conn = connection()  # Создаем соединение
    cursor = conn.cursor()  # Создаем курсор
    exchange = (exchange_id, exchange_name)
    # добавляем строку в таблицу selected_exchanges
    cursor.execute("""INSERT INTO selected_exchanges ('exchange_id', 'exchange_name') VALUES (?, ?);""", exchange)
    # выполняем транзакцию
    conn.commit()   

def delete_selected_exchanges():
    """Функция для очищения временной таблицы"""
    conn = connection()  # Создаем соединение
    cursor = conn.cursor()  # Создаем курсор
    cursor.execute("""DELETE FROM selected_exchanges;""")
    conn.commit()  # Выполняем коммит транзакции

def get_selected_exchanges():
    """Функция возвращает все  выбранные пользователем 
    биржи из базы в виде списка кортежей, эти биржи будут 
    использоваться в проверке монет"""
    conn = connection()  # Создаем соединение
    cursor = conn.cursor()  # Создаем курсор
    cursor.execute("""SELECT * FROM selected_exchanges;""")
    result = cursor.fetchall()
    return result


def get_row_count_table_coins():
    """Функция возвращает количество строк в таблице 
    coins в виде списка кортежей""" 
    conn = connection()  # Создаем соединение
    cursor = conn.cursor()  # Создаем курсор
    cursor.execute("""SELECT COUNT (*) FROM coins;""")
    row_count = cursor.fetchone()
    return row_count[0]


def get_coin(id): 
    """Функция возвращает coin из базы
    по id в виде кортежа"""  
    conn = connection()  # Создаем соединение
    cursor = conn.cursor()  # Создаем курсор
    cursor.execute("""SELECT * FROM coins WHERE id = ?;""", (id, ))
    result = cursor.fetchone()
    return result
       