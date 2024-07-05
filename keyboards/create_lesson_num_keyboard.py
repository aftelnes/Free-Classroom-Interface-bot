from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime, timedelta

from helpers.get_data import get_data
from helpers.compare_time import compare_time
from consts.buttons import BACK_BTN
from api.consts import LESSONS_NUM_ENDPOINT


# async def create_lesson_num_keyboard(selected_date):
#         """Функция создаёт клавиатуру с номерами пар"""
#         lesson_num = await get_data(endpoint=LESSONS_NUM_ENDPOINT)
#         current_date = datetime.now()
#         current_time = current_date.time().strftime('%H:%M')
#         lesson_num_ary = InlineKeyboardBuilder()
#
#         # Если выбранный день сегодняшний, то ограничиваем показ пар в зависимости от времени
#         if selected_date == current_date.strftime('%d.%m.%Y'):
#             for i in range(len(lesson_num)):
#                 if compare_time(current_time, lesson_num[i]["time"]):
#                     lesson_num_ary.add(InlineKeyboardButton(
#                         text=f'{lesson_num[i]["number"]}',
#                         callback_data="les_" + str(lesson_num[i]["id"])
#                     ))
#         else:
#             for i in range(len(lesson_num)):
#                 lesson_num_ary.add(InlineKeyboardButton(
#                     text=f'{lesson_num[i]["number"]}',
#                     callback_data="les_" + str(lesson_num[i]["id"])
#                 ))
#
#         lesson_num_ary.adjust(3).as_markup()
#
#         lesson_num_ary.row(InlineKeyboardButton(
#             text=BACK_BTN,
#             callback_data='select_day'
#         ))
#
#         return lesson_num_ary.as_markup()


# Версия с костылём - добавляем + 80 минут к получаемому времени
async def create_lesson_num_keyboard(selected_date):
    """Функция создаёт клавиатуру с номерами пар"""
    lesson_num = await get_data(endpoint=LESSONS_NUM_ENDPOINT)
    current_date = datetime.now()
    current_time = current_date.time().strftime('%H:%M')
    lesson_num_ary = InlineKeyboardBuilder()

    # Если выбранный день сегодняшний, то ограничиваем показ пар в зависимости от времени
    if selected_date == current_date.strftime('%d.%m.%Y'):
        for i in range(len(lesson_num)):

            # Блок костыля
            lesson_time = datetime.strptime(lesson_num[i]["time"], "%H:%M")
            new_lesson_time = lesson_time + timedelta(minutes=80)
            formatted_lesson_num = new_lesson_time.strftime("%H:%M")
            # ===========

            if compare_time(current_time, formatted_lesson_num):
                lesson_num_ary.add(InlineKeyboardButton(
                    text=f'{lesson_num[i]["number"]}',
                    callback_data="les_" + str(lesson_num[i]["id"])
                ))
    else:
        for i in range(len(lesson_num)):
            lesson_num_ary.add(InlineKeyboardButton(
                text=f'{lesson_num[i]["number"]}',
                callback_data="les_" + str(lesson_num[i]["id"])
            ))

    lesson_num_ary.adjust(3).as_markup()

    lesson_num_ary.row(InlineKeyboardButton(
        text=BACK_BTN,
        callback_data='select_day'
    ))

    return lesson_num_ary.as_markup()