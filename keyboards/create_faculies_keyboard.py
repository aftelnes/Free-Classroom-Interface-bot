from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from helpers.get_data import get_data
from consts.buttons import BACK_BTN, CONTINUE_BTN
from api.consts import FACULTIES_ENDPOINT


async def create_faculties_state():
    """Функция создаёт массив объектов, с состоянием нажатия на кнопку"""
    faculties = await get_data(endpoint=FACULTIES_ENDPOINT)

    faculties_ary_state = []

    for i in range(len(faculties)):
        if faculties[i]['inactive'] is False:
            faculties_ary_state.append({"short_name": faculties[i]["short_name"],
                                        "is_selected": False, "id": str(faculties[i]["id"])})

    return faculties_ary_state


async def create_faculties_keyboard(faculties_ary_state):
    """Фукция создаёт клавиатуру факультетов"""
    faculties_keyboard = InlineKeyboardBuilder()

    for i in range(len(faculties_ary_state)):
        if faculties_ary_state[i]["is_selected"]:
            faculties_keyboard.add(InlineKeyboardButton(text='✅' + faculties_ary_state[i]["short_name"],
                                                        callback_data="fac_" + faculties_ary_state[i]["id"]))

        elif not faculties_ary_state[i]["is_selected"] and faculties_ary_state[i]["short_name"][0] == "✅":
            faculties_keyboard.add(InlineKeyboardButton(text=str(faculties_ary_state[i]["short_name"])[1:],
                                                        callback_data="fac_" + faculties_ary_state[i]["id"]))
        else:
            faculties_keyboard.add(InlineKeyboardButton(text=faculties_ary_state[i]["short_name"],
                                                        callback_data="fac_" + faculties_ary_state[i]["id"]))

    faculties_keyboard.adjust((2)).as_markup()

    faculties_keyboard.row(
        InlineKeyboardButton(text=BACK_BTN, callback_data='back_to_select_lesson_num'),
        InlineKeyboardButton(text=CONTINUE_BTN, callback_data='select_equipments')
    )

    return faculties_keyboard.as_markup()
