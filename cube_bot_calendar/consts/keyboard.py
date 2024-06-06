"""
Модуль со статическими клавиатурами календаря.
"""
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from consts.buttons import *

select_month_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text=BEGIN,
            callback_data='select_month'
        )
    ]
])
