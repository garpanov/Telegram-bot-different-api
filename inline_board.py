from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

start_board_inline = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='🌡️ Температура', callback_data='temperature')],
	[InlineKeyboardButton(text='📈 Акции', callback_data='shares')]])

return_board_inline = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='🏠 Главное меню', callback_data='return_menu')]])

shares_method_inline = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='📝 По имени', callback_data='name_share')],
	[InlineKeyboardButton(text='🌟 По тикеру', callback_data='ticker_share')]])

shares_return_inline = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='‹ Назад', callback_data='shares')]])