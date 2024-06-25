from datetime import datetime
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from cube_bot_calendar.consts.consts import MONTHS
from cube_bot_calendar.create_calendar import create_months_keyboard, create_days_keyboard
from helpers.create_messages import create_message

from helpers.show_not_over_lessons import show_not_over_lessons
from helpers.get_data import get_data

from api.consts import LESSONS_NUM_ENDPOINT


async def show_month_keyboard(callback_querry: CallbackQuery, state: FSMContext):
    """Функция показывает клавиатуру с календарём"""
    current_month = datetime.now().month

    #Узнаём время последней пары и записываем его в стейт
    lessons = await get_data(endpoint=LESSONS_NUM_ENDPOINT)
    await state.update_data(last_lesson_time=lessons[-1]['time'])

    await callback_querry.message.edit_text(
        text=create_message(
            params={},
            type_mes='select_month'
        ),
        reply_markup=await create_months_keyboard(from_month=current_month)
    )


async def show_days_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция показывающая клавиатуру календаря"""
    selected_month = callback_query.data[6:]
    await state.update_data(month=selected_month)
    await state.update_data(month_name=MONTHS[int(selected_month)])
    data = await state.get_data()

    await callback_query.message.edit_text(
        text=create_message(params=data, type_mes='select_day'),
        reply_markup=await create_days_keyboard(
            year=2024,
            month=int(selected_month),
            over_day_symbol='❎',
            over_day_time=data["last_lesson_time"]
        )
    )


async def back_to_show_day_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция показывает клавиатуру с выбором дня, при нажатии на кнопку 'назад' """
    data = await state.get_data()
    selected_month = data["month"]
    data = await state.get_data()

    await callback_query.message.edit_text(
        text=create_message(params=data, type_mes='select_day'),
        reply_markup=await create_days_keyboard(
            year=2024,
            month=int(selected_month),
            over_day_symbol='❎',
            over_day_time=data["last_lesson_time"]
        )
    )


async def callback_days_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция отлавливает нажатие на определённый день"""
    current_date = datetime.now()

    selected_day = callback_query.data[4:]

    if selected_day == 'is_over':
        await callback_query.answer(text='Этот день закончился!')
        return

    data = await state.get_data()

    selected_date = datetime(current_date.year, int(data["month"]), int(selected_day)).strftime("%d.%m.%Y")
    date_for_request = datetime(current_date.year, int(data["month"]), int(selected_day)).strftime("%Y-%m-%d")
    await state.update_data(date=selected_date)
    await state.update_data(date_for_request=date_for_request)

    await show_not_over_lessons(
        callback_query=callback_query,
        state=state,
        selected_date=selected_date
    )

async def callback_today_button(callback_query: CallbackQuery, state: FSMContext):
    """Функция обработки кнопки 'сегодня'"""
    current_date = datetime.now()

    selected_month = current_date.month
    month_name = MONTHS[int(selected_month)]
    await state.update_data(month_name=month_name)
    await state.update_data(month=current_date.month)
    await state.update_data(date=current_date.strftime("%d.%m.%Y"))
    await state.update_data(date_for_request=current_date.strftime("%Y-%m-%d"))

    await show_not_over_lessons(
        callback_query=callback_query,
        state=state,
        selected_date=current_date.strftime("%d.%m.%Y")
    )
