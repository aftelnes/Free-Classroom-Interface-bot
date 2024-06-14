"""
Функция создаёт клавиатуру в том случае, если пары на сегодня закончились
"""
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import CallbackQuery

from consts.buttons import BACK_BTN, RETURN_TO_START_BTN
from helpers.create_messages import create_message


async def create_lessons_is_over_keyboard():
    keyboard = InlineKeyboardBuilder()
    keyboard.add(
        InlineKeyboardButton(
            text=BACK_BTN,
            callback_data='select_day'
        ),
        InlineKeyboardButton(
            text=RETURN_TO_START_BTN,
            callback_data='select_month')
        )
    return keyboard.as_markup()


async def show_lessons_is_over(callback_query: CallbackQuery):
    await callback_query.message.edit_text(
        text=create_message(
            params={},
            type_mes='time_is_over'
        ),
        reply_markup=await create_lessons_is_over_keyboard()
    )
