"""Главный модуль в котором происходит анализ
 и подготовка данных к отправке пользователю"""

from connect_db import get_row_count_table_coins, get_coin
from connect_db import get_selected_exchanges

from coingecko_api import get_data

from coin_functions import sorting_coins

import pandas as pd

from time import sleep


import logging

logging.basicConfig(
    level=logging.INFO,
    filename='log_file.log',
    filemode='a',
    format='%(asctime)s %(levelname)s %(message)s'
)


new_data = []

def main(stop=False, min_spread=1):
    """Загружаем все 750 монет  из базы в список кортежей"""
    try:
        coins_count = get_row_count_table_coins()
    except Exception as ex:
        logging.info(f'При загрузке coins_count: {ex}')

    while stop == False:
        id_coin= 1       

        """Проходим циклом по монетам"""
        while id_coin <= coins_count: # перебираем индексы от 1 до последнего в базе с монетами
            try:
                coin = get_coin(id_coin) # получаем coin из базы в виде кортежа (id, coin_id, symbol, name)
            except Exception as ex:
                logging.info(f'При загрузке coin: {ex}')
            coin_id = coin[1] #  записываем в переменную coin_id значение id из кортежа
            print(coin_id)
            coin_name = coin[3] #  записываем в переменную coin_name значение name из базы
            coin_symbol = coin[2].upper() # все заглавные
            
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
                list_exchanges = get_selected_exchanges()
                
                """Преребираем строки DataFrame df_exchanges"""
                for item in list_exchanges:
                    exchange_id = item[0]
                    exchange_name = item[1]
                    
                    """Сортируем данные в список словарей"""
                    lst_tickers = sorting_coins(data, coin_id, exchange_id)

                    if len(lst_tickers) > 0:
                        """С помощью метода from_records добавляем список словарей в DataFrame df_tickers"""
                        df_tickers = pd.concat([df_tickers, pd.DataFrame.from_records(lst_tickers)], ignore_index=True)
                        # print(df_tickers)
                        # df_tickers.to_csv(f'df_tickers{coin_name}.csv', index=True)# temp!!!!
                    
                        """Возвращаю максисальную и минимальную цену монеты"""
                        price_min = df_tickers['price'].min()
                        price_max = df_tickers['price'].max()
                        spread = ((price_max - price_min)/ price_min) * 100
                        print(spread)
                        if min_spread <= spread <= 30:
                            """Возвращаем в виде фреймов строки с 
                            "price" == price_max и "price" == price_min"""
                            df_min = df_tickers[df_tickers['price'] == price_min]
                            df_max = df_tickers[df_tickers['price'] == price_max]
                        

                            """Создаем словарь для возврата пользователю"""
                            return_dict = {}
                            return_dict['coin'] = coin_name
                            return_dict['coin_symbol'] = coin_symbol
                            return_dict['target_coin'] = df_min.iloc[0]['target_coin_id']
                            return_dict['datetime'] = df_min.iloc[0]['datetime']
                            return_dict['pr_min_exchange'] = df_min.iloc[0]['exchange']
                            return_dict['ex_min_volume'] = df_min.iloc[0]['volume_base']
                            return_dict['ex_min_volume_usd'] = df_min.iloc[0]['volume_usd']
                            return_dict['price_min'] = price_min
                            return_dict['pr_min_link'] = df_min.iloc[0]['link_tickers']
                                                      
                            return_dict['pr_max_exchange'] = df_max.iloc[0]['exchange']
                            return_dict['ex_max_volume'] = df_max.iloc[0]['volume_base']
                            return_dict['ex_max_volume_usd'] = df_max.iloc[0]['volume_usd']
                            return_dict['price_max'] = price_max
                            return_dict['pr_max_link'] = df_max.iloc[0]['link_tickers']
                            
                            
                            return_dict['spread'] = round(spread, 2)

                            df = pd.DataFrame([return_dict])
                            

            #                 """START TEMP"""

            #                 # df_tickers.to_csv(f'df_tickers{coin_name}.csv', index=True)
            #                 # df.to_csv(f'return_dict{spread}.csv', index=True, )

            #                 """FINISH TEMP"""


                            return_str = (f"Біржи: {return_dict['pr_min_exchange']}\{return_dict['pr_max_exchange']}\n"
                                          f"Актив: {return_dict['coin']}({return_dict['coin_symbol']})\\USDT\n"
                                          f"{return_dict['datetime']}\n"
                                          "\n\n"
                                          f"Об'єм: {return_dict['ex_min_volume']} --> {return_dict['ex_min_volume_usd']}$\n"
                                          f"Ціна: {return_dict['price_min']} USDT\n"
                                          f"Посилання: {return_dict['pr_min_link']}\n"
                                          "\n\n"
                                          f"Об'єм: {return_dict['ex_max_volume']} --> {return_dict['ex_max_volume_usd']}$\n"
                                          f"Ціна: {return_dict['price_max']} USDT\n"
                                          f"Посилання: {return_dict['pr_max_link']}\n"
                                          "\n\n"
                                          f"Спред: {return_dict['spread']}%")
                            
                            """Добавляем строку в список new_data"""
                            new_data.append(return_str)

                                              
                        
                else:
                    logging.info(f'COIN {coin_name} EMPTY lst_tickers')

            else:
                print('Please wait 90 seconds')
                logging.info(f'COIN {coin_name} DATA is FALSE')
                sleep(90) # пауза в 90 секунд
            
            id_coin += 1   # next coin 
        
