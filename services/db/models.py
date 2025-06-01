from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger

class Base(DeclarativeBase):
	pass

class UserLang(Base):
	__tablename__ = 'user_lang'
	id_user: Mapped[int] = mapped_column(BigInteger, primary_key=True)
	lang: Mapped[str]