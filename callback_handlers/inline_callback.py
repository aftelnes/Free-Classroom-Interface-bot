"""
Модуль с логикой inline клавиатур.
"""
from aiogram import F
from aiogram.filters import or_f
from aiogram.types import CallbackQuery
from aiogram_calendar import SimpleCalendar, SimpleCalendarCallback
from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram import types, Router

from datetime import datetime

from keyboards.create_lesson_num_keyboard import create_lesson_num_keyboard
from keyboards.inline import select_date_keyboard

from helpers.create_messages import create_message

from callback_handlers.lesson_num import show_lesson_num_keyboard
from callback_handlers.faculties import show_faculties_keyboard, callback_faculties_keyboard, \
    back_to_show_faculties_keyboard
from callback_handlers.equipments import show_equipment_keyboard, callback_equipment_keyboard, \
    back_to_show_equipments_keyboard
from callback_handlers.size import show_size_keyboard, callback_size_keyboard
from callback_handlers.result import show_result

callback_handlers_router = Router()

@callback_handlers_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    '''По команде /start показывает клавиатуру с кнопкой "Выбрать дату"'''

    await state.update_data(faculties=[])
    await state.update_data(equipments=[])
    await state.update_data(faculties_short_name='Все')
    await state.update_data(equipments_name='Любое')
    await state.update_data(size=1)

    #Тестовое поле
    await state.update_data(faculties_state='')
    await state.update_data(equipments_state='')

    await message.answer(text=create_message(params={}, type_mes='start'), reply_markup=select_date_keyboard)


@callback_handlers_router.callback_query(or_f((F.data == 'select_date'), (F.data == 'back_to_select_date')))
async def show_calendar_keyboard(callback_querry: CallbackQuery):
    """Функция отправляет клавиатуру с календарём"""
    calendar = SimpleCalendar(
        locale='ru_RU', show_alerts=True
    )
    current_date = datetime.now()
    calendar.set_dates_range(datetime(current_date.year, current_date.month, current_date.day), datetime(2025, 12, 31))
    await callback_querry.message.edit_text(text=create_message(params={}, type_mes='select_data'),
        reply_markup=await calendar.start_calendar(year=current_date.year, month=current_date.month)
    )
@callback_handlers_router.callback_query(SimpleCalendarCallback.filter())
async def callback_calendar_keyboard(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    """Функция отправляет клавиатуру с выбором пары, после того, как была выбрада дата в календаре"""
    calendar = SimpleCalendar(
        locale='ru_RU', show_alerts=True
    )
    current_date = datetime.now()
    calendar.set_dates_range(datetime(current_date.year, current_date.month, current_date.day), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date=date.strftime("%d.%m.%Y"))
        await state.update_data(date_for_request=date.strftime("%Y-%m-%d"))
        data = await state.get_data()
        await callback_query.message.edit_text(text=create_message(params=data, type_mes='select_les_num'),
                                               reply_markup=await create_lesson_num_keyboard())

@callback_handlers_router.callback_query()
async def cath_all_callback(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == 'back_to_select_lesson_num':
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
