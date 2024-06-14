"""
Функция сравнивающая 2 времени
"""
from datetime import datetime

def compare_time(time_1, time_2):
    """Сравнивает time_1 с time_2 """
    time_format = "%H:%M"
    time_1 = datetime.strptime(time_1, time_format)
    time_2 = datetime.strptime(time_2, time_format)

    if time_1 >= time_2:
        return False
    elif time_1 < time_2:
        return True
