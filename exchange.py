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