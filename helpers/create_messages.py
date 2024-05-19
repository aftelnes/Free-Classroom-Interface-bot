"""
Функция, создающая сообщения под пайплайн взаимодействия с пользвователем
"""
from consts.messages import message_templates


def create_message(type_mes, params) -> str:
    """Функция получает на вход параметры и тип сообщения, возвращает текст"""
    return message_templates.get(type_mes).format(**params)
