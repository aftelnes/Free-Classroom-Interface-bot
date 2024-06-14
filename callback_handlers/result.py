"""
Модуль с логикой работы результирующей клавиатуры
"""
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from helpers.get_data import get_data
from api.consts import FREE_PLACES_ENDPOINT
from helpers.format_result import format_result
from keyboards.inline import result_keyboard


async def show_result(callback_query: CallbackQuery, state: FSMContext):
    """Функция отпралвяет сообщения с ответом, поулченным с API"""
    data = await state.get_data()

    params_to_request = {
        'date': data["date_for_request"],
        'number': data["lesson_num"],
        'faculty': data["faculties"],
        'equipment': data["equipments"],
        'size': data["size"]
    }

    response = await get_data(endpoint=FREE_PLACES_ENDPOINT, params=params_to_request)
    free_places = format_result(response, data)

    await state.update_data(faculties=[])
    await state.update_data(equipments=[])
    await state.update_data(faculties_short_name='')
    await state.update_data(equipments_name='')
    await state.update_data(size=1)

    await callback_query.message.edit_text(
        text=free_places,
        reply_markup=result_keyboard
    )
