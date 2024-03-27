"""
Модуль с логикой inline клавиатур.
"""
from aiogram import F
from aiogram.filters import or_f
from aiogram.types import CallbackQuery
from aiogram_calendar import SimpleCalendar, get_user_locale, SimpleCalendarCallback
from aiogram.filters.callback_data import CallbackData
from datetime import datetime
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart
from aiogram import types, Router


from keyboards.inline import select_lesson_number, find_keyboard
from keyboards.create_faculies_keyboard import create_faculties_keyboard
from keyboards.create_equipment_keyboard import create_equipment_keyboard
from helpers.compare_faculty_num import compare_faculty_num
from helpers.compare_lesson_num import compare_lesson_num
from helpers.compare_equip_num import compare_equip_num
from helpers.compare_faculty_short_name import compare_faculty_short_name
from helpers.compare_eqiup_name import compare_equip_name
from helpers.get_free_classrooms import get_free_classrooms
from keyboards.inline import select_date
from consts.main import *


callback_handlers_router = Router()

@callback_handlers_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    '''По команде /start показывает клавиатуру с кнопкой "Выбрать дату" '''
    await message.answer(text='Выберите дату', reply_markup=select_date)


@callback_handlers_router.callback_query(or_f((F.data == 'select_date'), (F.data == 'back_to_select_date')))
async def show_calendar_keyboard(callback_querry: CallbackQuery):
    '''Функция отправляет клавиатуру с календарём'''
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_querry.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2024, 3, 10), datetime(2025, 12, 31))
    await callback_querry.message.edit_reply_markup(
        reply_markup=await calendar.start_calendar(year=2024, month=3)
    )
@callback_handlers_router.callback_query(SimpleCalendarCallback.filter())
async def callback_calendar_keyboard(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    '''Функция отправляет клавиатуру с выбором пары, после того, как была выбрада дата в календаре'''
    calendar = SimpleCalendar(
        locale=await get_user_locale(callback_query.from_user), show_alerts=True
    )
    calendar.set_dates_range(datetime(2024, 3, 10), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date_from_user=date.strftime("%Y-%m-%d"))
        #Инициализируем пустые поля в сторе FSMContext
        await state.update_data(lesson_num='1')
        await state.update_data(faculties=[])
        await state.update_data(equipments=[])
        await state.update_data(faculties_short_name='')
        await state.update_data(equipments_name='')

        #=============================================
        data = await state.get_data()
        print('les_num = ', data["date_from_user"])
        message_text = f'Дата: {data["date_from_user"]}'
        await callback_query.message.edit_text(text=message_text, reply_markup=select_lesson_number)


@callback_handlers_router.callback_query(F.data == 'back_to_select_lesson_num')
async def show_lesson_num_keyboard(callback_querry: CallbackQuery):
    '''Функция отправляет клавиатуру с выбором номера пары, при нажитие кнопки "назад" в меню клавиатуры факультетов '''
    await callback_querry.message.edit_reply_markup(reply_markup=select_lesson_number)


@callback_handlers_router.callback_query((F.data.in_(LES_NUM)))
async def show_faculties_keyboard(callback_querry: CallbackQuery, state: FSMContext):
    '''Функция отправляет клавиатуру с выбором факультетов после выбора пары'''
    await state.update_data(lesson_num=compare_lesson_num(str(callback_querry.data)))
    data = await state.get_data()
    message_text = f'Дата: {data["date_from_user"]}\nПара: {data["lesson_num"]}'
    await callback_querry.message.edit_text(text=message_text, reply_markup=create_faculties_keyboard())
@callback_handlers_router.callback_query(F.data.startswith('fac_'))
async def callback_faculties_keyboard(callback_querry: CallbackQuery, state: FSMContext):
    '''Функция реагирует на выбор факультетов'''
    data = await state.get_data()
    updated_faculties = data["faculties"]
    updated_faculties.append(compare_faculty_num(str(callback_querry.data)))
    await state.update_data(faculties=updated_faculties)
    data = await state.get_data()

    updated_faculties_short_name = data["faculties_short_name"]
    updated_faculties_short_name += str(compare_faculty_short_name(str(callback_querry.data))) + ', '
    await state.update_data(faculties_short_name=updated_faculties_short_name)

    print('fac = ', data["faculties"])
    print('les_num = ', data["lesson_num"])
    await callback_querry.answer(f'{compare_faculty_short_name(callback_querry.data)}')
@callback_handlers_router.callback_query(F.data == 'back_to_select_faculties')
async def show_faculties_keyboard(callback_querry: CallbackQuery):
    '''Функция отправляет клавиатуру с выбором факультетов после нажатия на кнопку "назад" в меню выбора оснащения'''
    await callback_querry.message.edit_reply_markup(reply_markup=create_faculties_keyboard())



@callback_handlers_router.callback_query(F.data == 'select_equipments')
async def show_equipment_keyboard(callback_querry: CallbackQuery, state: FSMContext):
    '''Функция отправляет клавиатуру с выбором оснащения после выбора факультетов'''
    data = await state.get_data()
    message_text = f'Дата: {data["date_from_user"]}\nПара: {data["lesson_num"]}\nФакультеты: {data["faculties_short_name"]}'
    await callback_querry.message.edit_text(text=message_text, reply_markup=create_equipment_keyboard())
@callback_handlers_router.callback_query(F.data.startswith('equip_'))
async def callback_equipment_keyboard(callback_querry: CallbackQuery, state: FSMContext):
    '''Функция реагирует на выбор оснащения'''
    data = await state.get_data()
    updated_equipments = data["equipments"]
    updated_equipments.append(compare_equip_num(str(callback_querry.data)))
    await state.update_data(equipments=updated_equipments)
    data = await state.get_data()

    updated_equipments_name = data["equipments_name"]
    updated_equipments_name += str(compare_equip_name(str(callback_querry.data))) + ', '
    await state.update_data(equipments_name=updated_equipments_name)

    print('eq = ', data["equipments"])
    await callback_querry.answer(f'{compare_equip_name(callback_querry.data)}')

@callback_handlers_router.callback_query(F.data == 'back_to_select_equipments')
async def show_equipment_keyboard(callback_querry: CallbackQuery):
    '''Функция отправляет клавиатуру с выбором оснащения после нажатия на кнопку "назад"'''
    await callback_querry.message.edit_reply_markup(reply_markup=create_equipment_keyboard())


@callback_handlers_router.callback_query(F.data == 'all_data_is_selected')
async def show_find_keyboard(callback_querry: CallbackQuery, state: FSMContext):
    '''Функция отправляет класиатуру с кнопкой "назад" и "найти" после выбора всех полей в предыдуших клавиатурах'''
    data = await state.get_data()
    message_text = f'Дата: {data["date_from_user"]}\nПара: {data["lesson_num"]}\nФакультеты: {data["faculties_short_name"]}\nОснащение: {data["equipments_name"]}'
    await callback_querry.message.edit_text(text=message_text, reply_markup=find_keyboard)

@callback_handlers_router.callback_query(F.data == 'get_free_classrooms')
async def show_find_keyboard(callback_querry: CallbackQuery, state: FSMContext):
    '''Функция отпралвяет сообщения с ответом, поулченным с API'''
    data = await state.get_data()
    result = get_free_classrooms(data["date_from_user"], data["lesson_num"], data["faculties"], data["equipments"])
    await callback_querry.message.answer(text=result)