from certifi import where
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.transaction import Country as CountryModel, Currency
from app.repositories.base import BaseRepository


class CountryRepository(BaseRepository):
	def __init__(self):
		super().__init__(model=CountryModel)


	@classmethod
	async def get_country_by_name(cls, session:AsyncSession, country_name: str):
		stmt = select(CountryModel).where(CountryModel.name == country_name)
		result = await session.execute(stmt)
		country = result.scalar_one_or_none()
		return country.guid if country else None

	async def all(self, session: AsyncSession):
		query = select(CountryModel).options(
			selectinload(CountryModel.currency),
			selectinload(CountryModel.receiving_methods),
			selectinload(CountryModel.sending_methods)
		)
		result = await session.execute(query)
		return result.scalars().all()

	@classmethod
	async def get_country_with_currency_and_methods(cls, session: AsyncSession, country_name: str) -> CountryModel:
		stmt = select(CountryModel).where(
			CountryModel.name == country_name
		).options(
			selectinload(CountryModel.currency),
			selectinload(CountryModel.sending_methods),
			selectinload(CountryModel.receiving_methods)
		)
		result = await session.execute(stmt)
		return result.scalars().first()




country_repository = CountryRepository()