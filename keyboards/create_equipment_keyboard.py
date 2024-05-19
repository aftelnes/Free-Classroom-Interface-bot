from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from helpers.get_data import get_data
from consts.buttons import BACK_BTN, CONTINUE_BTN
from api.consts import EQUIPMENTS_ENDPOINT


async def create_equipment_keyboard():
    """Функция создаёт клавиатуру с оснащением"""
    equipments = await get_data(endpoint=EQUIPMENTS_ENDPOINT)
    equipments_ary = InlineKeyboardBuilder()
    for i in range(len(equipments)):
        equipments_ary.add(InlineKeyboardButton(text=equipments[i]['name'],
                                                callback_data="equip_" + str(equipments[i]['id'])))

    equipments_ary.add(InlineKeyboardButton(text=BACK_BTN, callback_data='select_faculties'))
    equipments_ary.add(InlineKeyboardButton(text=CONTINUE_BTN, callback_data='select_size'))

    return equipments_ary.adjust((2)).as_markup()


async def create_equipments_state():
    """Функция создаёт массив объектов, с состоянием нажатия на кнопку"""
    equipments = await get_data(endpoint=EQUIPMENTS_ENDPOINT)
    equipments_ary_state = []

    for i in range(len(equipments)):
        equipments_ary_state.append({"name": equipments[i]['name'], "is_selected": False,
                                     "id": str(equipments[i]['id'])})

    return equipments_ary_state


async def create_equipments_keyboard(equipments_ary_state):
    """Фукция создаёт клавиатуру оснащения"""
    equipments_keyboard = InlineKeyboardBuilder()
    for i in range(len(equipments_ary_state)):
        if equipments_ary_state[i]["is_selected"]:
            equipments_keyboard.add(InlineKeyboardButton(text='✅' + equipments_ary_state[i]["name"],
                                                         callback_data="equip_" + equipments_ary_state[i]["id"]))
        elif not equipments_ary_state[i]["is_selected"] and equipments_ary_state[i]["name"][0] == "✅":
            equipments_keyboard.add(InlineKeyboardButton(text=str(equipments_ary_state[i]["name"])[1:],
                                                         callback_data="equip_" + equipments_ary_state[i]["id"]))
        else:
            equipments_keyboard.add(InlineKeyboardButton(text=equipments_ary_state[i]["name"],
                                                         callback_data="equip_" + equipments_ary_state[i]["id"]))

    equipments_keyboard.add(InlineKeyboardButton(text=BACK_BTN, callback_data='select_faculties'))
    equipments_keyboard.add(InlineKeyboardButton(text=CONTINUE_BTN, callback_data='select_size'))

    return equipments_keyboard.adjust((2)).as_markup()
