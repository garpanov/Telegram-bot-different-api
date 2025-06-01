from google import genai
import os

from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv('GEMINI_KEY'))

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Какой тикер акций на бирже имеет компания епл? Дай только тикер",
)

print(response.text)