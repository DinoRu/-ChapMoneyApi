import uuid
from sqlite3 import IntegrityError
from typing import List, Sequence

from fastapi import HTTPException, status
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.transaction import ExchangeRates, Currency
from app.repositories.base import BaseRepository


class ExchangeRateRepository(BaseRepository):
	def __init__(self):
		super().__init__(model=ExchangeRates)

	@classmethod
	async def get_currency_by_name(cls, session: AsyncSession, currency_name: str):
		query = select(Currency).where(Currency.name == currency_name)
		result = await session.execute(query)
		return result.scalar_one_or_none()

	async def create_exchange_rate(self, session: AsyncSession, from_currency: str, to_currency:
	str, rate: float) -> ExchangeRates | None:
		from_currency_obj = await self.get_currency_by_name(session=session, currency_name=from_currency)
		to_currency_obj = await self.get_currency_by_name(session=session, currency_name=to_currency)

		if not from_currency_obj or not to_currency_obj:
			return None
		new_exchange_rate = ExchangeRates(
			from_currency_id=from_currency_obj.guid,
			to_currency_id=to_currency_obj.guid,
			rates=rate
		)
		try:
			session.add(new_exchange_rate)
			await session.commit()
			await session.refresh(new_exchange_rate)
			return new_exchange_rate
		except IntegrityError:
			await session.rollback()
			return None

	@classmethod
	async def get_exchange_rate(cls, from_currency: str, to_currency: str,
												 session: AsyncSession):
		stmt_from = select(Currency).where(Currency.name == from_currency)
		stmt_to = select(Currency).where(Currency.name == to_currency)

		result_from = await session.execute(stmt_from)
		result_to = await session.execute(stmt_to)

		from_currency = result_from.scalar_one_or_none()
		to_currency = result_to.scalar_one_or_none()

		if not from_currency or not to_currency:
			return None
		query = select(ExchangeRates).where(
			ExchangeRates.from_currency_id == from_currency.guid,
			ExchangeRates.to_currency_id == to_currency.guid
		)
		result = await session.execute(query)
		return result.scalars().first()

	@classmethod
	async def get_all_exchange_rates(cls, session: AsyncSession) -> Sequence[ExchangeRates]:
		query = select(ExchangeRates).options(
			joinedload(ExchangeRates.from_currency),
			joinedload(ExchangeRates.to_currency)
		)
		results = await session.execute(query)
		return results.scalars().all()

	@classmethod
	async def update_exchange_rate(cls, session: AsyncSession, from_currency: str, to_currency:
	str, new_rate: float) -> bool | None:
		from_currency_obj = await cls.get_currency_by_name(session=session, currency_name=from_currency)
		to_currency_obj = await cls.get_currency_by_name(session=session, currency_name=to_currency)

		if not from_currency_obj or not to_currency_obj:
			return None
		query = (
			update(ExchangeRates).where(
				ExchangeRates.from_currency_id == from_currency_obj.guid,
				ExchangeRates.to_currency_id == to_currency_obj.guid
			).values(rates=new_rate)
			.execution_options(synchronize_session='fetch')
		)
		result = await session.execute(query)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def update_rate(cls, session: AsyncSession, exchange_rate: ExchangeRates, new_rate: float):
		exchange_rate.rates = new_rate
		session.add(exchange_rate)
		await session.commit()
		await session.refresh(exchange_rate)
		return exchange_rate

	async def delete_exchange_rate(self, session: AsyncSession, from_currency: str, to_currency:
	str) -> bool | None:
		from_currency_obj = await self.get_currency_by_name(session=session,
														   currency_name=from_currency)
		to_currency_obj = await self.get_currency_by_name(session=session,
														  currency_name=to_currency)

		if not from_currency_obj or not to_currency_obj:
			return None
		query = (
			delete(ExchangeRates).where(
				ExchangeRates.from_currency_id == from_currency_obj.guid,
				ExchangeRates.to_currency_id == to_currency_obj.guid
			)
			.execution_options(synchronize_session='fetch')
		)
		result = await session.execute(query)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def delete_all(cls, session: AsyncSession) -> bool:
		stmt = delete(ExchangeRates)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

exchange_rate_repository = ExchangeRateRepository()