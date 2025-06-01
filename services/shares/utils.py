import pandas as pd
import yfinance as yf
from google import genai
from curl_cffi.requests.exceptions import HTTPError
import asyncio
import os

from dotenv import load_dotenv
load_dotenv()

df = pd.read_csv("nasdaq_data_tickers.csv") # data with tickers from NASDAQ
client = genai.Client(api_key=os.getenv('GEMINI_KEY'))

async def connect_to_api(symbol: str) -> dict:
	try:
		def get_price():
			return yf.Ticker(symbol).info['regularMarketPrice']
		price = await asyncio.to_thread(get_price)
		return {'price': price}

	except KeyError:
		return {'error': 'Данные о цене отсутствуют. Попробуйте выбрать другую компанию.'}
	except HTTPError as e:
		status = e.response.status_code
		if status == 404:
			return {'error': 'По вашему запросу ничего не найдено. Попробуйте ещё раз:'}
		else:
			return {'error': 'Не удалось получить данные. Попробуйте снова чуть позже.'}
	except ValueError:
		return {'error': 'Недопустимые данные'}


async def get_price_now(name: str | None = None, request_symbol: str | None = None) -> dict:
	symbol = request_symbol
	if name:
		response_ai = await client.aio.models.generate_content(model="gemini-2.0-flash",
                            contents=f"Тикер компании '{name}'? Ответ должен быть: один тикер или 'NotFound'")
		print(response_ai.text)
		if response_ai.text == 'NotFound':
			return {'error': 'По вашему запросу ничего не найдено. Попробуйте ещё раз:'}
		symbol = response_ai.text

	data_from_api = await connect_to_api(symbol)
	if 'error' in data_from_api:
		return data_from_api

	return {'symbol': symbol, 'price': data_from_api['price']}

# async def get_price_now(name: str | None = None, request_symbol: str | None = None) -> dict:
# 	if not name and not request_symbol:
# 		return {'error': 'Необходимо передать хотя бы один параметр.'}
#
# 	symbol = ''
# 	if name:
# 		symbol_list = df[df['Name'] == name]['Symbol'].values
# 		if len(symbol_list) >= 1:
# 			symbol = symbol_list[0]
# 		else:
# 			return {'error': 'Не найдено компании с таким именем. '
# 			                 'Пожалуйста, проверьте правильность ввода и попробуйте снова: '}
#
# 	elif request_symbol:
# 		symbol = request_symbol
#
# 	data_from_api = await connect_to_api(symbol)
# 	if 'error' in data_from_api:
# 		return data_from_api
#
# 	return {'symbol': symbol, 'price': data_from_api['price']}