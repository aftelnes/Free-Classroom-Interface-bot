from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from helpers.get_data import get_data
from consts.buttons import BACK_BTN, CONTINUE_BTN

async def create_equipment_keyboard():
    '''Функция создаёт клавиатуру с оснащением'''
    equipments = await get_data('EQUIPMENTS')
    equipments_ary = InlineKeyboardBuilder()
    for i in range(len(equipments)):
        equipments_ary.add(InlineKeyboardButton(text=equipments[i]['name'], callback_data="equip_" + str(equipments[i]['id'])))

    equipments_ary.add(InlineKeyboardButton(text=BACK_BTN, callback_data='select_faculties'))
    equipments_ary.add(InlineKeyboardButton(text=CONTINUE_BTN, callback_data='select_size'))


    return equipments_ary.adjust((2)).as_markup()