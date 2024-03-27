from aiogram.fsm.state import State, StatesGroup

class DataFromUser(StatesGroup):

    """Данные, получаемые от пользователя"""
    date_from_user: str = State()
    lesson_num: str = State()
    size: int = State()
    faculties: list[int] = State()
    equipments: list[int] = State()

    faculties_short_name: str = State()
    equipments_name: str = State()