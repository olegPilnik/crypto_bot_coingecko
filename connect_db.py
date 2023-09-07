import sqlite3;


def add_profile_in_db(user_id, user_name, full_name):
    conn = sqlite3.connect("subscribed_users.db")
    cursor = conn.cursor()
    profile = (user_id, user_name, full_name)
    # добавляем строку в таблицу profiles
    cursor.execute(f"INSERT INTO profiles ('user_id', 'user_name', 'full_name') VALUES (?, ?, ?)", profile)
    # выполняем транзакцию
    conn.commit()   

def get_user_id():
    """Функция возвращает все user_id из базы
    в виде списка кортежей"""
    conn = sqlite3.connect("subscribed_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM profiles")
    return cursor.fetchall()