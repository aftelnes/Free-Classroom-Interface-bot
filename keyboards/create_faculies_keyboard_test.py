from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from helpers.get_data import get_data
from consts.buttons import BACK_BTN, CONTINUE_BTN
from api.consts import FACULTIES_ENDPOINT


async def create_faculties_state():
    faculties = await get_data(endpoint=FACULTIES_ENDPOINT)

    faculties_ary_state = []

    for i in range(len(faculties)):
        if faculties[i]['inactive'] is False:
            faculties_ary_state.append({"short_name": faculties[i]["short_name"],
                                        "is_selected": False, "id": str(faculties[i]["id"])})

    return faculties_ary_state

async def create_faculties_keyboard_test(faculties_ary_state):
    faculties_keyboard = InlineKeyboardBuilder()
    for i in range(len(faculties_ary_state)):
        faculties_keyboard.add(InlineKeyboardButton(text=faculties_ary_state[i]["short_name"],
                                                    callback_data="fac_" + faculties_ary_state[i]["id"]))

    faculties_keyboard.add(InlineKeyboardButton(text=CONTINUE_BTN, callback_data='select_equipments'))
    faculties_keyboard.add(InlineKeyboardButton(text=BACK_BTN, callback_data='back_to_select_lesson_num'))

    return faculties_keyboard.adjust((3)).as_markup()

async def change_faculties_keyboard(faculties_keyboard):

    print('faculties_keyboard = ', faculties_keyboard)

    faculties_keyboard_changed = InlineKeyboardBuilder()
    for i in range(len(faculties_keyboard)):
        if faculties_keyboard[i]["is_selected"] == True:
            faculties_keyboard_changed.add(InlineKeyboardButton(text='✅' + faculties_keyboard[i]["short_name"],
                                                        callback_data="fac_" + faculties_keyboard[i]["id"]))

        elif faculties_keyboard[i]["is_selected"] == False and faculties_keyboard[i]["short_name"][0] == "+":
            print('name = ', faculties_keyboard[i]["short_name"])
            faculties_keyboard_changed.add(InlineKeyboardButton(text=str(faculties_keyboard[i]["short_name"])[1:],
                                                                callback_data="fac_" + faculties_keyboard[i]["id"]))
        else:
            faculties_keyboard_changed.add(InlineKeyboardButton(text=faculties_keyboard[i]["short_name"],
                                                        callback_data="fac_" + faculties_keyboard[i]["id"]))

    faculties_keyboard_changed.add(InlineKeyboardButton(text=CONTINUE_BTN, callback_data='select_equipments'))
    faculties_keyboard_changed.add(InlineKeyboardButton(text=BACK_BTN, callback_data='back_to_select_lesson_num'))

    return faculties_keyboard_changed.adjust((3)).as_markup()