"""
Модуль со статичными клавиатурами.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from consts.buttons import *

select_date_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=BEGIN,
            callback_data='select_date'
        )
    ]
])

select_size_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=SIZE_2O,
            callback_data='size_20'
        ),
        InlineKeyboardButton(
            text=SIZE_40,
            callback_data='size_40'
        )
    ],
    [
        InlineKeyboardButton(
            text=SIZE_60,
            callback_data='size_60'
        ),
        InlineKeyboardButton(
            text=SIZE_80,
            callback_data='size_80'
        )
    ],
[
        InlineKeyboardButton(
            text=CONTINUE_BTN,
            callback_data='all_data_is_selected'
        ),
        InlineKeyboardButton(
            text=BACK_BTN,
            callback_data='select_equipments'
        ),
    ]
])

find_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=FIND_BTN,
            callback_data='get_free_classrooms'
        ),

    ],
    [
        InlineKeyboardButton(
            text=RETURN_TO_START_BTN,
            callback_data='select_date'
        ),
    ]
])

result_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=RETURN_TO_START_BTN,
            callback_data='select_date'
        ),
    ]
])