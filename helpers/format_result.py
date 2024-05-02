from consts.buttons import NO_FREE_PLACES


def format_result(response) -> str:
    '''Функция получает на вход респонс с апи и форматирует его для вывода'''
    if response == None:
        return NO_FREE_PLACES
    free_paces = ('<code>Аудитория | Факультет | Вместимость</code>\n'
                  '<code>-----------------------------------</code>\n')


    for i in range(len(response)):
        size = str(response[i]["size"])
        classroom_number = str(response[i]["name"])

        if response[i]["faculty"] == None:
            short_name = '-'
        else:
            short_name = response[i]["faculty"]["short_name"]
        # TODO сообщение ответа формируется в виде строки(тестовый и пока не рабочий вариант)


        while len(classroom_number) < 10:
            classroom_number += ' '
        while len(short_name) < 10:
            short_name += ' '

        free_paces += f'<code>{classroom_number}| {short_name}| {size}</code>\n'

    return free_paces