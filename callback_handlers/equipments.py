"""
Модуль с логикой работы клавиатуры с оснащением
"""
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from keyboards.create_equipment_keyboard import (create_equipments_keyboard, create_equipments_state)
from helpers.create_messages import create_message


async def show_equipment_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция отправляет клавиатуру с выбором оснащения после выбора факультетов"""
    equipments = await create_equipments_state()
    await state.update_data(equipments_state=equipments)
    data = await state.get_data()

    #Если факультеты не выбраны, то добавит вместо этого слово "Все"
    if data["faculties_short_name"] == '':
        await state.update_data(faculties_short_name='Все')
    data = await state.get_data()

    await callback_query.message.edit_text(text=create_message(params=data, type_mes='select_equipment'),
                                           reply_markup=await create_equipments_keyboard(data["equipments_state"]))

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
    if updated_equipments_name == 'Любое':
        updated_equipments_name = ''

    inline_keyboard = callback_query.message.reply_markup.inline_keyboard
    for row in inline_keyboard:
        for button in row:
            if button.callback_data == callback_query.data:
                button_text = button.text
                if button_text not in updated_equipments_name and str(button_text)[1:] not in updated_equipments_name:
                    updated_equipments_name += str(button_text) + ', '
                elif str(button_text)[1:] in updated_equipments_name:
                    updated_equipments_name = updated_equipments_name.replace(str(button_text)[1:] + ', ', '')
                for i in range(len(equipments_state)):
                    if equipments_state[i]["name"] == button_text or '✅'+equipments_state[i]["name"] == button_text:
                        equipments_state[i]["is_selected"] = not(equipments_state[i]["is_selected"])
                        await state.update_data(equipments_name=updated_equipments_name)
                        await callback_query.message.edit_reply_markup(
                            reply_markup=await create_equipments_keyboard(equipments_state)
                        )

async def back_to_show_equipments_keyboard(callback_query: CallbackQuery, state: FSMContext):
    """Функция отправляет клавиатуру с выбором оснащенияп осле нажатия на кнопку "назад" в меню выбора вместимости"""
    data = await state.get_data()
    await callback_query.message.edit_text(text=create_message(params=data, type_mes='select_equipment'),
                                           reply_markup=await create_equipments_keyboard(data["equipments_state"]))