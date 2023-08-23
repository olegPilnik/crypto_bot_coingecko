"""Модуль для функций, связанных с обработкой данных о монетах"""
from datetime import datetime
import pytz

def convert_to_decimal(number): 
    """price convert to decimal"""
    # Если число уже в десятичной форме, то просто вернуть его
    if isinstance(number, float):
        return number
    
    # Если число в экспоненциальной форме, выполнить преобразование
    elif isinstance(number, str):
        parts = number.split('e')
        coefficient = float(parts[0])
        exponent = int(parts[1])
        return coefficient * 10 ** exponent
    
    else:
        raise ValueError("Unsupported number format")


def get_current_time():
    # Выберите часовой пояс Киева
    kiev_timezone = pytz.timezone('Europe/Kiev')
    
    # Получите текущее время в выбранном часовом поясе
    current_time = datetime.now(tz=kiev_timezone)
    
    return current_time



def sorting_coins(data, coin_id, exchange_id):
    """Сортируем монеты по условию,
    пропускаем только с обьемом более 10000
    и те в которых монета против тетхера и возвращаем 
    список словарей с отсортированными данными"""
    tickers = data['tickers']

    lst_tickers = [] #  Создаем промежуточный список
    for item in tickers:  #  Пробегаемся по списку словарей, каждый item- словарь, отдельная биржа
        
        """Проверка данных на соответствие условиям""" 
        exchange_identifier = item['market']['identifier']
        if exchange_id == exchange_identifier: # Проверка есть ли биржа среди интересующих

            volume = item.get('volume')
            if volume >= 10000:  # Отсеиваем торги с объемом меньше 10000
                if item.get('target_coin_id') is not None:
                    target_coin_id = item['target_coin_id']
                    coin_id_coingecko = item['coin_id']
                    if coin_id_coingecko == coin_id and target_coin_id == 'tether':
                        price = convert_to_decimal(item['last'])
                        volume_usd = item['converted_volume']['usd'] 
                        exchange = item['market']['name']
                        
                        link_tickers = item['trade_url']
                        dct = {}  # создаем промежуточный словарь
                        dct['coin_id'] = coin_id
                        dct['target_coin_id'] = target_coin_id
                        dct['price'] = round(price, 7)
                        dct['volume_base'] = round(volume, 2)
                        dct['volume_usd'] = round(volume_usd, 2)
                        dct['exchange'] = exchange
                        dct['datetime'] = (get_current_time()).strftime('%d-%m-%Y %H:%M:%S')
                        dct['link_tickers'] = link_tickers
                        
                        lst_tickers.append(dct) #  Если условия выполненны добавляем словарь в список
                    

                    else:
                        pass
                else:
                    pass
            else:
                pass
        else:
            pass      

                


    return lst_tickers








