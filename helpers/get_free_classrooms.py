import requests
import os
from dotenv import load_dotenv

load_dotenv()

def get_free_classrooms(date: str, les_num: str, faculties: list[str], equipments: list[str]):
    """Функция получения свободных аудиторий"""
    print(f'Дата = {date}\nПара = {les_num}\nФакультеты = {faculties}\nОснащение = {equipments}')
    print(os.getenv(f'FREE_PLACES_URL'))

    params_to_request = {
        'date': date,
        'number': les_num,
        'faculty': faculties,
        'equipment': equipments,
        'size': 1
    }
    response = ''
    try:
        response = requests.get(f"https://0ee3-85-172-29-2.ngrok-free.app/{os.getenv(f'FREE_PLACES_URL')}", params=params_to_request).json()
    except requests.exceptions.HTTPError as err:
        print(f'Request Error = {err}')

    res = ''

    for i in range(len(response)):
        if  response[i]["faculty"] == None:
            short_name = '-'
        else:
            short_name = response[i]["faculty"]["short_name"]
        res += f'№: {response[i]["name"]}, {short_name}, {response[i]["size"]}\n'

    return res