from datetime import datetime
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.create_lesson_num_keyboard import create_lesson_num_keyboard
from cube_bot_calendar.consts.consts import MONTHS
from cube_bot_calendar.create_calendar import create_months_keyboard, create_days_keyboard
from helpers.create_messages import create_message


async def show_month_keyboard(callback_querry: CallbackQuery):
    await callback_querry.message.edit_text(text=create_message(params={}, type_mes='select_month'),
                                            reply_markup=await create_months_keyboard())


async def show_days_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция показывающая клавиатуру календаря"""
    selected_month = callback_query.data[6:]
    await state.update_data(month=selected_month)
    await state.update_data(month_name=MONTHS[int(selected_month)])
    data = await state.get_data()

    await callback_query.message.edit_text(text=create_message(params=data, type_mes='select_day'),
                                           reply_markup=await create_days_keyboard(2024, int(selected_month)))


async def back_to_show_day_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция показывает клавиатуру с выбором дня, при нажатии на кнопку 'назад' """
    data = await state.get_data()
    selected_month = data["month"]
    data = await state.get_data()
    print()
    await callback_query.message.edit_text(text=create_message(params=data, type_mes='select_day'),
                                           reply_markup=await create_days_keyboard(2024, int(selected_month)))


async def callback_days_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция отлавливает нажатие на определённый день"""
    current_date = datetime.now()

    data = await state.get_data()
    selected_month = data["month"]
    selected_day = callback_query.data[4:]

    if int(selected_month) == current_date.month and int(selected_day) < current_date.day:
        await callback_query.answer(text='Этот день закончился!')
        return

    data = await state.get_data()

    selected_date = datetime(current_date.year, int(data["month"]), int(selected_day)).strftime("%d.%m.%Y")
    date_for_request = datetime(current_date.year, int(data["month"]), int(selected_day)).strftime("%Y-%m-%d")
    await state.update_data(date=selected_date)
    await state.update_data(date_for_request=date_for_request)
    data = await state.get_data()

    await callback_query.message.edit_text(text=create_message(params=data, type_mes='select_les_num'),
                                           reply_markup=await create_lesson_num_keyboard())


async def callback_today_button(callback_query: CallbackQuery, state: FSMContext):
    """Функция обработки кнопки 'сегодня'"""

    selected_month = datetime.now().month
    month_name = MONTHS[int(selected_month)]
    await state.update_data(month_name=month_name)
    await state.update_data(month=datetime.now().month)
    await state.update_data(date=datetime.now().strftime("%d.%m.%Y"))
    await state.update_data(date_for_request=datetime.now().strftime("%Y-%m-%d"))
    data = await state.get_data()

    await callback_query.message.edit_text(text=create_message(params=data, type_mes='select_les_num'),
                                           reply_markup=await create_lesson_num_keyboard())
