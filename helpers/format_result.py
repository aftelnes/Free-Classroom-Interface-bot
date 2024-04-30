from consts.buttons import NO_FREE_PLACES
from prettytable import PrettyTable

table = PrettyTable()

def format_result(response) -> str:
    '''Функция получает на вход респонс с апи и форматирует его для вывода'''
    print('response = ', response)
    if response == None:
        return NO_FREE_PLACES
    free_paces = ''
    #TODO сообщение ответа формируется в виде таблицы(тестовый и пока не рабочий вариант)
    table.field_names = ["Аудитория", "Факультет", "Вместимость"]

    for i in range(len(response)):
        if response[i]["faculty"] == None:
            short_name = '-'
        else:
            short_name = response[i]["faculty"]["short_name"]
        # TODO сообщение ответа формируется в виде строки(тестовый и пока не рабочий вариант)
        free_paces += f'№: {response[i]["name"]}, {short_name}, {response[i]["size"]}\n'
        table.add_row([response[i]["name"], short_name, response[i]["size"]])

    return table.get_string()
