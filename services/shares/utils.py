import pandas as pd
import yfinance as yf
from google import genai
from curl_cffi.requests.exceptions import HTTPError
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from locales.lang_search import get_string

df = pd.read_csv("nasdaq_data_tickers.csv") # data with tickers from NASDAQ
client = genai.Client(api_key=os.getenv('GEMINI_KEY'))

async def connect_to_api(symbol: str, language: str) -> dict:
	try:
		def get_price():
			return yf.Ticker(symbol).info['regularMarketPrice']
		price = await asyncio.to_thread(get_price)
		return {'price': price}

	except KeyError:
		text_for_response = get_string(language, 'keyError_api_share')
		return {'error': f"{text_for_response}"}
	except HTTPError as e:
		status = e.response.status_code
		if status == 404:
			text_for_response = get_string(language, 'HTTPError_api_share_404')
			return {'error': f"{text_for_response}"}
		else:
			text_for_response = get_string(language, 'HTTPError_api_share')
			return {'error': f"{text_for_response}"}
	except ValueError:
		text_for_response = get_string(language, 'valueError_api_share')
		return {'error': f"{text_for_response}"}


async def get_price_now(language: str, name: str | None = None, request_symbol: str | None = None) -> dict:
	symbol = request_symbol
	if name:
		response_ai = await client.aio.models.generate_content(model="gemini-2.0-flash",
                            contents=f"Тикер компании '{name}'? Ответ должен быть: один тикер или 'NotFound'")
		if response_ai.text == 'NotFound':
			text_for_response = get_string(language, 'ai_NotFound')
			return {'error': f"{text_for_response}"}
		symbol = response_ai.text

	data_from_api = await connect_to_api(symbol, language)
	if 'error' in data_from_api:
		return data_from_api

	return {'symbol': symbol, 'price': data_from_api['price']}