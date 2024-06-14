"""
Модуль с логикой работы клавиатуры выбора пары
"""
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.create_lesson_num_keyboard import create_lesson_num_keyboard
from helpers.create_messages import create_message


async def show_lesson_num_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция отправляет клавиатуру с выбором номера пары, при нажитие кнопки "назад" в меню клавиатуры факультетов"""
    data = await state.get_data()
    await callback_query.message.edit_text(
        text=create_message(
            params=data,
            type_mes='select_les_num'
        ),
        reply_markup=await create_lesson_num_keyboard(selected_date=data["date"])
    )
