"""
Модуль календаря
"""
from datetime import datetime
import calendar

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from cube_bot_calendar.consts.consts import MONTHS, WEEK_DAYS

from consts.buttons import BACK_BTN

from helpers.compare_time import compare_time


async def create_months_keyboard(from_month=1, to_month=12):
    """Функция создаёт клавиатуру с календарём"""
    months_keyboard = InlineKeyboardBuilder()

    today = datetime.now().strftime("%d.%m.%Y")
    for i in range(from_month, to_month + 1):
        months_keyboard.add(InlineKeyboardButton(
            text=f'{MONTHS[i]}',
            callback_data=f'month_{i}'
        ))
    months_keyboard.adjust((3)).as_markup()

    months_keyboard.row(InlineKeyboardButton(
        text=f'▶️ Сегодня ({today}) ◀️',
        callback_data='today'
    ))

    return months_keyboard.as_markup()


async def create_days_keyboard(
        year,
        month,
        from_current_day=True,
        over_day_symbol='✖️',
        over_day_time='20:10'
):
    """Функция создаёт клавиатуру с днями месяца"""
    days = InlineKeyboardBuilder()

    month_start, number_of_days = calendar.monthrange(year, month)

    for i in range(len(WEEK_DAYS)):
        days.add(InlineKeyboardButton(
            text=f'{WEEK_DAYS[i]}',
            callback_data=f'_'
        ))

    for i in range(month_start):
        days.add(InlineKeyboardButton(
            text=f' ',
            callback_data=f'_'
        ))

    if from_current_day and month == datetime.now().month:

        # last_over_day - день, до которого нужно блокировать выбор (включительно)
        last_over_day = datetime.now().day
        if compare_time(over_day_time, datetime.now().time().strftime('%H:%M')):
            last_over_day += 1

        for i in range(1, last_over_day):
            days.add(InlineKeyboardButton(
                text=f'{over_day_symbol}',
                callback_data='day_is_over'
            ))
        for i in range(last_over_day, number_of_days + 1):
            days.add(InlineKeyboardButton(
                text=f'{i}',
                callback_data=f'day_{i}'
            ))
    else:
        for i in range(1, number_of_days + 1):
            days.add(InlineKeyboardButton(
                text=f'{i}',
                callback_data=f'day_{i}'
            ))

    # last_empty_btns = ((month_start + number_of_days) // 7 + 1) * 7 - (month_start + number_of_days)
    last_empty_btns = 7 - datetime(year, month, number_of_days).weekday() - 1

    for i in range(last_empty_btns):
        days.add(InlineKeyboardButton(
            text=f' ',
            callback_data=f'_'
        ))

    days.adjust((7)).as_markup()

    today = datetime.now().strftime("%d.%m.%Y")
    days.row(InlineKeyboardButton(
            text=f'▶️ Сегодня ({today}) ◀️',
            callback_data='today'
        ))

    days.row(
        InlineKeyboardButton(
            text=BACK_BTN,
            callback_data='select_month'
        ),

    )

    return days.as_markup()
