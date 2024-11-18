from fastapi import APIRouter, status, Body
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.exchange_rates import exchange_rate_controller
from app.database import get_session
from app.schemas.exchange_rates import ExchangeRateCreateRequest


router = APIRouter(
	prefix="/exchange_rates",
	tags=['Exchange rates'],
	responses={404: {'description': 'not found'}}
)

@router.get("/all/rates", status_code=status.HTTP_200_OK, summary='Get all exchange rates')
async def get_all_exchange_rates(session: AsyncSession = Depends(get_session)):
	return await exchange_rate_controller.fetch_all_rates(session=session)


@router.get("/{from_currency}/to/{to_currency}",
			status_code=status.HTTP_200_OK,
			summary="Get rate from currency to currency")
async def get_rate_from_currency_to_currency(
		from_currency: str,
		to_currency: str,
		session: AsyncSession = Depends(get_session)
):
	return await exchange_rate_controller.fetch_exchange_rate(
		session=session,
		from_currency=from_currency,
		to_currency=to_currency
	)

@router.post("/rate/create/{from_currency}/to/{to_currency}",
			 status_code=status.HTTP_201_CREATED,
			 summary="Create new exchange rate between two currencies")
async def create_exchange_rate(
		from_currency: str,
		to_currency: str,
		request: ExchangeRateCreateRequest,
		session: AsyncSession = Depends(get_session)
):
	return await exchange_rate_controller.create_new_exchange_rate(
		session=session,
		from_currency=from_currency,
		to_currency=to_currency,
		rate=request.rate
	)

@router.patch('/update/rate/{from_currency}/to/{to_currency}',
			  status_code=status.HTTP_200_OK,
			  summary="Update rate")
async def update_rate(
		from_currency: str,
		to_currency: str,
		new_rate: float = Body(..., embed=True),
		session: AsyncSession = Depends(get_session)):
	return await exchange_rate_controller.update(
		session=session,
		new_rate=new_rate,
		from_currency=from_currency,
		to_currency=to_currency
	)

@router.delete("/delete/{from_currency}/to/{to_currency}", status_code=status.HTTP_200_OK,
			   summary="Delete rate")
async def delete(
		from_currency: str,
		to_currency: str,
		session: AsyncSession = Depends(get_session)
):
	return await exchange_rate_controller.delete(
		session=session,
		from_currency=from_currency,
		to_currency=to_currency
	)


