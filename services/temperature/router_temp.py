from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.middleware import FSMContext

from inline_board import return_board_inline, return_board_2_inline
from services.temperature.utils import fetch

class StateForm(StatesGroup):
	city = State()

rout_temp = Router()
jacket = FSInputFile('./images/jacket.jfif')
t_shirt = FSInputFile('./images/t-shirt.jfif')

@rout_temp.callback_query(F.data == 'temperature')
async def cmd_temperature(callback: CallbackQuery, state: FSMContext):
	await callback.message.delete()
	await state.set_state(StateForm.city)

	await callback.message.answer("Чтобы узнать температуру 🌡️\nвведите название города 👇", reply_markup=return_board_2_inline)

@rout_temp.message(StateForm.city)
async def cmd_search_city(message: Message, state: FSMContext):
	city_name = message.text
	data = await fetch(city_name)
	if 'error' in data:
		if data['error'] == 'Not Found':
			await message.answer("Город не найден 🤷‍♂️.\nУбедитесь, что название введено <b>правильно</b>, и попробуйте снова 👇")
		else:
			await message.answer('В настоящий момент сервис поиска температуры города <b>недоступен</b>🥺.\nПожалуйста, попробуйте позже.',
			                     reply_markup=return_board_inline)
			await state.clear()
		return

	temperature = data['temperature']
	city = data['city']
	if temperature < 15:
		await message.answer_photo(photo=jacket, caption=f'Сегодня в городе <b>{city}</b> 🏘️\nтемпература — <b>{temperature}°C</b>,\nхолодно, одень куртку 🥶',
		                     reply_markup=return_board_inline, parse_mode='HTML')
	else:
		await message.answer_photo(photo=t_shirt, caption=f'Сегодня в городе <b>{city}</b> 🏘️\nтемпература — <b>{temperature}°C</b>,\nотличный день, можно бегать в футболке 🌞',
		                     reply_markup=return_board_inline, parse_mode='HTML')
	await state.clear()



