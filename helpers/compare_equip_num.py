def compare_equip_num(equipment_num: str) -> int:
    '''Функция конвертации колбэка оснащения в число(для запроса на сервер)'''
    equipments = {
        'equip_1': 1,
        'equip_2': 2,
        'equip_3': 3,
        'equip_4': 4,
        'equip_5': 5,
        'equip_6': 6,
        'equip_7': 7,
        'equip_8': 8,
        'equip_9': 9,
    }

    return equipments[equipment_num]