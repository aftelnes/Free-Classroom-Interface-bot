from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from helpers.get_data_from_api import get_data
from consts.buttons import BACK_BTN, CONTINUE_BTN

def create_equipment_keyboard():
    equipments = get_data('EQUIPMENTS_URL')
    equipments_ary = InlineKeyboardBuilder()
    for i in range(len(equipments)):
        equipments_ary.add(InlineKeyboardButton(text=equipments[i]['name'], callback_data="equip_" + str(equipments[i]['id'])))

    equipments_ary.add(InlineKeyboardButton(text=BACK_BTN, callback_data='back_to_select_faculties'))
    equipments_ary.add(InlineKeyboardButton(text=CONTINUE_BTN, callback_data='all_data_is_selected'))


    return equipments_ary.adjust((2)).as_markup()