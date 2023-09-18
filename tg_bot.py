import telebot
from telebot import types

from dotenv import load_dotenv
import os

from connect_db import add_profile_in_db, get_user_id, get_exchanges
from connect_db import add_selected_exchanges_in_db, delete_selected_exchanges

from main_process import main, new_data

import threading # модуль для запуска нескольких потоков

from time import sleep

import logging

logging.basicConfig(
    level=logging.INFO,
    filename='log_file.log',
    filemode='a',
    format='%(asctime)s %(levelname)s %(message)s'
)

load_dotenv('.env')

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def subscribe(message):
    # Добавляем пользователя
    user_id = message.from_user.id
    user_name = message.from_user.username
    full_name = message.from_user.full_name
    """Записываем в базу профиль"""
    try:
        add_profile_in_db(user_id, user_name, full_name)
        bot.send_message(user_id, "Ви підписались на повідомлення від CryptoBot.")
    except Exception as ex: 
        logging.info(f'{ex}: {user_id}')
        bot.send_message(user_id, "Ви вже підписані на повідомлення від CryptoBot.")


# Создаем Inline-клавиатуру
keyboard = types.InlineKeyboardMarkup()

"""Проходим циклом по всем биржам из базы и создаем кнопки с наизваниями бирж"""
for item in  get_exchanges():
    button = types.InlineKeyboardButton(f'{item[2]} ✅', callback_data= f'{item[1]},{item[2]}')
    keyboard.add(button)


# Обработчик команды /select_exchanges для отправки клавиатуры с кнопками
@bot.message_handler(commands=['selected_exchanges'])
def send_keyboard(message):
    delete_selected_exchanges() # Функция очистки временной таблицы с биржами selected_exchanges
    bot.send_message(message.chat.id, "Оберіть біржі:", reply_markup=keyboard)
    

# Обработчик нажатий на инлайн-кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    exchange = call.data.split(',')
    exchange_id = exchange[0]
    exchange_name = exchange[1]
    try:
        add_selected_exchanges_in_db(exchange_id, exchange_name)
        bot.send_message(call.message.chat.id, f"Ви обрали біржу: {exchange_name}")
    except Exception as ex:
        logging.info(ex)
        bot.send_message(call.message.chat.id, f"Ви вже обрали біржу {exchange_name}")
        
    
    





# for item in get_exchanges():
        # if call.data == str(item[0]):
        #     data_from_database = add_selected_exchanges_in_db(item[1], item[2])
        #     bot.send_message(call.message.chat.id, data_from_database)

        # else:
        #     pass
        # call.data == '2':
        #     data_from_database = add_selected_exchanges_in_db(item[1], item[2])
        #     bot.send_message(call.message.chat.id, data_from_database)

        # elif call.data == '3':
        #     data_from_database = add_selected_exchanges_in_db(item[1], item[2])
        #     bot.send_message(call.message.chat.id, data_from_database)

        # elif call.data == '4':
        #     data_from_database = add_selected_exchanges_in_db(item[1], item[2])
        #     bot.send_message(call.message.chat.id, data_from_database)

        # elif call.data == '5':
        #     data_from_database = add_selected_exchanges_in_db(item[1], item[2])
        #     bot.send_message(call.message.chat.id, data_from_database)

        # elif call.data == '6':
        #     data_from_database = add_selected_exchanges_in_db(item[1], item[2])
        #     bot.send_message(call.message.chat.id, data_from_database)

        # elif call.data == '7':
        #     data_from_database = add_selected_exchanges_in_db(item[1], item[2])
        #     bot.send_message(call.message.chat.id, data_from_database)

        # elif call.data == '8':
        #     data_from_database = add_selected_exchanges_in_db(item[1], item[2])
        #     bot.send_message(call.message.chat.id, data_from_database)
        
        # elif call.data == '9':
        #     data_from_database = add_selected_exchanges_in_db(item[1], item[2])
        #     bot.send_message(call.message.chat.id, data_from_database)

        # elif call.data == '10':
        #     data_from_database = add_selected_exchanges_in_db(item[1], item[2])
        #     bot.send_message(call.message.chat.id, data_from_database)

        # elif call.data == '11':
        #     data_from_database = add_selected_exchanges_in_db(item[1], item[2])
        #     bot.send_message(call.message.chat.id, data_from_database)
        
        # elif call.data == '12':
        #     data_from_database = add_selected_exchanges_in_db(item[1], item[2])
        #     bot.send_message(call.message.chat.id, data_from_database)


              
        #     # Выбран вариант 1 - выполните действия с данными из базы данных, например, выберите их и отправьте пользователю
        #     data_from_database = "Данные из базы данных для Варианта 1"
        #     bot.send_message(call.message.chat.id, data_from_database)
        # elif call.data == "option2":
        #     # Выбран вариант 2 - выполните действия с данными из базы данных для этого варианта
        #     data_from_database = "Данные из базы данных для Варианта 2"
        #     bot.send_message(call.message.chat.id, data_from_database)
        # elif call.data == "option3":
        #     # Выбран вариант 3 - выполните действия с данными из базы данных для этого варианта
        #     data_from_database = "Данные из базы данных для Варианта 3"
        #     bot.send_message(call.message.chat.id, data_from_database)












 
# # Обработчик команды /spread (Выводит сообщение с просьбой ввести Spread и перенаправляет к следующему шагу)
# @bot.message_handler(commands=['stop'])
# def comand_stop(message):
#     stop = True
#     # msg = bot.send_message(message.chat.id, "Введіть значення 'Spread' від 1 до 8 %: ")
#     # bot.register_next_step_handler(msg, input_spread)

# # def input_spread(message):
# #     min_spread = message.text
# #     main_thread.stop()
# #     #     bot.register_next_step_handler(msg, input_spread)



# # Обработчик команды /start_app (Запускает приложение)
# @bot.message_handler(commands=['start_app'])
# def comand_start_app(message):
#     msg = bot.send_message(message.chat.id, "Введіть значення 'Spread' від 1 до 8 %: ")
#     bot.register_next_step_handler(msg, input_spread)


# def input_spread(message):
#     min_spread = message.text
#     main_thread = threading.Thread(target=main, args=(min_spread, ))
#     main_thread.start()
    




def send_data():
    """Функция для отправки данных 
    пользователям (не асинхронная)"""
    while True:
        if new_data:
            data_to_send = new_data.pop(0)
            #  Открываем файл со списком пользователей
            for element in get_user_id():
                userid = element[0]
                bot.send_message(userid, str(data_to_send))
        sleep(2)  # Пауза между проверками новых данных




# Запуск бота в отдельном потоке
def bot_polling():
    bot.polling()


"""Запуск основных функций в отдельных потоках"""
main_thread = threading.Thread(target=main)
send_data_thread = threading.Thread(target=send_data)
bot_thread = threading.Thread(target=bot_polling)



main_thread.start()
send_data_thread.start()
bot_thread.start()