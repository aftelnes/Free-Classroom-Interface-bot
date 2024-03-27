def compare_faculty_short_name(faculty_num: str) -> int:
    '''Функция конвертации колбэка факультетов в сокращенное названгие(для показа пользователю)'''
    faculties = {
        'fac_1': 'ФМиКН',
        'fac_2': 'ФКТиПМ',
        'fac_3': 'ФТФ',
        'fac_4': 'ФППК',
        'fac_5': 'ЭФ',
        'fac_6': 'БФ',
        'fac_7': 'ФАД',
        'fac_8': 'ФЖ',
        'fac_9': 'ФИСМО',
        'fac_10': 'РГФ',
        'fac_11': 'ФУП',
        'fac_12': 'ФХиВТ',
        'fac_13': 'ФФ',
        'fac_14': 'ХГФ',
        'fac_15': 'ЮФ'
    }
    return faculties[faculty_num]

