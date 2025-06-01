from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, FSInputFile
from aiogram.fsm.middleware import FSMContext
from aiogram.fsm.state import State, StatesGroup

from inline_board import return_board_inline, shares_method_inline, shares_return_inline, return_board_2_inline
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
	await callback.message.answer("Выберите способ получения цены акции 👇", reply_markup=shares_method_inline)

@rout_shares.callback_query(F.data == 'name_share')
async def cmd_name_share(callback: CallbackQuery, state: FSMContext):
	await state.set_state(StateForm.company_name)
	await callback.message.delete()

	await callback.message.answer("Введите название компании 🏙️, акции которой вас интересуют по цене 👇",
	                              reply_markup=shares_return_inline)

@rout_shares.message(StateForm.company_name)
async def cmd_price_name(message: Message, state: FSMContext):
	data = await get_price_now(name=message.text)

	if 'error' in data:
		await message.answer(data['error'])
		return

	await message.answer_photo(photo=shares, caption=f'Компания под символом\n<b>{data['symbol']}</b> 📝 на данный момент торгуется \nпо цене - 💲{data['price']}',
	                     reply_markup=return_board_inline, parse_mode='HTML')
	await state.clear()

@rout_shares.callback_query(F.data == 'ticker_share')
async def cmd_symbol_shares(callback: CallbackQuery, state: FSMContext):
	await state.set_state(StateForm.company_symbol)
	await callback.message.delete()

	await callback.message.answer("Введите символ компании 🏙️ \n(например, <b>'AAPL'</b> вместо <b>'Apple'</b>)",
	                              reply_markup=shares_return_inline, parse_mode='HTML')


@rout_shares.message(StateForm.company_symbol)
async def cmd_price_symbol(message: Message, state: FSMContext):
	data = await get_price_now(request_symbol=message.text)

	if 'error' in data:
		await message.answer(data['error'])
		return

	await message.answer_photo(photo=shares,
	    caption=f'Компания под символом\n<b>{data['symbol'].upper()}</b> 📝 на данный момент торгуется \nпо цене - 💲{data['price']}',
		reply_markup=return_board_inline, parse_mode='HTML')
	await state.clear()