from sqlalchemy import select
from redis.asyncio import Redis
import os
from dotenv import load_dotenv
load_dotenv()

from services.db.config import maker_async
from services.db.models import UserLang

redis = Redis(host=os.getenv('REDIS_HOST'), port=6379, decode_responses=True)

async def get_lang(id_user: int) -> str:
	cache = await redis.get(str(id_user))
	if cache:
		return cache

	async with maker_async() as session:
		data = (await session.execute(select(UserLang).where(UserLang.id_user == id_user))).scalars().first()
		if not data:
			return 'ru'

		await redis.set(str(id_user), data.lang)
		return data.lang

async def update_lang(id_user: int, lang: str) -> str:
	async with maker_async() as session:
		user = (await session.execute(select(UserLang).where(UserLang.id_user == id_user))).scalars().first()
		if user:
			user.lang = lang
		else:
			user = UserLang(id_user=id_user, lang=lang)

		session.add(user)
		await session.commit()
		await redis.set(str(id_user), lang)
		return lang
