def compare_lesson_num(lesson_num: str) -> int:
    '''Функция конвертации колбэка номера пары в число(для запроса на сервер)'''
    lessons = {
        'les_1': 1,
        'les_2': 2,
        'les_3': 3,
        'les_4': 4,
        'les_5': 5,
        'les_6': 6,
        'les_7': 7,
        'les_8': 8,
        'les_9': 9,
    }
    return lessons[lesson_num]

