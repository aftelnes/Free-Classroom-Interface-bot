"""
Модуль с логикой работа клавиатуры с выбором факультетов
"""
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.create_faculies_keyboard import create_faculties_state, create_faculties_keyboard
from helpers.create_messages import create_message


async def show_faculties_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция отправляет клавиатуру с выбором факультетов после выбора пары"""
    await state.update_data(lesson_num=int(str(callback_query.data)[4:]))
    faculties = await create_faculties_state()
    await state.update_data(faculties_state=faculties)
    data = await state.get_data()

    await callback_query.message.edit_text(
        text=create_message(
            params=data,
            type_mes='select_faculty'
        ),
        reply_markup=await create_faculties_keyboard(faculties_ary_state=data["faculties_state"])
    )


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
    if updated_faculties_short_name == 'Все':
        updated_faculties_short_name = ''

    #Получаем текст кнопки, при нажатии
    inline_keyboard = callback_query.message.reply_markup.inline_keyboard
    for row in inline_keyboard:
        for button in row:
            if button.callback_data == callback_query.data:
                button_text = button.text
                if button_text not in updated_faculties_short_name and str(button_text)[1:] not in updated_faculties_short_name:
                    updated_faculties_short_name += str(button_text) + ', '
                elif str(button_text)[1:] in updated_faculties_short_name:
                    updated_faculties_short_name = updated_faculties_short_name.replace(str(button_text)[1:]+ ', ', '')
                for i in range(len(faculties_state)):
                    if faculties_state[i]["short_name"] == button_text or '✅'+faculties_state[i]["short_name"] == button_text:
                        faculties_state[i]["is_selected"] = not(faculties_state[i]["is_selected"])
                        await state.update_data(faculties_short_name=updated_faculties_short_name)
                        await callback_query.message.edit_reply_markup(
                            reply_markup=await create_faculties_keyboard(faculties_ary_state=faculties_state))


async def back_to_show_faculties_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция отправляет клавиатуру с выбором факультетов после нажатия на кнопку "назад" в меню выбора оснащения"""
    data = await state.get_data()
    await callback_query.message.edit_text(
        text=create_message(
            params=data,
            type_mes='select_faculty'
        ),
        reply_markup=await create_faculties_keyboard(faculties_ary_state=data["faculties_state"])
    )
