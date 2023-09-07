import sqlite3;


# создаем подключение
con = sqlite3.connect("subscribed_users.db")

# получаем курсор
cursor = con.cursor()


# создаем таблицу people
cursor.execute("""CREATE TABLE profiles
                (id INTEGER PRIMARY KEY AUTOINCREMENT,  
                user_id INTEGER UNIQUE,
                user_name TEXT, 
                full_name TEXT)
            """)