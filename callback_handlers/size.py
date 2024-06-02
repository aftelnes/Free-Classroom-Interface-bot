"""
Модуль с логикой работы клавиатуры выбора вместимости
"""
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from helpers.create_messages import create_message
from keyboards.inline import find_keyboard, select_size_keyboard


async def show_size_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Фнукия отправляет клавиатуру с выбором кол-ва необходимых посадочных мест"""
    data = await state.get_data()

    if data["equipments_name"] == '':
        await state.update_data(equipments_name='Любое')
    data = await state.get_data()

    await callback_query.message.edit_text(text=create_message(params=data, type_mes='select_size'),
                                           reply_markup=select_size_keyboard)


async def callback_size_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция реагирует на выбор вместимости, записывает в стейт и показывает слудеющую клавиатуру"""
    await state.update_data(size=int(callback_query.data[5:]))
    data = await state.get_data()
    await callback_query.message.edit_text(text=create_message(params=data, type_mes='find'),
                                           reply_markup=find_keyboard)
