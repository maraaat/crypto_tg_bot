import requests
import os
from dotenv import load_dotenv


def get_page():
    load_dotenv()
    url = os.getenv('URL')
    res = requests.get(url).json()
    return res['data']


def get_coin_data_by_name(name):
    coins = get_page()
    for coin in coins:
        if coin['symbol'] == name:
            return coin


def get_coin_by_id(curr_id):
    coins = get_page()
    for coin in coins:
        if int(coin['id']) == curr_id:
            return coin['symbol']
