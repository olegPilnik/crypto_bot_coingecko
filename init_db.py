import sqlite3;
"""Модуль для создания таблиц
раскоментировать если нужно пересоздать таблицу, 
данные будут очищенны"""


# создаем подключение
con = sqlite3.connect("crypto_bot.db")

# получаем курсор
cursor = con.cursor()

# cursor.execute("""DROP TABLE IF EXISTS profiles;""")
# cursor.execute("""DROP TABLE IF EXISTS exchanges;""")
# cursor.execute("""DROP TABLE IF EXISTS selected_exchanges;""")
# cursor.execute("""DROP TABLE IF EXISTS coins;""")

# создаем таблицу profiles
# cursor.execute("""CREATE TABLE profiles
#                 (id INTEGER PRIMARY KEY AUTOINCREMENT,  
#                 user_id INTEGER UNIQUE,
#                 user_name TEXT, 
#                 full_name TEXT)
#             """)

# создаем таблицу exchanges
# cursor.execute("""CREATE TABLE exchanges
#                 (id INTEGER PRIMARY KEY AUTOINCREMENT,  
#                 exchange_id TEXT UNIQUE, 
#                 exchange_name TEXT)
#             """)

# создаем таблицу selected_exchanges
# cursor.execute("""CREATE TABLE selected_exchanges  
#                 (exchange_id TEXT PRIMARY KEY, 
#                 exchange_name TEXT)
#             """)

# создаем таблицу coins
# cursor.execute("""CREATE TABLE coins  
#                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                  coin_id TEXT UNIQUE, 
#                  symbol TEXT,
#                  name TEXT)
#             """)