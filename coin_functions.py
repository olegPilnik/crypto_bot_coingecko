"""Модуль для функций, связанных с обработкой данных о монетах"""
from datetime import datetime


def sorting_coins(data, coin_id):
    """Сортируем монеты по условию,
    пропускаем только с обьемом более 10000
    и те в которых монета против тетхера и возвращаем 
    список словарей с отсортированными данными"""
    tickers = data['tickers']

    lst_tickers = [] #  Создаем промежуточный список
    for item in tickers:  #  Пробегаемся по списку словарей, каждый item- словарь, отдельная биржа
        
        """Проверка данных на соответствие условиям""" 
        volume = item.get('volume')
        if volume >= 10000:  # Отсеиваем торги с объемом меньше 10000
            if item.get('target_coin_id') is not None:
                target_coin_id = item['target_coin_id']
                coin_id_coingecko = item['coin_id']
                if coin_id_coingecko == coin_id and target_coin_id == 'tether':
                    price = item['last']   
                    exchange = item['market']['name']
                    link_tickers = item['trade_url']
                    dct = {}  # создаем промежуточный словарь
                    dct['coin_id'] = coin_id
                    dct['target_coin_id'] = target_coin_id
                    dct['price'] = round(price, 6)
                    dct['volume'] = round(volume, 4)
                    dct['exchange'] = exchange
                    dct['datetime'] = (datetime.now()).strftime('%d-%m-%Y %H:%M:%S')
                    dct['link_tickers'] = link_tickers
                    
                    lst_tickers.append(dct) #  Если условия выполненны добавляем словарь в список
                    
                else:
                    pass
            else:
                pass
        else:
            pass      

    return lst_tickers










