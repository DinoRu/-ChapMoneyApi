from typing import List, Dict

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import ExchangeRates as ExchangeRatesModel
from app.repositories.exchange_rates import exchange_rate_repository
from app.schemas.exchange_rates import CreateExchangeRate, ExchangeRateBase


class ExchangeRateController:

	@classmethod
	async def create(cls, session: AsyncSession, exchange_schema: CreateExchangeRate):
		rate = ExchangeRatesModel(**exchange_schema.dict())
		return await exchange_rate_repository.create(session=session, instance=rate)

	@classmethod
	async def create_new_exchange_rate(cls, session: AsyncSession, from_currency: str,
									   to_currency: str, rate: float):
		new_exchange_rate = await exchange_rate_repository.create_exchange_rate(
			session=session,
			from_currency=from_currency,
			to_currency=to_currency,
			rate=rate
		)
		if not new_exchange_rate:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Invalid currency names or exchange rate already exists."
			)

		return {
			"from_currency": from_currency,
			"to_currency": to_currency,
			"rate": new_exchange_rate.rates
		}

	@classmethod
	async def get(cls, session: AsyncSession, guid: str):
		rate = await exchange_rate_repository.get(session=session, guid=guid)
		return rate

	@classmethod
	async def all(cls, session: AsyncSession):
		rates = await exchange_rate_repository.all(session=session)
		return rates

	@classmethod
	async def fetch_exchange_rate(cls, session:AsyncSession, from_currency: str, to_currency: str):
		exchange_rate = await exchange_rate_repository.get_exchange_rate(session=session,
																		 from_currency=from_currency,to_currency=to_currency)
		if not exchange_rate:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Exchange rate not found or one of the currencies is invalid."
			)
		return {
			"from_currency": from_currency,
			"to_currency": to_currency,
			"rates": exchange_rate.rates
		}

	@classmethod
	async def fetch_all_rates(cls, session: AsyncSession) -> List[Dict[str, str]]:
		exchange_rates = await exchange_rate_repository.get_all_exchange_rates(session=session)
		return [
			{
				"from_currency": rate.from_currency.name,
				"to_currency": rate.to_currency.name,
				"rates": rate.rates
			} for rate in exchange_rates
		]

	@classmethod
	async def update(cls, session: AsyncSession, new_rate: float,  from_currency: str,
					 to_currency: str):
		success = await exchange_rate_repository.update_exchange_rate(
			session=session,
			from_currency=from_currency,
			to_currency=to_currency,
			new_rate=new_rate
		)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Exchange rate not found or one of the currencies is invalid."
			)
		return {"detail": "Exchange rate updated successfully."}

	@classmethod
	async def modify_rate(cls, session: AsyncSession, from_currency: str, to_currency: str, new_rate: float):
		exchange_rate = await exchange_rate_repository.get_exchange_rate(
			session=session,
			from_currency=from_currency,
			to_currency=to_currency,
		)
		if not exchange_rate:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Exchange not found."
			)
		updated_rate = await exchange_rate_repository.update_rate(session, exchange_rate, new_rate=new_rate)
		if not updated_rate:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Exchange not found for updated."
			)
		return {'detail': "Exchange rate updated successfully."}

	@classmethod
	async def delete(cls, session: AsyncSession, from_currency: str, to_currency: str):
		success = await exchange_rate_repository.delete_exchange_rate(
			session=session,
			from_currency=from_currency,
			to_currency=to_currency
		)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Exchange rate not found or one of the currencies is invalid."
			)
		return {"detail": "Exchange rate deleted successfully."}

	@classmethod
	async def remove_all(cls, session: AsyncSession):
		success = await exchange_rate_repository.delete_all(session)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Exchange rate not found or one of the currencies is invalid."
			)
		return {"detail": "Exchange rates deleted successfully."}



exchange_rate_controller = ExchangeRateController()

