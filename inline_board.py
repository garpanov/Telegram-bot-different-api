from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from locales.lang_search import get_string

languages_all_inline = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='🇺🇦 Українська', callback_data='lang_uk')],
	[InlineKeyboardButton(text='🇷🇺 Русский', callback_data='lang_ru')],
	[InlineKeyboardButton(text='🇬🇧 English', callback_data='lang_en')],
	[InlineKeyboardButton(text='‹ Назад', callback_data='return_menu')]])

def get_start_board_inline(lang: str):
	string_data = get_string(lang, 'start_board_inline')

	start_board_inline = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text=string_data["temperature"], callback_data='temperature')],
		[InlineKeyboardButton(text=string_data["shares"], callback_data='shares')],
		[InlineKeyboardButton(text=string_data["lang"], callback_data='all_lang')]])

	return start_board_inline

def get_variants_temp_inline(lang: str):
	string_data = get_string(lang, 'variants_temp_inline')

	variants_temp_inline = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text=string_data['geolocation'], request_location=True)],
		[InlineKeyboardButton(text=string_data['name'], callback_data='temperature')],
		[InlineKeyboardButton(text=string_data["return"], callback_data='return_menu')]])
	return variants_temp_inline

def get_return_board_inline(lang: str):
	return_board_inline = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text=get_string(lang, "return"), callback_data='return_menu')]])
	return return_board_inline

def get_return_board_2_inline(lang: str):
	return_board_2_inline = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text=get_string(lang, "return"), callback_data='return_menu')]])
	return return_board_2_inline

def get_shares_method_inline(lang: str):
	string_data = get_string(lang, "shares_method_inline")

	shares_method_inline = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text=string_data["name"], callback_data='name_share')],
		[InlineKeyboardButton(text=string_data["ticker"], callback_data='ticker_share')],
		[InlineKeyboardButton(text=string_data["return"], callback_data='return_menu')]])

	return shares_method_inline

def get_shares_return_inline(lang: str):
	shares_return_inline = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text=get_string(lang, "return"), callback_data='shares')]])
	return shares_return_inline