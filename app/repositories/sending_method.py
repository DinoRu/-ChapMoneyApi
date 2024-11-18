import uuid

from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import SendingMethod as SendingMethodModel, Country, Account
from app.repositories.base import BaseRepository


class SendingMethodRepository(BaseRepository):
	def __init__(self):
		super().__init__(model=SendingMethodModel)

	@classmethod
	async def get_country_by_name(cls, session: AsyncSession, country_name: str) -> Country:
		query = select(Country).where(Country.name == country_name)
		result = await session.execute(query)
		return result.scalar_one_or_none()

	@classmethod
	async def get_account_by_type(cls, session: AsyncSession, account_type: str) -> Account:
		query = select(Account).where(Account.account_type == account_type)
		result = await session.execute(query)
		return result.scalar_one_or_none()


	async def create_sending_method(self,
									session: AsyncSession,
									name: str,
									country_name: str,
									number: str,
									owner_name: str
									) -> SendingMethodModel | None:
		country = await self.get_country_by_name(session=session, country_name=country_name)
		if not country:
			return None
		new_sending_method = SendingMethodModel(
			name=name,
			country_guid=country.guid,
			number=number,
			owner_name=owner_name
		)
		try:
			session.add(new_sending_method)
			await session.commit()
			await session.refresh(new_sending_method)
			return new_sending_method
		except IntegrityError:
			await session.rollback()
			return None

	@classmethod
	async def update_method(cls,
							session: AsyncSession,
							method_id: uuid.UUID,
							name: str,
							number: str,
							owner_name: str
							) -> bool:
		stmt = (
			update(SendingMethodModel)
			.where(SendingMethodModel.guid == method_id)
			.values(name=name, number=number, owner_name=owner_name)
			.execution_options(synchronize_session='fetch')
		)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0


	@classmethod
	async def update_number_method(
			cls,
			method_id: uuid.UUID,
			number: str,
			session: AsyncSession
	) -> bool:
		stmt = (
			update(SendingMethodModel)
			.where(SendingMethodModel.guid == method_id)
			.values(number=number)
			.execution_options(synchronize_session='fetch')
		)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def delete_method(cls, session: AsyncSession,method_id: uuid.UUID) -> bool:
		stmt = (
			delete(SendingMethodModel)
			.where(SendingMethodModel.guid == method_id)
			.execution_options(synchronize_session='fetch')
		)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def list_sending_methods(cls, session: AsyncSession, country_name: str):
		country = await cls.get_country_by_name(session, country_name)
		if not country:
			return None
		stmt = select(SendingMethodModel).where(
			SendingMethodModel.country_guid == country.guid
		)
		result = await session.execute(stmt)
		return result.scalars().all()




send_payment_repository = SendingMethodRepository()