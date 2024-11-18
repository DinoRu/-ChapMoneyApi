import uuid
from typing import Union, Iterable

from fastapi import HTTPException, status
from sqlalchemy import update

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import Account
from app.repositories.accounts import account_repository
from app.schemas.accounts import CreateAccount, AccountBase as AccountSchema
from app.utils.messages import messages


class AccountController:

	@classmethod
	async def add_account(
			cls,
			session: AsyncSession,
			account_name: str,
			account_number: str,
			account_type: str
	):
		return await account_repository.create_new_account(
			session=session,
			account_type=account_type,
			account_name=account_name,
			account_number=account_number
		)

	@classmethod
	async def modify_account(
			cls,
			session: AsyncSession,
			account_id: uuid.UUID,
			account_name: str = None,
			account_number: str = None,
			account_type: str = None
	):
		success = await account_repository.update_account(
			session=session,
			account_guid=account_id,
			account_name=account_name,
			account_number=account_number,
			account_type=account_type
		)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Account not found."
			)
		return {"detail": "Account updated successfully."}

	@classmethod
	async def modify_account_name(
			cls,
			session: AsyncSession,
			account_id: uuid.UUID,
			new_name: str
	):
		success = await account_repository.update_account_name(
			session=session,
			account_id=account_id,
			new_name=new_name
		)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Account not found"
			)
		return  {"detail": "Account name updated successfully"}

	@classmethod
	async def modify_account_number(
			cls,
			session: AsyncSession,
			account_id: uuid.UUID,
			new_number: str
	):
		success = await account_repository.update_account_number(
			session=session,
			account_id=account_id,
			new_name=new_number
		)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Account not found"
			)
		return {"detail": "Account number updated successfully"}

	@classmethod
	async def remove_account(cls, session: AsyncSession, account_id: uuid.UUID):
		success = await account_repository.delete_account(session=session, account_id=account_id)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Account not found."
			)
		return {"detail": "Account deleted successfully"}

	@classmethod
	async def remove_accounts(cls, session: AsyncSession):
		success = await account_repository.delete_accounts(session=session)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Can't not performed this."
			)
		return {"detail": "Accounts deleted successfully"}

	@classmethod
	async def get_accounts(cls,session: AsyncSession):
		return await account_repository.list_accounts(session=session)

	@classmethod
	async def get_account(cls, session: AsyncSession, account_id: uuid.UUID):
		account = await account_repository.get_account_by_id(session=session, account_id=account_id)
		if not account:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Account not found."
			)
		return {
			"guid": account.guid,
			"account_name": account.account_name,
			"account_number": account.account_number,
			"account_type": account.account_type
		}

account_controller = AccountController()