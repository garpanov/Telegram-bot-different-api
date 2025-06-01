from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.middleware import FSMContext

from locales.lang_search import get_string
from services.db.query import get_lang
from inline_board import get_return_board_inline, get_return_board_2_inline, get_variants_temp_inline
from services.temperature.utils import fetch, fetch_api_geo

class StateForm(StatesGroup):
	city = State()

rout_temp = Router()
jacket = FSInputFile('./images/jacket.jfif')
t_shirt = FSInputFile('./images/t-shirt.jfif')

@rout_temp.callback_query(F.data == 'temperature_variants')
async def cmd_temperature_variants(callback: CallbackQuery):
	await callback.message.delete()
	lang = await get_lang(callback.from_user.id)
	text_for_response = get_string(lang, 'cmd_temperature_variants')

	await callback.message.answer(f"{text_for_response}", reply_markup=get_variants_temp_inline(lang))

@rout_temp.callback_query(F.data == 'temperature')
async def cmd_temperature(callback: CallbackQuery, state: FSMContext):
	await callback.message.delete()
	await state.set_state(StateForm.city)

	lang = await get_lang(callback.from_user.id)
	text_for_response = get_string(lang, 'cmd_temperature')
	await callback.message.answer(f"{text_for_response}", reply_markup=get_return_board_2_inline(lang))

@rout_temp.callback_query(F.data == 'geolocation')
async def cmd_temp_geo(callback: CallbackQuery):
	await callback.message.delete()

@rout_temp.message(StateForm.city)
async def cmd_search_city(message: Message, state: FSMContext):
	city_name = message.text
	data = await fetch(city_name)

	lang = await get_lang(message.from_user.id)
	if 'error' in data:
		if data['error'] == 'Not Found':
			text_for_response = get_string(lang, 'cmd_search_city_not_found')
			await message.answer(f'{text_for_response}', parse_mode='HTML')
		else:
			text_for_response = get_string(lang, 'cmd_search_city_error')
			await message.answer(f'{text_for_response}',
			                     reply_markup=get_return_board_inline(lang), parse_mode='HTML')
			await state.clear()
		return

	temperature = data['temperature']
	city = data['city']
	if temperature < 15:
		text_for_response = get_string(lang, 'cmd_search_city_<15').format(city=city, temperature=temperature)
		await message.answer_photo(photo=jacket, caption=f'{text_for_response}',
		                     reply_markup=get_return_board_inline(lang), parse_mode='HTML')
	else:
		text_for_response = get_string(lang, 'cmd_search_city_>15').format(city=city, temperature=temperature)
		await message.answer_photo(photo=t_shirt, caption=f'{text_for_response}',
		                     reply_markup=get_return_board_inline(lang), parse_mode='HTML')
	await state.clear()



