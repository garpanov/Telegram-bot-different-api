from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.middleware import FSMContext, BaseMiddleware
from datetime import datetime
import gspread
import asyncio
import os

from services.shares.router_shares import rout_shares
from services.temperature.router_temp import rout_temp
from inline_board import start_board_inline
from dotenv import load_dotenv
load_dotenv()

class SheetsLogger(BaseMiddleware):
    def __init__(self, sheet):
        self.sheet = sheet

    async def __call__(self, handler, event, data):
        try:
            user_id = getattr(event.from_user, "id", "N/A")
            username = getattr(event.from_user, "username", "N/A")
            content = ""

            if isinstance(event, Message):
                content = event.text or "N/A"
            elif isinstance(event, CallbackQuery):
                content = event.data or "N/A"
            else:
                return await handler(event, data) # Ignore all other

            self.sheet.append_row([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                str(user_id),
                username,
                content
            ])
        except Exception as e:
            print(f"[LOG ERROR]: {e}")

        return await handler(event, data)

gc = gspread.service_account(filename='creds.json')
wks = gc.open("task-test-logins").sheet1

token = os.getenv('TOKEN_TG')
bot = Bot(token=token)
dp = Dispatcher()
dp.include_routers(rout_temp, rout_shares)
dp.message.middleware(SheetsLogger(wks))
dp.callback_query.middleware(SheetsLogger(wks))
logo = FSInputFile('./images/logo.png')

@dp.message(CommandStart())
async def command_start(message: Message, state: FSMContext):
	await state.clear() # We reset the state if the user hasn't completed it.
	await message.answer_photo(photo=logo, caption='<b>Привет!</b> 👋\nЧем могу помочь? 😊', reply_markup=start_board_inline, parse_mode='HTML')

@dp.callback_query(F.data == 'return_menu')
async def start_menu(callback: CallbackQuery, state: FSMContext):
	await state.clear() # We reset the state if the user hasn't completed it.
	await callback.message.delete()
	await callback.message.answer_photo(photo=logo, caption='<b>Привет!</b> 👋\nЧем могу помочь? 😊', reply_markup=start_board_inline, parse_mode='HTML')

async def main():
	await bot.delete_webhook(drop_pending_updates=True) # Delete messages that were received while the bot was offline.
	await dp.start_polling(bot)

if __name__ == '__main__':
	asyncio.run(main())
