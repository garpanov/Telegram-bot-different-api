import aiohttp
from google import genai
import os

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('WEATHER_KEY')
client = genai.Client(api_key=os.getenv('GEMINI_KEY'))

async def fetch_api(city):
	params = {'key': API_KEY, 'q': city}
	async with aiohttp.ClientSession() as session:
		async with session.get('http://api.weatherapi.com/v1/current.json', params=params) as response:
			data = await response.json()

			if response.status == 200:
				temp = data['current']['temp_c']
				return {'city': data['location']['name'], 'temperature': temp}

			elif data['error']['message'] == 'No matching location found.':
				return {'error': "Not Found"}

			else:
				return {'error': 'Problems with api'}

async def fetch(city: str):
	response_ai = await client.aio.models.generate_content(model='gemini-2.0-flash',
	                                                 contents=f'Напиши город з речення «{city}» латиницей по официальным нормам и початковой форме. Только один ответ (город) или NotFound)')
	print(response_ai.text)
	if response_ai.text == 'NotFound':
		return {'error': "Not Found"}

	response_weather_api = await fetch_api(response_ai.text)
	return response_weather_api


