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
from keyboards.inline import find_keyboard, select_size
from keyboards.inline import select_date
from keyboards.create_faculies_keyboard import create_faculties_keyboard
from keyboards.create_equipment_keyboard import create_equipment_keyboard

from helpers.compare_lesson_num import compare_lesson_num
from helpers.compare_equip_num import compare_equip_num
from helpers.compare_eqiup_name import compare_equip_name
from helpers.get_data import get_data
from helpers.format_result import format_result



callback_handlers_router = Router()

#Тестирую другой вариант календаря
from aiogram_calendar import DialogCalendar, DialogCalendarCallback
@callback_handlers_router.message(F.text.lower() == 'dialog calendar w month')
async def dialog_cal_handler_month(message: types.Message):
    await message.answer(
        "Please <b>select</b> a date:\n—————————————————— ",
        reply_markup=await DialogCalendar(
            locale='ru_ru'
        ).start_calendar(year=2024, month=4)
    )
@callback_handlers_router.callback_query(DialogCalendarCallback.filter())
async def process_dialog_calendar(callback_query: CallbackQuery, callback_data: CallbackData):
    selected, date = await DialogCalendar(
        locale='ru_RU'
    ).process_selection(callback_query, callback_data)
    if selected:
        await callback_query.message.answer(
            f'You selected {date.strftime("%d/%m/%Y")}',
        )

@callback_handlers_router.message(F.text.lower() == 'navigation calendar')
async def nav_cal_handler(message: types.Message):
    await message.answer(
        "Please select a date: ",
        reply_markup=await SimpleCalendar(locale='ru_RU').start_calendar()
    )

#=================================




@callback_handlers_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    '''По команде /start показывает клавиатуру с кнопкой "Выбрать дату"'''

    await state.update_data(faculties=[])
    await state.update_data(equipments=[])
    await state.update_data(faculties_short_name='')
    await state.update_data(equipments_name='')
    await state.update_data(size=1)

    await message.answer(text='Данный инструмент позволяет просто\nи быстро найти свободную аудиторию!', reply_markup=select_date)


@callback_handlers_router.callback_query(or_f((F.data == 'select_date'), (F.data == 'back_to_select_date')))
async def show_calendar_keyboard(callback_querry: CallbackQuery):
    '''Функция отправляет клавиатуру с календарём'''
    calendar = SimpleCalendar(
        locale='ru_RU', show_alerts=True
    )
    current_date = datetime.now()
    calendar.set_dates_range(datetime(current_date.year, current_date.month, current_date.day), datetime(2025, 12, 31))
    await callback_querry.message.edit_text(text='Выберите дату: \n——————————————————',
        reply_markup=await calendar.start_calendar(year=current_date.year, month=current_date.month)
    )
@callback_handlers_router.callback_query(SimpleCalendarCallback.filter())
async def callback_calendar_keyboard(callback_query: CallbackQuery, callback_data: CallbackData, state: FSMContext):
    '''Функция отправляет клавиатуру с выбором пары, после того, как была выбрада дата в календаре'''
    calendar = SimpleCalendar(
        locale='ru_RU', show_alerts=True
    )
    current_date = datetime.now()
    calendar.set_dates_range(datetime(current_date.year, current_date.month, current_date.day), datetime(2025, 12, 31))
    selected, date = await calendar.process_selection(callback_query, callback_data)
    if selected:
        await state.update_data(date_from_user=date.strftime("%Y-%m-%d"))
        data = await state.get_data()
        message_text = f'Дата: <b>{data["date_from_user"]}</b>\nВыберите пару: \n——————————————————'
        await callback_query.message.edit_text(text=message_text, reply_markup=await create_lesson_num_keyboard())



@callback_handlers_router.callback_query(F.data == 'back_to_select_lesson_num')
async def show_lesson_num_keyboard(callback_query: CallbackQuery):
    '''Функция отправляет клавиатуру с выбором номера пары, при нажитие кнопки "назад" в меню клавиатуры факультетов '''
    await callback_query.message.edit_reply_markup(reply_markup=await create_lesson_num_keyboard())

@callback_handlers_router.callback_query(F.data.startswith('les_'))
async def show_faculties_keyboard(callback_query: CallbackQuery, state: FSMContext):
    '''Функция отправляет клавиатуру с выбором факультетов после выбора пары'''
    await state.update_data(lesson_num=compare_lesson_num(str(callback_query.data)))
    data = await state.get_data()
    message_text = f'Дата: <b>{data["date_from_user"]}</b>\nПара: <b>{data["lesson_num"]}</b>\nВыберите факультет: \n——————————————————'
    await callback_query.message.edit_text(text=message_text, reply_markup=await create_faculties_keyboard())

