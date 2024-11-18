import uuid

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import SendingMethod as SendingMethodModel, ReceivingMethod, Country
from app.repositories.base import BaseRepository


class ReceiveMethodRepository(BaseRepository):
	def __init__(self):
		super().__init__(model=SendingMethodModel)

	@classmethod
	async def get_country(cls, session: AsyncSession, name: str):
		stmt = select(Country).where(Country.name == name)
		result = await session.execute(stmt)
		return result.scalar_one_or_none()

	@classmethod
	async def create_method(cls,
							session: AsyncSession,
							country_name: str,
							name: str,
							required_card: bool = False) -> ReceivingMethod | None:
		country = await cls.get_country(session, country_name)
		if not country:
			raise None
		new_receiving_method = ReceivingMethod(
			name=name,
			country_id=country.guid,
			required_card_number=required_card
		)
		session.add(new_receiving_method)
		await session.commit()
		await session.refresh(new_receiving_method)
		return new_receiving_method

	@classmethod
	async def update_method(cls, session: AsyncSession, method_id: uuid.UUID, name: str,
							required_card) -> bool:
		stmt = (
			update(ReceivingMethod)
			.where(ReceivingMethod.guid == method_id)
			.values(name=name, required_card_number=required_card)
			.execution_options(synchronize_session='fetch')
		)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def delete_method(cls, session: AsyncSession, method_id: uuid.UUID) -> bool:
		stmt = delete(ReceivingMethod).where(ReceivingMethod.guid == method_id)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def list_methods(cls, session: AsyncSession):
		stmt = select(ReceivingMethod)
		result = await session.execute(stmt)
		return result.scalars().all()

	@classmethod
	async def get_method(cls, session: AsyncSession, method_id: uuid.UUID):
		stmt = select(ReceivingMethod).where(ReceivingMethod.guid == method_id)
		result = await session.execute(stmt)
		return result.scalar_one_or_none()


receive_payment_repository = ReceiveMethodRepository()