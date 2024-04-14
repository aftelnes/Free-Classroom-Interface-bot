import requests
import config


def get_free_classrooms(date: str, les_num: str, faculties: list[str], equipments: list[str], size: int):
    """Функция получения свободных аудиторий"""
    print(f'Дата = {date}\nПара = {les_num}\nФакультеты = {faculties}\nОснащение = {equipments}')

    params_to_request = {
        'date': date,
        'number': les_num,
        'faculty': faculties,
        'equipment': equipments,
        'size': size
    }
    response = ''
    try:
        response = requests.get(f"{config.base_config.SERV_URL}{config.base_config.FREE_PLACES_URL}", params=params_to_request).json()
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