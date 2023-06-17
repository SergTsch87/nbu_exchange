#!usr/bin/env
import json
import xmltodict
import requests
from urllib.request import urlopen


# # # -------------------------------------------------------
# Декоратор для заміру часу виконання функції

import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Функція {func.__name__} виконалася за {execution_time} секунд")
        return result
    return wrapper

# -------------------------------------------------------
# Декоратор для перехоплення та обробки винятків

def handle_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            print(f"Помилка: {str(e)}")
            # Додаткові дії для обробки помилки

    return wrapper

# -------------------------------------------------------

def get_xml_data_currencies(url):
    response = requests.get(url)
    return xmltodict.parse(response.content)


# Дістанемо з одного JSON-файлу список словників:
#       усі назви валют, та їх відповідні значення
def get_data_all_currencies(url):
    response = urlopen(url)
    return json.loads(response.read())

# get MAX
def get_max_value_dict(my_dict):
    return max(my_dict, key = my_dict.get)

# get MIN
def get_min_value_dict(my_dict):
    return min(my_dict, key = my_dict.get)

# ===========================================================================================

def dict_from_file(func):
    def wrapper(url):
        dict_data = func(url)
        new_dict = {dict_item['CurrencyCodeL']: float(dict_item['Amount']) for dict_item in dict_data}
        return new_dict
    return wrapper

@dict_from_file
def get_new_dict_xml(url):
    return get_xml_data_currencies(url)['CURRENCYCOURSE']['ROW']

@dict_from_file
def get_new_dict_json(url):
    return get_data_all_currencies(url)

# ===========================================================================================

@handle_exceptions
@timer
def print_max_min_val(func):
    def wrapper():
        new_dict = func()
        max_value = get_max_value_dict(new_dict)
        print(f'{func.__name__} Валюта з максимальним значенням:\n{max_value}: {new_dict[max_value]}')

        min_value = get_min_value_dict(new_dict)
        print(f'{func.__name__} Валюта з мінімальним значенням:\n{min_value}: {new_dict[min_value]}')
    return wrapper


@print_max_min_val
def get_dict_json():
    url = 'https://bank.gov.ua/NBU_Exchange/exchange?json'
    return get_new_dict_json(url)


@print_max_min_val
def get_dict_xml():
    url = 'https://bank.gov.ua/NBU_Exchange/exchange'
    return get_new_dict_xml(url)

# --------------------------------------------------------

if __name__ == '__main__':    

    get_dict_json()
    get_dict_xml()