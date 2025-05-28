import aiohttp
import os

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('WEATHER_KEY')

async def fetch(city):
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

