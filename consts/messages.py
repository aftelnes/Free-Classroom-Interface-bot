"""
Объект, хранящий готовые сообщения, для отправки пользователю.
"""

message_templates = {
    'start': '🔍 Найти аудиторию \n',
    'select_month': '🗓️ Выберите месяц: \n——————————————————',
    'select_day': '🗓️ Месяц: <b>{month_name}</b> \n🔅 Выберите день: \n——————————————————',
    'select_les_num': '🗓️ Дата: <b>{date}</b>\n🕒 Выберите пару: \n——————————————————',
    'select_faculty': '🗓️ Дата: <b>{date}</b>\n'
                      '🕒 Пара: <b>{lesson_num}</b>\n'
                      '🏛 Выберите факультет: \n——————————————————',
    'select_equipment': '🗓️ Дата: <b>{date}</b>\n'
                        '🕒 Пара: <b>{lesson_num}</b>\n'
                        '🏛 Факультеты: <b>{faculties_short_name}</b>\n🖥 Выберите оснащение: \n'
                        '——————————————————',
    'select_size': '🗓️ Дата: <b>{date}</b>\n'
                   '🕒 Пара: <b>{lesson_num}</b>\n🏛 Факультеты: '
                   '<b>{faculties_short_name}</b>\n'
                   '🖥 Оснащение: <b>{equipments_name}</b>\n'
                   '🪑 Выберите вместимость: \n——————————————————',
    'find': '🗓️ Дата: <b>{date}</b>\n'
            '🕒 Пара: <b>{lesson_num}</b>\n'
            '🏛 Факультеты: <b>{faculties_short_name}</b>\n'
            '🖥 Оснащение: <b>{equipments_name}</b>\n'
            '🪑 Вместимость: <b>{size}</b> \n——————————————————'
}
