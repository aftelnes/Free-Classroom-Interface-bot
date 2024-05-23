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
from keyboards.inline import find_keyboard, select_size_keyboard ,select_date_keyboard, result_keyboard
from keyboards.create_equipment_keyboard import create_equipment_keyboard

from helpers.get_data import get_data
from helpers.format_result import format_result
from helpers.create_messages import create_message

from api.consts import FREE_PLACES_ENDPOINT

from keyboards.create_faculies_keyboard import (create_faculties_state, create_faculties_keyboard)
from keyboards.create_equipment_keyboard import (create_equipments_keyboard, create_equipments_state)

callback_handlers_router = Router()

@callback_handlers_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    '''По команде /start показывает клавиатуру с кнопкой "Выбрать дату"'''

    await state.update_data(faculties=[])
    await state.update_data(equipments=[])
    await state.update_data(faculties_short_name='')
    await state.update_data(equipments_name='')
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



@callback_handlers_router.callback_query(F.data == 'back_to_select_lesson_num')
async def show_lesson_num_keyboard(callback_query: CallbackQuery):
    """Функция отправляет клавиатуру с выбором номера пары, при нажитие кнопки "назад" в меню клавиатуры факультетов"""
    await callback_query.message.edit_reply_markup(reply_markup=await create_lesson_num_keyboard())

@callback_handlers_router.callback_query(F.data.startswith('les_'))
async def show_faculties_keyboard(callback_query: CallbackQuery, state: FSMContext):
    '''Функция отправляет клавиатуру с выбором факультетов после выбора пары'''
    await state.update_data(lesson_num=int(str(callback_query.data)[4:]))
    faculties = await create_faculties_state()
    await state.update_data(faculties_state=faculties)
    data = await state.get_data()
    await callback_query.message.edit_text(text=create_message(params=data, type_mes='select_faculty'),
                                           reply_markup=await create_faculties_keyboard(data["faculties_state"]))

@callback_handlers_router.callback_query(F.data.startswith('fac_'))
async def callback_faculties_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция реагирует на выбор факультетов"""
    data = await state.get_data()

    #Присваиваем числовое значение факультета в стор====
    faculty_id = int(callback_query.data[4:])
    updated_faculties = data["faculties"]
    if faculty_id not in updated_faculties:
        updated_faculties.append(faculty_id)
        await state.update_data(faculties=updated_faculties)
    #===================================================

    faculties_state = data["faculties_state"]

    updated_faculties_short_name = data["faculties_short_name"]

    #Получаем текст кнопки, при нажатии
    inline_keyboard = callback_query.message.reply_markup.inline_keyboard
    for row in inline_keyboard:
        for button in row:
            if button.callback_data == callback_query.data:
                button_text = button.text
                if button_text not in updated_faculties_short_name and str(button_text)[1:] not in updated_faculties_short_name:
                    updated_faculties_short_name += str(button_text) + ' '
                elif str(button_text)[1:] in updated_faculties_short_name:
                    updated_faculties_short_name = updated_faculties_short_name.replace(str(button_text)[1:], '')
                for i in range(len(faculties_state)):
                    if faculties_state[i]["short_name"] == button_text or '✅'+faculties_state[i]["short_name"] == button_text:
                        faculties_state[i]["is_selected"] = not(faculties_state[i]["is_selected"])
                        await state.update_data(faculties_short_name=updated_faculties_short_name)
                        await callback_query.message.edit_reply_markup(
                            reply_markup=await create_faculties_keyboard(faculties_state))

@callback_handlers_router.callback_query(F.data == 'select_faculties')
async def show_faculties_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция отправляет клавиатуру с выбором факультетов после нажатия на кнопку "назад" в меню выбора оснащения"""
    data = await state.get_data()
    faculties_state = data["faculties_state"]
    await callback_query.message.edit_reply_markup(reply_markup=await create_faculties_keyboard(faculties_state))



@callback_handlers_router.callback_query(F.data == 'select_equipments')
async def show_equipment_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция отправляет клавиатуру с выбором оснащения после выбора факультетов"""
    equipments = await create_equipments_state()
    await state.update_data(equipments_state=equipments)
    data = await state.get_data()
    await callback_query.message.edit_text(text=create_message(params=data, type_mes='select_equipment'),
                                           reply_markup=await create_equipments_keyboard(data["equipments_state"]))
# @callback_handlers_router.callback_query(F.data.startswith('equip_'))
# async def callback_equipment_keyboard(callback_query: CallbackQuery, state: FSMContext):
#     """Функция реагирует на выбор оснащения"""
#     data = await state.get_data()
#     updated_equipments = data["equipments"]
#     updated_equipments.append(int(callback_query.data[6:]))
#     await state.update_data(equipments=updated_equipments)
#
#
#     updated_equipments_name = data["equipments_name"]
#     inline_keyboard = callback_query.message.reply_markup.inline_keyboard
#     for row in inline_keyboard:
#         for button in row:
#             if button.callback_data == callback_query.data:
#                 button_text = button.text
#                 if button_text in updated_equipments_name:
#                     await callback_query.answer(f"{button_text} уже добавлен")
#                     break
#                 updated_equipments_name += str(button_text) + ' '
#
#     await state.update_data(equipments_name=updated_equipments_name)
#
#     await callback_query.answer(button_text)
@callback_handlers_router.callback_query(F.data.startswith('equip_'))
async def callback_equipment_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция реагирует на выбор оснащения"""
    data = await state.get_data()


    equipment_id = int(callback_query.data[6:])
    updated_equipments = data["equipments"]
    if equipment_id not in updated_equipments:
        updated_equipments.append(equipment_id)
        await state.update_data(equipments=updated_equipments)


    equipments_state = data["equipments_state"]
    updated_equipments_name = data["equipments_name"]

    inline_keyboard = callback_query.message.reply_markup.inline_keyboard
    for row in inline_keyboard:
        for button in row:
            if button.callback_data == callback_query.data:
                button_text = button.text
                if button_text not in updated_equipments_name and str(button_text)[1:] not in updated_equipments_name:
                    updated_equipments_name += str(button_text) + ' '
                elif str(button_text)[1:] in updated_equipments_name:
                    updated_equipments_name = updated_equipments_name.replace(str(button_text)[1:], '')
                for i in range(len(equipments_state)):
                    if equipments_state[i]["name"] == button_text or '✅'+equipments_state[i]["name"] == button_text:
                        equipments_state[i]["is_selected"] = not(equipments_state[i]["is_selected"])
                        await state.update_data(equipments_name=updated_equipments_name)
                        await callback_query.message.edit_reply_markup(
                            reply_markup=await create_equipments_keyboard(equipments_state)
                        )


@callback_handlers_router.callback_query(F.data == 'select_size')
async def show_size_keyboard(callback_query: CallbackQuery, state: FSMContext):
        """Фнукия отправляет клавиатуру с выбором кол-ва необходимых посадочных мест"""
        data = await state.get_data()
        await callback_query.message.edit_text(text=create_message(params=data, type_mes='select_size'),
                                               reply_markup=select_size_keyboard)
@callback_handlers_router.callback_query(F.data.startswith('size_'))
async def callback_size_keyboard(callback_query: CallbackQuery, state: FSMContext):
        await state.update_data(size=int(callback_query.data[5:]))
        data = await state.get_data()
        await callback_query.message.edit_text(text=create_message(params=data, type_mes='find'),
                                               reply_markup=find_keyboard)

@callback_handlers_router.callback_query(F.data == 'get_free_classrooms')
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

    await callback_query.message.edit_text(text=free_places, reply_markup=result_keyboard)
