import uuid
from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy_utils import PhoneNumber

from app.models.transaction import Transaction, TransactionStatus, ExchangeRates
from app.models.users import User
from app.repositories.country import country_repository
from app.repositories.exchange_rates import exchange_rate_repository
from app.repositories.transfert_fees import transfer_fees_repository
from app.schemas.transaction import Transfer


class TransactionRepository:

	@classmethod
	async def create(cls, session: AsyncSession, transfer: Transfer, sender_id: uuid.UUID) -> Transaction:
		from_ = await country_repository.get_country_with_currency_and_methods(session=session, country_name=transfer.from_country)
		to_ = await country_repository.get_country_with_currency_and_methods(session=session, country_name=transfer.to_country)
		rate = await exchange_rate_repository.get_exchange_rate(session=session, from_currency=from_.currency.name, to_currency=to_.currency.name)
		converted_amount = transfer.amount * rate.rates
		fees = await transfer_fees_repository.get_fees(session=session, sender_country_id=from_.guid, receiver_country_id=to_.guid)
		final_amount = transfer.amount + (transfer.amount * fees.fee_percentage)
		date = datetime.now().strftime("%d.%m.%Y %H:%M")
		transaction = Transaction(
			**transfer.dict(),
			completed_at=date,
			sender_id=sender_id,
			converted_amount=converted_amount,
			final_amount=final_amount
		)
		session.add(transaction)
		await session.commit()
		return transaction

	@classmethod
	async def get_or_404(cls, session: AsyncSession, transaction_guid: uuid.UUID) -> Transaction:
		stmt = select(Transaction).where(Transaction.guid == transaction_guid)
		result = await session.execute(stmt)
		return result.scalar_one_or_none()

	@classmethod
	async def get_by_user(cls, sender_id: uuid.UUID, session: AsyncSession):
		stmt = select(Transaction).where(Transaction.sender_id == sender_id)
		result = await session.execute(stmt)
		return result.scalars().all()


	@classmethod
	async def all(cls, session: AsyncSession):
		stmt = select(Transaction).options(selectinload(Transaction.sender))
		result = await session.execute(stmt)
		return result.scalars().all()

	@classmethod
	async def update_transaction(cls, session: AsyncSession,
								 transaction: Transaction, status: TransactionStatus) -> Transaction:
		transaction.transaction_status = status.PENDING
		session.add(transaction)
		await session.commit()
		await session.refresh(transaction)

	@classmethod
	async def update_transaction_status(cls, session: AsyncSession, transaction_id: uuid.UUID, new_status: TransactionStatus) -> Transaction:
		transaction = await cls.get_or_404(session, transaction_id)
		transaction.status = new_status
		await session.commit()
		await session.refresh(transaction)
		return transaction

	@classmethod
	async def get_transaction_by_status(cls, session: AsyncSession, status: TransactionStatus):
		stmt = select(Transaction).where(Transaction.status == status)
		result = await session.execute(stmt)
		return result.scalars().all()

transaction_repository = TransactionRepository()