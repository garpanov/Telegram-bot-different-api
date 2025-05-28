from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.middleware import FSMContext

from inline_board import return_board_inline
from services.temperature.utils import fetch

class StateForm(StatesGroup):
	city = State()

rout_temp = Router()

@rout_temp.callback_query(F.data == 'temperature')
async def cmd_temperature(callback: CallbackQuery, state: FSMContext):
	await callback.message.delete()
	await state.set_state(StateForm.city)

	await callback.message.answer("Чтобы узнать температуру, введите название этого города латиницей"
	                              "(например, 'Kyiv' вместо 'Киев')👇")

@rout_temp.message(StateForm.city)
async def cmd_search_city(message: Message, state: FSMContext):
	city_name = message.text
	data = await fetch(city_name)
	if 'error' in data:
		if data['error'] == 'Not Found':
			await message.answer("Город не найден. Введите название латиницей (например, 'Kyiv' вместо 'Киев'). 👇")
		else:
			await message.answer('В настоящий момент сервис поиска температуры города недоступен. Пожалуйста, попробуйте позже.',
			                     reply_markup=return_board_inline)
			await state.clear()
		return

	temperature = data['temperature']
	if temperature < 15:
		await message.answer(f'Сегодня температура {temperature} градусов, холодно, одень куртку.',
		                     reply_markup=return_board_inline)
	else:
		await message.answer(f'Сегодня {temperature} градусов, отличный день, можно бегать в футболке.',
		                     reply_markup=return_board_inline)
	await state.clear()



