import uuid

from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.controllers.countries import country_controller
from app.database import get_session
from app.models.transaction import Country
from app.schemas.countries import CreateCountry, CountryResponse, UpdateCountryName
from app.utils.messages import messages

router = APIRouter(prefix='/countries', tags=["Countries"], responses={404: {"description":
                                                                                  "Not found"}})

@router.post('/create', status_code=status.HTTP_200_OK, summary="Get all countries")
async def create(
        country_schema: CreateCountry,
        session: AsyncSession = Depends(get_session)
):
    await country_controller.create(session=session, country_schema=country_schema)
    return {'detail': messages.COUNTRY_CREATED}


@router.get("/", status_code=status.HTTP_200_OK, summary="Get all countries",
            response_model=list[CountryResponse])
async def get_countries(session: AsyncSession = Depends(get_session)):
    countries = await country_controller.all(session=session)
    return countries

@router.get("/list_countries", response_model=list[CountryResponse])
async def list_countries(db: AsyncSession = Depends(get_session)):
    result = await db.execute(select(Country)
                              .options(selectinload(Country.currency),
                                       selectinload(Country.receiving_methods),
                                       selectinload(Country.sending_methods)))
    countries = result.scalars().all()
    return countries

@router.get("/country/{country_name}", status_code=status.HTTP_200_OK,
            response_model=CountryResponse,
            summary="Get single country with currency and methods.")
async def get_country_with_currency_and_methods(
        country_name: str,
        session: AsyncSession = Depends(get_session)
):
    country = await country_controller.get_country_with_currency_and_methods(
        session=session, country_name=country_name
    )
    return country

@router.get("/{country_guid}", status_code=status.HTTP_200_OK, summary="Get country by country id")
async def get_by_id(
        country_guid: str,
        session: AsyncSession = Depends(get_session)):
    return await country_controller.get_or_404(session=session, country_guid=country_guid)



@router.put("/country/{country_guid}", status_code=status.HTTP_200_OK, summary="Update country")
async def update_country(country_guid: str,
                         update_schema: UpdateCountryName,
                         session: AsyncSession = Depends(get_session)):
    await country_controller.update(session=session, update_schema=update_schema,
                                    country_guid=country_guid)
    return {"detail": messages.COUNTRY_UPDATED}

@router.delete('/{country_guid}/delete', status_code=status.HTTP_200_OK, summary="Delete countries")
async def delete(
        country_guid: str,
        session: AsyncSession = Depends(get_session)
):
    await country_controller.delete(session=session, country_guid=country_guid)
    return {'detail': messages.COUNTRY_DELETED}