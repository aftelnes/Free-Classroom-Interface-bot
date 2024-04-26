from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from consts.buttons import BACK_BTN, CONTINUE_BTN
from helpers.get_data import get_data
async def create_faculties_keyboard():
    '''Функция создаёт клавиатуру с факультетами'''
    faculties = await get_data('FACULTIES')

    faculties_ary = InlineKeyboardBuilder()
    for i in range(len(faculties)):
        if faculties[i]['inactive'] == False:
            faculties_ary.add(InlineKeyboardButton(text=faculties[i]["short_name"], callback_data="fac_" + str(faculties[i]["id"])))

    faculties_ary.add(InlineKeyboardButton(text=CONTINUE_BTN, callback_data='select_equipments'))
    faculties_ary.add(InlineKeyboardButton(text=BACK_BTN, callback_data='back_to_select_lesson_num'))

    return faculties_ary.adjust((3)).as_markup()

