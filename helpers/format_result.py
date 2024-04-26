from consts.buttons import NO_FREE_PLACES

def format_result(response) -> str:
    '''Функция получает на вход респонс с апи и форматирует дату для вывода'''
    print('response = ', response)
    if response == None:
        return NO_FREE_PLACES
    free_paces = ''
    for i in range(len(response)):
        if response[i]["faculty"] == None:
            short_name = '-'
        else:
            short_name = response[i]["faculty"]["short_name"]
        free_paces += f'№: {response[i]["name"]}, {short_name}, {response[i]["size"]}\n'

        return free_paces