#from datetime import datetime
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext


#from helpers.compare_time import compare_time
#from keyboards.create_lessons_is_over import show_lessons_is_over
from helpers.create_messages import create_message
from keyboards.create_lesson_num_keyboard import create_lesson_num_keyboard



async def show_not_over_lessons(callback_query: CallbackQuery, state: FSMContext, selected_date):
    """Функция, сравнивающая время и в зависимости от этого показывающая клавиатуру с выбором пары"""
    #TODO ПОСЛЕ ТЕСТОВ КОММЕНТАРИИ УДАЛИТЬ!

    # current_date = datetime.now()
    data = await state.get_data()

    # current_time = current_date.time().strftime('%H:%M')
    # if selected_date == current_date.strftime('%d.%m.%Y'):
    #     if compare_time("21:30", current_time):
    #         await show_lessons_is_over(callback_query)
    #         return
    #     else:
    #         await callback_query.message.edit_text(
    #             text=create_message(
    #                 params=data,
    #                 type_mes='select_les_num'
    #             ),
    #             reply_markup=await create_lesson_num_keyboard(selected_date=data["date"])
    #         )
    # else:
    #     await callback_query.message.edit_text(
    #         text=create_message(
    #             params=data,
    #             type_mes='select_les_num'
    #         ),
    #         reply_markup=await create_lesson_num_keyboard(selected_date=data["date"])
    #     )
    await callback_query.message.edit_text(
        text=create_message(
            params=data,
            type_mes='select_les_num'
        ),
        reply_markup=await create_lesson_num_keyboard(selected_date=data["date"])
    )
