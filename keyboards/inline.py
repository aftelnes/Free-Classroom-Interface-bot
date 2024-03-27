"""
Модуль со статичными клавиатурами.
"""

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from consts.buttons import *

select_date = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=PICK_DATE,
            callback_data='select_date'
        )
    ]
])

select_lesson_number = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=LESSON_1,
            callback_data='les_1'
        ),
        InlineKeyboardButton(
            text=LESSON_2,
            callback_data='les_2'
        ),
        InlineKeyboardButton(
            text=LESSON_3,
            callback_data='les_3'
        )
    ],
[
        InlineKeyboardButton(
            text=LESSON_4,
            callback_data='les_4'
        ),
        InlineKeyboardButton(
            text=LESSON_5,
            callback_data='les_5'
        ),
        InlineKeyboardButton(
            text=LESSON_6,
            callback_data='les_6'
        )
    ],
[
        InlineKeyboardButton(
            text=LESSON_7,
            callback_data='les_7'
        ),
        InlineKeyboardButton(
            text=LESSON_8,
            callback_data='les_8'
        ),
        InlineKeyboardButton(
            text=LESSON_9,
            callback_data='les_9'
        )
    ],
    [
        InlineKeyboardButton(
            text=BACK_BTN,
            callback_data='back_to_select_date'
        )
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
            text=BACK_BTN,
            callback_data='back_to_select_equipments'
        ),
    ]
])