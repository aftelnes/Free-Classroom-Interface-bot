"""
Объект, хранящий готовые сообщения, для отправки пользователю.
"""

message_templates = {
    'start': 'Найти аудиторию\n',
    'select_data': 'Выберите дату: \n——————————————————',
    'select_les_num': 'Дата: <b>{date}</b>\nВыберите пару: \n——————————————————',
    'select_faculty': 'Дата: <b>{date}</b>\n'
                      'Пара: <b>{lesson_num}</b>\n'
                      'Выберите факультет: \n——————————————————',
    'select_equipment': 'Дата: <b>{date}</b>\n'
                        'Пара: <b>{lesson_num}</b>\n'
                        'Факультеты: <b>{faculties_short_name}</b>\nВыберите оснащение: \n'
                        '——————————————————',
    'select_size': 'Дата: <b>{date}</b>\n'
                   'Пара: <b>{lesson_num}</b>\nФакультеты: '
                   '<b>{faculties_short_name}</b>\n'
                   'Оснащение: <b>{equipments_name}</b>\n'
                   'Выберите вместимость: \n——————————————————',
    'find': 'Дата: <b>{date}</b>\n'
            'Пара: <b>{lesson_num}</b>\n'
            'Факультеты: <b>{faculties_short_name}</b>\n'
            'Оснащение: <b>{equipments_name}</b>\n'
            'Кол-во мест: <b>{size}</b> \n——————————————————'
}
