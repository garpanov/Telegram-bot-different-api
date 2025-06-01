from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.middleware import FSMContext
from aiogram.fsm.state import State, StatesGroup

from locales.lang_search import get_string
from services.db.query import get_lang
from inline_board import get_return_board_inline, get_shares_method_inline, get_shares_return_inline, get_return_board_2_inline
from services.shares.utils import get_price_now

class StateForm(StatesGroup):
	company_name = State()
	company_symbol = State()


rout_shares = Router()
shares = FSInputFile('./images/shares.jfif')

@rout_shares.callback_query(F.data == 'shares')
async def cmd_shares(callback: CallbackQuery, state: FSMContext):
	await state.clear()
	await callback.message.delete()

	lang = await get_lang(callback.from_user.id)
	text_for_response = get_string(lang, 'cmd_shares')
	await callback.message.answer(f"{text_for_response}", reply_markup=get_shares_method_inline(lang))

@rout_shares.callback_query(F.data == 'name_share')
async def cmd_name_share(callback: CallbackQuery, state: FSMContext):
	await state.set_state(StateForm.company_name)
	await callback.message.delete()

	lang = await get_lang(callback.from_user.id)
	text_for_response = get_string(lang, 'cmd_name_share')
	await callback.message.answer(f"{text_for_response}",
	                              reply_markup=get_shares_return_inline(lang))

@rout_shares.message(StateForm.company_name)
async def cmd_price_name(message: Message, state: FSMContext):
	lang = await get_lang(message.from_user.id)
	data = await get_price_now(language=lang, name=message.text)

	if 'error' in data:
		await message.answer(data['error'])
		return

	text_for_response = get_string(lang, 'cmd_price_name').format(symbol=data['symbol'], price=data['price'])
	await message.answer_photo(photo=shares, caption=f'{text_for_response}',
	                     reply_markup=get_return_board_inline(lang), parse_mode='HTML')
	await state.clear()

@rout_shares.callback_query(F.data == 'ticker_share')
async def cmd_symbol_shares(callback: CallbackQuery, state: FSMContext):
	await state.set_state(StateForm.company_symbol)
	await callback.message.delete()

	lang = await get_lang(callback.from_user.id)
	text_for_response = get_string(lang, 'cmd_symbol_shares')
	await callback.message.answer(f"{text_for_response}",
	                              reply_markup=get_shares_return_inline(lang), parse_mode='HTML')


@rout_shares.message(StateForm.company_symbol)
async def cmd_price_symbol(message: Message, state: FSMContext):
	lang = await get_lang(message.from_user.id)
	data = await get_price_now(request_symbol=message.text, language=lang)

	if 'error' in data:
		await message.answer(data['error'])
		return

	text_for_response = get_string(lang, 'cmd_price_symbol').format(symbol=data['symbol'].upper(), price=data['price'])
	await message.answer_photo(photo=shares,
	    caption=f'{text_for_response}',
		reply_markup=get_return_board_inline(lang), parse_mode='HTML')
	await state.clear()