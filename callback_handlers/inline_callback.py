"""
Модуль с логикой inline клавиатур.
"""
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram import types, Router


from helpers.create_messages import create_message

from callback_handlers.lesson_num import show_lesson_num_keyboard
from callback_handlers.faculties import show_faculties_keyboard, callback_faculties_keyboard, \
    back_to_show_faculties_keyboard
from callback_handlers.equipments import show_equipment_keyboard, callback_equipment_keyboard, \
    back_to_show_equipments_keyboard
from callback_handlers.size import show_size_keyboard, callback_size_keyboard
from callback_handlers.result import show_result
from callback_handlers.calendar import show_month_keyboard, show_days_keyboard, back_to_show_day_keyboard, \
    callback_days_keyboard, callback_today_button

from cube_bot_calendar.consts.keyboard import select_month_keyboard

callback_handlers_router = Router()


@callback_handlers_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    """По команде /start показывает клавиатуру с кнопкой "Выбрать дату"""

    await state.update_data(faculties=[])
    await state.update_data(equipments=[])
    await state.update_data(faculties_short_name='Все')
    await state.update_data(equipments_name='Любое')
    await state.update_data(size=1)

    await state.update_data(faculties_state='')
    await state.update_data(equipments_state='')

    await state.update_data(month='')
    await state.update_data(month_name='')
    await state.update_data(date='')
    await state.update_data(date_for_request='')

    await message.answer(text=create_message(params={}, type_mes='start'), reply_markup=select_month_keyboard)


@callback_handlers_router.callback_query()
async def cath_all_callback(callback_query: CallbackQuery, state: FSMContext):
    """Обработчик всех callback"""

    if callback_query.data == 'select_month':
        await show_month_keyboard(callback_query)
    elif 'month_' in callback_query.data:
        await show_days_keyboard(callback_query, state)
    elif callback_query.data == 'today':
        await callback_today_button(callback_query, state)
    elif 'day_' in callback_query.data:
        await callback_days_keyboard(callback_query, state)
    elif callback_query.data == 'select_day':
        await back_to_show_day_keyboard(callback_query, state)
    elif callback_query.data == 'back_to_select_lesson_num':
        await show_lesson_num_keyboard(callback_query, state)
    elif 'les_' in callback_query.data:
        await show_faculties_keyboard(callback_query, state)
    elif 'fac_' in callback_query.data:
        await callback_faculties_keyboard(callback_query, state)
    elif callback_query.data == 'select_faculties':
        await back_to_show_faculties_keyboard(callback_query, state)
    elif callback_query.data == 'select_equipments':
        await show_equipment_keyboard(callback_query, state)
    elif callback_query.data == 'back_to_select_equipments':
        await back_to_show_equipments_keyboard(callback_query, state)
    elif 'equip_' in callback_query.data:
        await callback_equipment_keyboard(callback_query, state)
    elif callback_query.data == 'select_size':
        await show_size_keyboard(callback_query, state)
    elif 'size_' in callback_query.data:
        await callback_size_keyboard(callback_query, state)
    elif callback_query.data == 'get_free_classrooms':
        await show_result(callback_query, state)
