from typing import Iterable

from fastapi import APIRouter, status, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.accounts import account_controller
from app.database import get_session
from app.repositories.accounts import account_repository
from app.schemas.accounts import (CreateAccount, UpdateAccountRequest,
								  UpdateAccountNameRequest, UpdateAccountNumberRequest)
from app.utils.messages import messages

router = APIRouter(prefix="/admin-accounts", tags=["Admin accounts"], responses={404: {
	'description': "Not Found"}})


@router.post('/new/accounts', status_code=status.HTTP_201_CREATED, summary="Create new account")
async def new_account(
		request: CreateAccount,
		session: AsyncSession = Depends(get_session)
):
	return await account_controller.add_account(
		session=session,
		account_name=request.account_name,
		account_number=request.account_number,
		account_type=request.account_type
	)


@router.get('/', status_code=status.HTTP_200_OK, summary="All Admin Accounts")
async def all_accounts(session: AsyncSession = Depends(get_session)):
	return await account_controller.get_accounts(session=session)


@router.put("/update/{account_guid}", status_code=status.HTTP_200_OK, summary="Update account")
async def update_account(
		account_guid: str,
		request: UpdateAccountRequest,
		session: AsyncSession = Depends(get_session)):
	return await account_controller.modify_account(
		session=session,
		account_name=request.account_name,
		account_number=request.account_number,
		account_type=request.account_type,
		account_id=account_guid
	)

@router.patch("/update/name/{account_id}",
			  status_code=status.HTTP_200_OK, summary="Update account name")
async def update_account_name(
		account_id: str,
		request: UpdateAccountNameRequest,
		session: AsyncSession = Depends(get_session)
):
	return await account_controller.modify_account_name(
		session=session,
		account_id=account_id,
		new_name=request.account_name
	)

@router.patch("/update/number/{account_id}",
			  status_code=status.HTTP_200_OK,
			  summary="Update account number",
			  )
async def update_account_number(
		account_id: str,
		request: UpdateAccountNumberRequest,
		session: AsyncSession = Depends(get_session)
):
	return await account_controller.modify_account_number(
		session=session,
		account_id=account_id,
		new_number=request.account_number
	)

@router.delete("/delete/account/{account_id}", status_code=status.HTTP_200_OK, summary="Delete "
																					   "account")
async def delete_account(
		account_id: str,
		session: AsyncSession = Depends(get_session)
):
	return await account_controller.remove_account(
		session, account_id
	)


@router.delete("/delete/accounts", status_code=status.HTTP_200_OK, summary="Delete all accounts")
async def delete_all_accounts(
		session: AsyncSession = Depends(get_session)
):
	return await account_controller.remove_accounts(session=session)