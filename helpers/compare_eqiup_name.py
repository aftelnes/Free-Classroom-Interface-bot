def compare_equip_name(equipment_num: str) -> int:
    '''Функция конвертации колбэка оснащения в название оснащения(для показа пользователю)'''
    equipments = {
        'equip_1': 'Компьютеры',
        'equip_2': 'Проектор',
        'equip_3': 'Меловая доска',
        'equip_4': 'Мультимедийная доска',
        'equip_5': 'Маркерная доска',
        'equip_6': 'ПО: Mathcad',
        'equip_7': 'ПО: Maple',
        'equip_8': 'ПО: Blender',
        'equip_9': 'ПО: Cisco Packet Tracer',
    }

    return equipments[equipment_num]