import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Country as CountryModel
from app.repositories.country import country_repository
from app.schemas.countries import CreateCountry, UpdateCountryName
from app.utils.messages import messages


class CountryController:

	@classmethod
	async def create(cls, session: AsyncSession, country_schema: CreateCountry):
		country_name = country_schema.name
		if await country_repository.get(session=session, name=country_name):
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=messages.COUNTRY_ALREADY_EXISTS
			)
		country = CountryModel(**country_schema.dict())
		return await country_repository.create(instance=country, session=session)

	@classmethod
	async def all(cls, session: AsyncSession):
		return await country_repository.all(session=session)

	@classmethod
	async def get_or_404(cls, session: AsyncSession, country_guid: str):
		return await country_repository.get(session=session, guid=country_guid)

	@classmethod
	async def get_by_name_or_404(cls, session: AsyncSession, country_name: str):
		return await country_repository.get(session=session, name=country_name)

	@classmethod
	async def update(cls, session: AsyncSession, update_schema: UpdateCountryName, country_guid:
	str):
		country = await cls.get_or_404(session=session, country_guid=country_guid)
		if not country:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail=messages.ACCOUNT_NOT_FOUND
			)
		for key, value in update_schema.dict(exclude_unset=True).items():
			setattr(country, key, value)
		await session.commit()
		await session.refresh(country)
		return country

	@classmethod
	async def delete(cls, country_guid: str, session: AsyncSession):
		if not (country := await cls.get_or_404(session=session, country_guid=country_guid)):
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail={'detail': messages.COUNTRY_NOT_FOUND}
			)
		await country_repository.delete(session=session, instance=country)

	@classmethod
	async def get_country_with_currency_and_methods(cls, session: AsyncSession, country_name: str):
		country = await country_repository.get_country_with_currency_and_methods(
			session=session,
			country_name=country_name
		)
		if not country:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Country not found."
			)
		return country

country_controller = CountryController()