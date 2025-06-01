from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile

from inline_board import languages_all_inline, get_start_board_inline
from services.db.query import update_lang, get_lang
from locales.lang_search import get_string


rout_lang = Router()
earth = FSInputFile('images/earth.jfif')
logo = FSInputFile('images/logo.png')

async def main_menu(callback: CallbackQuery):
	user_id = callback.from_user.id
	await callback.message.delete()

	lang = await get_lang(user_id)
	text_for_response = get_string(lang, 'command_start')
	await callback.message.answer_photo(photo=logo, caption=f"{text_for_response}", reply_markup=get_start_board_inline(lang), parse_mode='HTML')

@rout_lang.callback_query(F.data == 'all_lang')
async def all_languages(callback: CallbackQuery):
	await callback.message.delete()

	lang = await get_lang(callback.from_user.id)
	text_for_response = get_string(lang, 'all_languages')
	await callback.message.answer_photo(photo=earth, caption=f'{text_for_response}', reply_markup=languages_all_inline)

@rout_lang.callback_query(F.data.startswith('lang'))
async def change_languages(callback: CallbackQuery):
	lang_code = callback.data.split('_')[1]
	user_id = callback.from_user.id

	result = await update_lang(user_id, lang_code)
	await main_menu(callback)

