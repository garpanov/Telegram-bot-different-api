import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # директорія цього скрипта
file_path = BASE_DIR / 'strings.json'

def get_string(lang: str, string_name: str):
	with open(file_path, 'r', encoding='utf-8') as file:
		translations = json.load(file)
		return translations[lang][string_name]