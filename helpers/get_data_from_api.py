import requests
import os
from dotenv import load_dotenv

load_dotenv()
def get_data(data_to_get: str) -> list:
    """Функция получения списка факеультетов или оснащения"""
    url_endpoint = os.getenv(f'{data_to_get}')
    try:
        response = requests.get(f"https://0ee3-85-172-29-2.ngrok-free.app/{url_endpoint}").json()
    except:
        print(f'Request Error')
    return response


# print(get_data('FACULTIES_URL'))