@callback_handlers_router.callback_query(F.data.startswith('fac_'))
async def callback_faculties_keyboard(callback_query: CallbackQuery, state: FSMContext):
    '''Функция реагирует на выбор факультетов'''
    data = await state.get_data()

    #TODO Убрал функции заглушки для факультетов compare... но теперь захламился код уже непосредственно в логике колбэков
    #TODO в последствии уберу и все остальные, можешь ли дать совет как разгрузить теперь логику, описанную ниже
    #Присваиваем числовое значение факультета в стор====
    updated_faculties = data["faculties"]
    updated_faculties.append(int(callback_query.data[4:]))
    await state.update_data(faculties=updated_faculties)
    #===================================================

    #Получаем текст кнопки, при нажатии
    updated_faculties_short_name = data["faculties_short_name"]
    inline_keyboard = callback_query.message.reply_markup.inline_keyboard
    for row in inline_keyboard:
        for button in row:
            if button.callback_data == callback_query.data:
                button_text = button.text
                if button_text in updated_faculties_short_name:
                    await callback_query.answer(f"{button_text} уже добавлен")
                    break
                updated_faculties_short_name += str(button_text) + ' '
    #Добавляем текст кнопки (т.е. название факультета) в стор, откуда потом покажем пользователю, выбранные им факультеты
    await state.update_data(faculties_short_name=updated_faculties_short_name)
    #Реагируем на нажатие кнопки и показыавем текст кнопки (т.е. название факультета)
    await callback_query.answer(button_text)
    #======================================================================

@callback_handlers_router.callback_query(F.data == 'back_to_select_faculties')
async def show_faculties_keyboard(callback_query: CallbackQuery):
    '''Функция отправляет клавиатуру с выбором факультетов после нажатия на кнопку "назад" в меню выбора оснащения'''
    await callback_query.message.edit_reply_markup(reply_markup=await create_faculties_keyboard())



@callback_handlers_router.callback_query(F.data == 'select_equipments')
async def show_equipment_keyboard(callback_query: CallbackQuery, state: FSMContext):
    '''Функция отправляет клавиатуру с выбором оснащения после выбора факультетов'''
    data = await state.get_data()
    message_text = f'Дата: <b>{data["date_from_user"]}</b>\nПара: <b>{data["lesson_num"]}</b>\nФакультеты: <b>{data["faculties_short_name"]}</b>\nВыберите оснащение: \n——————————————————'
    await callback_query.message.edit_text(text=message_text, reply_markup=await create_equipment_keyboard())
@callback_handlers_router.callback_query(F.data.startswith('equip_'))
async def callback_equipment_keyboard(callback_query: CallbackQuery, state: FSMContext):
    '''Функция реагирует на выбор оснащения'''
    data = await state.get_data()
    updated_equipments = data["equipments"]
    updated_equipments.append(compare_equip_num(str(callback_query.data)))
    await state.update_data(equipments=updated_equipments)
    data = await state.get_data()

    updated_equipments_name = data["equipments_name"]
    updated_equipments_name += str(compare_equip_name(str(callback_query.data))) + ' '
    await state.update_data(equipments_name=updated_equipments_name)

    await callback_query.answer(f'{compare_equip_name(callback_query.data)}')

@callback_handlers_router.callback_query(F.data == 'back_to_select_equipments')
async def show_equipment_keyboard(callback_query: CallbackQuery):
    '''Функция отправляет клавиатуру с выбором оснащения после нажатия на кнопку "назад"'''
    await callback_query.message.edit_reply_markup(reply_markup=await create_equipment_keyboard())




@callback_handlers_router.callback_query(F.data == 'select_size')
async def show_size_keyboard(callback_query: CallbackQuery, state: FSMContext):
        '''Фнукия отправляет клавиатуру с выбором кол-ва необходимых посадочных мест'''
        data = await state.get_data()
        message_text = (f'Дата: <b>{data["date_from_user"]}</b>\nПара: <b>{data["lesson_num"]}</b>\nФакультеты: '
                        f'<b>{data["faculties_short_name"]}</b>\nОснащение: <b>{data["equipments_name"]}</b>\nВыберите вместимость: \n——————————————————')
        await callback_query.message.edit_text(text=message_text, reply_markup=select_size)
@callback_handlers_router.callback_query(F.data.startswith('size_'))
async def callback_size_keyboard(callback_querry: CallbackQuery, state: FSMContext):
        await state.update_data(size=int(callback_querry.data[5:]))

        inline_keyboard = callback_querry.message.reply_markup.inline_keyboard
        for row in inline_keyboard:
            for button in row:
                if button.callback_data == callback_querry.data:
                    button_text = button.text
                    await callback_querry.answer(button_text)

@callback_handlers_router.callback_query(F.data == 'all_data_is_selected')
async def show_find_keyboard(callback_query: CallbackQuery, state: FSMContext):
    '''Функция отправляет клавиатуру с кнопкой "назад" и "найти" после выбора всех полей в предыдуших клавиатурах'''
    data = await state.get_data()
    message_text = (f'Дата: <b>{data["date_from_user"]}</b>\nПара: <b>{data["lesson_num"]}</b>\nФакультеты: <b>{data["faculties_short_name"]}</b>\n'
                    f'Оснащение: <b>{data["equipments_name"]}</b>\nКол-во мест: <b>{data["size"]}</b> \n——————————————————')
    await callback_query.message.edit_text(text=message_text, reply_markup=find_keyboard)

@callback_handlers_router.callback_query(F.data == 'get_free_classrooms')
async def show_find_keyboard(callback_query: CallbackQuery, state: FSMContext):
    '''Функция отпралвяет сообщения с ответом, поулченным с API'''
    data = await state.get_data()

    params_to_request = {
        'date': data["date_from_user"],
        'number': data["lesson_num"],
        'faculty': data["faculties"],
        'equipment': data["equipments"],
        'size': data["size"]
    }

    response = await get_data(data_type='FREE_PLACES', params=params_to_request)
    free_places = format_result(response)

    await callback_query.message.answer(text=free_places)