from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from helpers.get_data import get_data
from consts.buttons import BACK_BTN
from api.consts import LESSONS_NUM_ENDPOINT


async def create_lesson_num_keyboard():
        """Функция создаёт клавиатуру с номерами пар"""
        lesson_num = await get_data(endpoint=LESSONS_NUM_ENDPOINT)

        lesson_num_ary = InlineKeyboardBuilder()
        for i in range(len(lesson_num)):
            lesson_num_ary.add(InlineKeyboardButton(text=f'{lesson_num[i]["number"]}',
                                                    callback_data="les_" + str(lesson_num[i]["id"])))

        lesson_num_ary.add(InlineKeyboardButton(text=BACK_BTN, callback_data='select_day'))

        return lesson_num_ary.adjust((3)).as_markup()
