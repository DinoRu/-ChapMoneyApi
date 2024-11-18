import uuid
from typing import Union

from fastapi import HTTPException, status
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Account
from app.repositories.base import BaseRepository
from app.utils.messages import messages


class AccountRepository(BaseRepository):
	def __init__(self):
		super().__init__(model=Account)

	@classmethod
	async def create_new_account(cls,
								 session: AsyncSession,
								 account_name: str,
								 account_number: str,
								 account_type: str
								 ) -> Account:
		new_account = Account(
			account_name=account_name,
			account_number=account_number,
			account_type=account_type
		)
		session.add(new_account)
		await session.commit()
		await session.refresh(new_account)
		return new_account

	@classmethod
	async def update_account(cls,
							 session: AsyncSession,
							 account_guid: uuid.UUID,
							 account_name: str = None,
							 account_number: str = None,
							 account_type: str = None) -> bool:
		stmt = (
			update(Account)
			.where(Account.guid == account_guid)
			.values(
				account_name=account_name,
				account_number=account_number,
				account_type=account_type
			)
			.execution_options(synchronize_session='fetch')
		)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def update_account_name(cls,
						  account_id: uuid.UUID,
						  new_name: str,
						  session: AsyncSession) -> bool:
		stmt = (
			update(Account)
			.where(Account.guid == account_id)
			.values(
				account_name=new_name
			)
			.execution_options(synchronize_session='fetch')
		)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def update_account_number(
			cls,
			account_id: str,
			new_number: str,
			session: AsyncSession) -> bool:
		stmt = (
			update(Account)
			.where(Account.guid == account_id)
			.values(account_number=new_number)
			.execution_options(synchronize_session='fetch')
		)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def delete_account(cls, account_id: uuid.UUID, session: AsyncSession) -> bool:
		stmt = (
			delete(Account)
			.where(Account.guid == account_id)
		)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

	@classmethod
	async def list_accounts(cls, session: AsyncSession):
		stmt = select(Account)
		result = await session.execute(stmt)
		return result.scalars().all()

	@classmethod
	async def get_account_by_id(cls, account_id: uuid.UUID, session: AsyncSession) -> Account:
		stmt = select(Account).where(Account.guid == account_id)
		result = await session.execute(stmt)
		return result.scalar_one_or_none()

	@classmethod
	async def delete_accounts(cls, session: AsyncSession) -> bool:
		stmt = delete(Account)
		result = await session.execute(stmt)
		await session.commit()
		return result.rowcount > 0

account_repository = AccountRepository()