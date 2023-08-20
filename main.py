from flask import Flask

import pandas as pd
from coingecko_api import get_data
from coin_functions import sorting_coins
from time import sleep

import telebot
import threading

from dotenv import load_dotenv
import os

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

new_data = []

# Отслеживаем подписанных пользователей
subscribed_users = set()    

# Обработчик команды /start telebot
@bot.message_handler(commands=['start'])
def subscribe(message):
    # Добавляем пользователя в список подписанных
    subscribed_users.add(message.chat.id)
    bot.send_message(message.chat.id, "Ви підписались на повідомлення про нові данні.")


def main():
    """Загружаем все монеты в DataFrame df_coins, 752 монеты"""
    df_coins = pd.read_csv('coins_list_752.csv', index_col='num')
    logging.info(f'В базе всего {len(df_coins)} монет')
    number_cycle = 1 # проверить присвоение !!!!!!!!!
    while True:
        id_coin= 1
    
        """Проходим циклом по монетам"""
        while id_coin <= len(df_coins): # перебираем индексы от 1 до последнего в базе с монетами (752)
            coin_id = df_coins.loc[id_coin]['id'] #  записываем в переменную coin_id значение ключа id из списка
            coin_name = df_coins.loc[id_coin]['name']        #  записываем в переменную coin_name значение ключа name из базы
            logging.info(f'Проверяю монету # {id_coin} : {coin_name}')

            """ Создаем дата фрейм"""
            df_tickers = pd.DataFrame(columns=['coin_id',
                                                'target_coin_id',
                                                'price',
                                                'volume',
                                                'exchange',
                                                'link_tickers'])
            
            data = get_data(coin_id) # Получаем данные о монете с API coingecko
            if data is not None:
                logging.info(f'COIN {coin_name} DATA is TRUE')
                """Сортируем данные в список словарей"""
                lst_tickers = sorting_coins(data, coin_id)

                if len(lst_tickers) > 0:
                    """С помощью метода from_records добавляем список словарей в DataFrame df_tickers"""
                    df_tickers = pd.concat([df_tickers, pd.DataFrame.from_records(lst_tickers)], ignore_index=True)
                    # df_tickers.to_csv(f'df_tickers{coin_name}.csv', index=True)
                
                    """Возвращаю максисальную и минимальную цену монеты"""
                    price_min = df_tickers['price'].min()
                    price_max = df_tickers['price'].max()
                    spread = round(((price_max - price_min)/ price_min) * 100, 3)
                    if spread >= 10:
                        """Возвращаем в виде фреймов строки с 
                        "price" == price_max и "price" == price_min"""
                        df_min = df_tickers[df_tickers['price'] == price_min]
                        df_max = df_tickers[df_tickers['price'] == price_max]
                       

                        """Создаем словарь для возврата пользователю"""
                        return_dict = {}
                        return_dict['coin'] = coin_name
                        return_dict['target_coin'] = df_min.iloc[0]['target_coin_id']
                        return_dict['datetime'] = df_min.iloc[0]['datetime']



                        return_dict['pr_min_exchange'] = df_min.iloc[0]['exchange']
                        return_dict['ex_min_volume'] = df_min.iloc[0]['volume']
                        return_dict['price_min'] = price_min
                        return_dict['pr_min_link'] = df_min.iloc[0]['link_tickers']
                        
                        
                        return_dict['pr_max_exchange'] = df_max.iloc[0]['exchange']
                        return_dict['ex_max_volume'] = df_max.iloc[0]['volume']
                        return_dict['price_max'] = price_max
                        return_dict['pr_max_link'] = df_max.iloc[0]['link_tickers']
                        
                        
                        return_dict['spread'] = spread

                        return_str = (f"Актив: {return_dict['coin']}\\USDT\
                                      Дата: {return_dict['datetime']}\
                                     Біржа1: {return_dict['pr_min_exchange']}\
                                     Об'єм: {return_dict['ex_min_volume']}\
                                     Вартість: {return_dict['price_min']}\
                                     Посилання: {return_dict['pr_min_link']}\n\
                                    \
                                     Біржа2: {return_dict['pr_max_exchange']}\
                                     Об'єм: {return_dict['ex_max_volume']}\
                                     Вартість: {return_dict['price_max']}\
                                     Посилання: {return_dict['pr_max_link']}\
                                     Спред: {return_dict['spread']}")
                        
                        """Добавляем строку в список new_data"""
                        new_data.append(return_str)
                        
                else:
                    logging.info(f'COIN {coin_name} EMPTY lst_tickers')

            else:
                print('Please wait 90 seconds')
                logging.info(f'COIN {coin_name} DATA is FALSE')
                sleep(90) # пауза в 90 секунд

            id_coin += 1   # next coin
       


def send_data():
    """Функция для отправки данных 
    пользователям (не асинхронная)"""
    while True:
        if new_data:
            data_to_send = new_data.pop(0)
            for user_id in subscribed_users:
                bot.send_message(user_id, f"Нові данні: {data_to_send}")
        sleep(2)  # Пауза между проверками новых данных


# Запуск бота в отдельном потоке
def bot_polling():
    bot.polling()

# Запуск основных функций в отдельных потоках
main_thread = threading.Thread(target=main)
send_data_thread = threading.Thread(target=send_data)
bot_thread = threading.Thread(target=bot_polling)

main_thread.start()
send_data_thread.start()
bot_thread.start()
