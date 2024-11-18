import uuid
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Transaction, TransactionStatus
from app.repositories.country import country_repository
from app.repositories.transactions import transaction_repository
from app.schemas.transaction import Transfer


class TransactionController:

	@classmethod
	async def transfer(cls,
					   session: AsyncSession,
					   data: Transfer,
					   sender_id: uuid.UUID) -> Transaction:
		return await transaction_repository.create(
			session=session,
			transfer=data,
			sender_id=sender_id
		)

	@classmethod
	async def get_transfer(cls, session: AsyncSession, transfer_id: uuid.UUID) -> Transaction:
		transfer = await transaction_repository.get_or_404(session, transfer_id)
		return transfer


	@classmethod
	async def get_transfer_by_user(cls, session: AsyncSession, sender_id: uuid.UUID) -> List[Transaction]:
		transactions = await transaction_repository.get_by_user(session=session, sender_id=sender_id)
		return transactions

	@classmethod
	async def update_transfer_status(cls, session: AsyncSession, transaction_id: uuid.UUID, status: TransactionStatus) -> Transaction:
		transaction = await transaction_repository.update_transaction_status(session=session, transaction_id=transaction_id, new_status=status)
		return transaction

	@classmethod
	async def get_all_transfers(cls, session: AsyncSession):
		transactions = await transaction_repository.all(session=session)
		return transactions

	@classmethod
	async def get_transactions_by_status(cls, session: AsyncSession, status: TransactionStatus) -> List[Transaction]:
		transactions = await transaction_repository.get_transaction_by_status(session, status)
		return transactions


transaction_controller = TransactionController()