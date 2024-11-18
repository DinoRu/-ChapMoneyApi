from collections.abc import Iterable

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import symbol
from sqlalchemy_utils import Currency
from starlette.status import HTTP_400_BAD_REQUEST

from app.models.transaction import Currency as CurrencyModel
from app.repositories.currency import currency_repository
from app.schemas.currencies import CreateCurrency
from app.utils.messages import messages


class CurrencyController:

	@classmethod
	async def create(cls, session: AsyncSession, currency_schema: CreateCurrency):
		name = Currency(currency_schema.name)
		currency_name = name.code
		currency_symbol=name.symbol
		currency_full_name = name.name
		if await currency_repository.get(session=session, name=currency_name):
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=messages.CURRENCY_ALREADY_EXISTS
			)

		currency = CurrencyModel(
			name=currency_name,
			full_name=currency_full_name,
			symbol=currency_symbol
		)
		return await currency_repository.create(instance=currency, session=session)

	@classmethod
	async def get_by_name(cls, session: AsyncSession, name: str) -> CurrencyModel |None:
		return await currency_repository.get(session=session, name=name)

	@classmethod
	async def get_all_currencies(cls, session: AsyncSession) -> Iterable[CurrencyModel] | None:
		return await currency_repository.all(session=session)

	@classmethod
	async def delete(cls, session: AsyncSession, name: str):
		currency = await cls.get_by_name(session=session, name=name)
		if not currency:
			raise HTTPException(
				status_code=HTTP_400_BAD_REQUEST,
				detail=messages.CURRENCY_NOT_FOUND
			)
		await currency_repository.delete(instance=currency, session=session)


currency_controller = CurrencyController()