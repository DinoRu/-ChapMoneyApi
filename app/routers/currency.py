from fastapi import APIRouter, Depends, status, Security
from fastapi.security import  HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.currency import currency_controller
from app.database import get_session
from app.routers.users import security
from app.schemas.currencies import CurrencyResponse
from app.schemas.currencies import CreateCurrency, CurrencyResponse
from app.utils.messages import messages

router = APIRouter(
	prefix="/currency",
	tags=["Currencies"],
	responses={404: {"description": "Not found"}}
)

# security = HTTPBearer()

@router.get("/", summary="Get all currencies available", status_code=status.HTTP_200_OK)
async def get_currencies(
		session: AsyncSession = Depends(get_session)
):
	currencies = await currency_controller.get_all_currencies(session=session)
	return [CurrencyResponse.from_orm(currency) for currency in currencies]


@router.post("/create", status_code=status.HTTP_201_CREATED, summary="Create currency")
async def create_currency(
		currency_schema: CreateCurrency,
		session: AsyncSession = Depends(get_session),
		credentials: HTTPAuthorizationCredentials = Security(security)
):
	await currency_controller.create(session=session, currency_schema=currency_schema)
	return {"details": messages.CURRENCY_CREATED}

@router.get("/currency/{currency_name}", status_code=status.HTTP_200_OK, summary="Get currency by name")
async def get_currency(
		currency_name: str,
		session: AsyncSession = Depends(get_session),
		# credentials: HTTPAuthorizationCredentials = Security(security)
):
	return await currency_controller.get_by_name(session=session, name=currency_name)

@router.delete('/currency/{currency_name}/delete', status_code=status.HTTP_200_OK,
			   summary="Delete currency")
async def delete(currency_name: str, session: AsyncSession = Depends(get_session)):
	await currency_controller.delete(session=session, name=currency_name)
	return {"detail": messages.CURRENCY_DELETED}