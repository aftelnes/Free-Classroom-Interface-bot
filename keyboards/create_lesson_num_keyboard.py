from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from consts.buttons import BACK_BTN
from helpers.get_data import get_data


async def create_lesson_num_keyboard():
        lesson_num = await get_data('LESSONS_NUM_URL')

        lesson_num_ary = InlineKeyboardBuilder()
        for i in range(len(lesson_num)):
            lesson_num_ary.add(InlineKeyboardButton(text=f'{lesson_num[i]["number"]}', callback_data="les_" + str(lesson_num[i]["id"])))

        lesson_num_ary.add(InlineKeyboardButton(text=BACK_BTN, callback_data='back_to_select_date'))
        return lesson_num_ary.adjust((3)).as_markup()