import uuid
from typing import Sequence

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.models.transaction import TransferFee, Country
from app.repositories.base import BaseRepository


class TransferFeesRepository(BaseRepository):
	def __init__(self):
		super().__init__(model=TransferFee)

	@classmethod
	async def get_country(cls, session: AsyncSession, country_name: str) -> Country:
		stmt = select(Country).where(Country.name == country_name)
		result = await session.execute(stmt)
		return result.scalar_one_or_none()


	@classmethod
	async def create_fees(cls,
						  session: AsyncSession,
						  from_country: str,
						  to_country: str,
						  fees: float) -> TransferFee:
		from_country_obj = await cls.get_country(session=session, country_name=from_country)
		to_country_obj = await cls.get_country(session=session, country_name=to_country)

		if not from_country_obj or not to_country_obj:
			raise ValueError(
				f"Country not found."
			)
		new_fees = TransferFee(
			sender_country_id=from_country_obj.guid,
			receiver_country_id=to_country_obj.guid,
			fee_percentage=fees
		)
		session.add(new_fees)
		await session.commit()
		return new_fees

	@classmethod
	async def get_fees(cls, session: AsyncSession,
					   sender_country_id: uuid.UUID,
					   receiver_country_id: uuid.UUID) -> TransferFee:
		stmt = (select(TransferFee)
			.options(
				selectinload(TransferFee.sender_country),
				selectinload(TransferFee.receiver_country)
		    )
			.where(
			TransferFee.sender_country_id == sender_country_id,
			TransferFee.receiver_country_id == receiver_country_id
		))
		result = await session.execute(stmt)
		return result.scalar_one_or_none()

	@classmethod
	async def get_all_fees(cls, session: AsyncSession) -> Sequence[TransferFee]:
		stmt = select(TransferFee).options(
			joinedload(TransferFee.sender_country),
			joinedload(TransferFee.receiver_country)
		)
		result = await session.execute(stmt)
		return result.scalars().all()

	@classmethod
	async def update_fees(cls, session: AsyncSession,
						  transfer_fee: TransferFee,
						  fee_percentage: float) -> TransferFee:
		transfer_fee.fee_percentage = fee_percentage
		session.add(transfer_fee)
		await session.commit()
		await session.refresh(transfer_fee)
		return transfer_fee


	@classmethod
	async def delete_fees(cls, session: AsyncSession, transfer_fee: TransferFee):
		await session.delete(transfer_fee)
		await session.commit()

	@classmethod
	async def clear_fees(cls, session: AsyncSession) -> bool:
		pass


transfer_fees_repository = TransferFeesRepository()