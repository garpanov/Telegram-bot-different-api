from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import asyncio
import os
from dotenv import load_dotenv
load_dotenv()

from services.db.models import Base


engine = create_async_engine(os.getenv('DATABASE_URL_DOCKER'), echo=True)
maker_async = async_sessionmaker(bind=engine)
async def get_session() -> AsyncSession:
	async with maker_async() as session:
		yield session

async def create_table():
	async with engine.begin() as conn:
		await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
	asyncio.run(create_table())