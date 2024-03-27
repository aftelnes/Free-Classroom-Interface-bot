def compare_faculty_num(faculty_num: str) -> int:
    '''Функция конвертации колбэка факультетов в число(для запроса на сервер)'''
    faculties = {
        'fac_1': 1,
        'fac_2': 2,
        'fac_3': 3,
        'fac_4': 4,
        'fac_5': 5,
        'fac_6': 6,
        'fac_7': 7,
        'fac_8': 8,
        'fac_9': 9,
        'fac_10': 10,
        'fac_11': 11,
        'fac_12': 12,
        'fac_13': 13,
        'fac_14': 14,
        'fac_15': 15
    }
    return faculties[faculty_num]

