def create_message(params, type) -> str:
    """Функция получает на вход параметры и тип сообщения, возвращает текст"""

    if type == 'start':
        return f'Данный инструмент позволяет просто\nи быстро найти свободную аудиторию!'
    elif type == 'select_data':
        return f'Выберите дату: \n——————————————————'
    elif type == 'select_les_num':
        return  f'Дата: <b>{params["date_from_user"]}</b>\nВыберите пару: \n——————————————————'
    elif type == 'select_faculty':
        return f'Дата: <b>{params["date_from_user"]}</b>\nПара: <b>{params["lesson_num"]}</b>\n'\
                           f'Выберите факультет: \n——————————————————'
    elif type == 'select_equipment':
        return f'Дата: <b>{params["date_from_user"]}</b>\nПара: <b>{params["lesson_num"]}</b>\n'\
                            f'Факультеты: <b>{params["faculties_short_name"]}</b>\nВыберите оснащение: \n'\
                            f'——————————————————'
    elif type == 'select_size':
        return f'Дата: <b>{params["date_from_user"]}</b>\nПара: <b>{params["lesson_num"]}</b>\nФакультеты: '\
                        f'<b>{params["faculties_short_name"]}</b>\nОснащение: <b>{params["equipments_name"]}</b>\n'\
                       f'Выберите вместимость: \n——————————————————'
    elif type == 'find':
        return f'Дата: <b>{params["date_from_user"]}</b>\nПара: <b>{params["lesson_num"]}</b>\n'\
                f'Факультеты: <b>{params["faculties_short_name"]}</b>\nОснащение: <b>{params["equipments_name"]}</b>\n'\
                f'Кол-во мест: <b>{params["size"]}</b> \n——————————————————'
