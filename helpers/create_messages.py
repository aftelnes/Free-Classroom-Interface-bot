"""
Функция, создающая сообщения под пайплайн взаимодействия с пользвователем
"""
from consts.messages import message_templates


def create_message(type_mes, params) -> str:
    """Функция получает на вход параметры и тип сообщения, возвращает текст"""

    # Для показа пользователю в факульетах и оснащении убираются последние 2 символа в строке (", ")
    if type_mes == 'select_size' and params["equipments_name"] != "Любое":
        params["equipments_name"] = str(params["equipments_name"])[:-2]
    if type_mes == 'select_equipment' and params["faculties_short_name"] != "Все":
        params["faculties_short_name"] = str(params["faculties_short_name"])[:-2]

    return message_templates.get(type_mes).format(**params)
