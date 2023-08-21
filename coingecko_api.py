"""Модуль для работы с API Coingecko."""
import requests
from dotenv import load_dotenv
import os
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='log_file.log',
    filemode='a',
    format='%(asctime)s %(levelname)s %(message)s'
)

load_dotenv('.env')
COINGECKO_API_TOKEN = os.environ.get('COINGECKO_API_TOKEN', '')



def get_data(coin_identifier: str, page: int):
    """функция получения данных о монете с API Coingecko"""
    # endpoint = f"coins/{coin_identifier}/tickers?exchange_ids=all"
    endpoint = f"coins/{coin_identifier}/tickers?page={page}"
    headers = {
        'accept': 'application/json',
    }
    try:
        response = requests.get(COINGECKO_API_TOKEN + endpoint, headers=headers)
        if response.status_code == 200:
            data = json.loads(response.text)
            headers = response.headers # response headers
            print(headers['total']) # count total
            return data
                  
        else:

            logging.info(response.reason) # reason - причина ошибки
            return None
            
    except requests.RequestException as e:
        logging.info("Ошибка при выполнении запроса:", e)
        return None

