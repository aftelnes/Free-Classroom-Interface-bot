from consts.buttons import NO_FREE_PLACES
import re

def format_result(response, user_data) -> str:
    """Функция получает на вход респонс с апи и форматирует его для вывода"""
    if response is None or response == []:
        return NO_FREE_PLACES

    free_paces = ''

    user_lesson_num = user_data['lesson_num']
    user_date = user_data['date']

    free_paces += (
        f'<code>Дата: {user_date}</code>\n'
        f'<code>Пара: {user_lesson_num}</code>\n'
        f'<code>-----------------------</code>\n'
    )

    free_paces += ('<code>  №   |Факультет| Мест</code>\n'
                  '<code>-----------------------</code>\n')
    for i in range(len(response)):
        size = str(response[i]["size"])
        classroom_number = str(response[i]["name"])

        if response[i]["faculty"] is None:
            short_name = '-'
        else:
            short_name = response[i]["faculty"]["short_name"]

        while len(classroom_number) < 6:
            classroom_number += ' '
        while len(short_name) < 8:
            short_name += ' '

        free_paces += f'<code>{classroom_number}| {short_name}| {size}</code>\n'

    if user_data['equipments_name'] != '':
        print('user_data["equipments_name"] = ', user_data['equipments_name'])
        # Форматируем строку с оснащением пользователя до нужного формата
        formatted_user_equipments = user_data['equipments_name'].replace(', ', '\n')

        free_paces += (f'<code>-----------------------</code>\n'
                       f'<code>Оснащение аудиторий:</code>\n'
                       f'<code>{formatted_user_equipments}</code>\n')

    return free_paces
