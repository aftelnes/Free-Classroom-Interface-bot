"""
Модуль календаря
"""
from datetime import datetime
import calendar

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton


from cube_bot_calendar.consts.consts import MONTHS, WEEK_DAYS


async def create_months_keyboard(from_month=1):
    """Функция создаёт клавиатуру с календарём"""
    months_keyboard = InlineKeyboardBuilder()

    for i in range(from_month, 13):
        months_keyboard.add(InlineKeyboardButton(text=f'{MONTHS[i]}',
                                                 callback_data=f'month_{i}'))
    months_keyboard.adjust((3)).as_markup()

    months_keyboard.row(InlineKeyboardButton(text='Сегодня', callback_data='today'))

    return months_keyboard.as_markup()


async def create_days_keyboard(year, month):
    """Функция создаёт клавиатуру с днями месяца"""
    days = InlineKeyboardBuilder()

    month_start, number_of_days = calendar.monthrange(year, month)

    for i in range(len(WEEK_DAYS)):
        days.add(InlineKeyboardButton(text=f'{WEEK_DAYS[i]}',
                                      callback_data=f'_'))

    for i in range(month_start):
        days.add(InlineKeyboardButton(text=f' ',
                                      callback_data=f'_'))

    for i in range(1, number_of_days + 1):
        days.add(InlineKeyboardButton(text=f'{i}',
                                      callback_data=f'day_{i}'))

    # last_empty_btns = ((month_start + number_of_days) // 7 + 1) * 7 - (month_start + number_of_days)
    last_empty_btns = 7 - datetime(year, month, number_of_days).weekday() - 1

    for i in range(last_empty_btns):
        days.add(InlineKeyboardButton(text=f' ',
                                      callback_data=f'_'))

    days.adjust((7)).as_markup()

    days.row(InlineKeyboardButton(text='Назад', callback_data='select_month'),
             InlineKeyboardButton(text='Сегодня', callback_data='today'))

    return days.as_markup()
