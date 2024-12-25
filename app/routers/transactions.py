import uuid
from typing import List

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.transactions import transaction_controller
from app.database import get_session
from app.dependencies import get_current_user
from app.models.users import User
from app.schemas.transaction import TransferOut, Transfer, TransactionStatus, AdminTransferOut

router = APIRouter(prefix="/transfer", tags=['transfer'], responses={404: {'description': "Not "
																						"found"}})
@router.get('/',
			status_code=status.HTTP_200_OK,
			response_model=List[AdminTransferOut],
			summary="Tranfer summary")
async def get_transfers(
		session: AsyncSession = Depends(get_session)
):
	transactions = await transaction_controller.get_all_transfers(session=session)
	return transactions

@router.post("/",
			 status_code=status.HTTP_201_CREATED,
			 response_model=TransferOut,
			 summary="Create transfer")
async def transfer_to_user(
		transfer_schema: Transfer,
		session: AsyncSession = Depends(get_session),
		sender: User = Depends(get_current_user)
):
	sender_id = sender.guid
	if transfer_schema.amount < 100:
		raise  HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Transaction amount should greatest or equal 100 of your local currency"
		)
	transaction = await transaction_controller.transfer(
		sender_id=sender_id,
		session=session,
		data=transfer_schema
	)
	return transaction

@router.get("/me/transactions",
			status_code=status.HTTP_200_OK,
			response_model=List[TransferOut],
			summary="Get transaction by ID")
async def get_transaction(
		session: AsyncSession = Depends(get_session),
		sender: User = Depends(get_current_user)
):
	transactions  = await transaction_controller.get_transfer_by_user(session=session, sender_id=sender.guid)
	return transactions

@router.get("/{transaction_status}/",
			response_model=List[TransferOut],
			status_code=status.HTTP_200_OK, summary="Pending transfers")
async def get_transfers_by_status(
		transaction_status: TransactionStatus,
		session: AsyncSession = Depends(get_session),
):
	transactions = await transaction_controller.get_transactions_by_status(session=session, status=transaction_status)
	return transactions


@router.patch("/transaction/{transaction_id}/pending",
			  response_model=TransferOut,
			  status_code=status.HTTP_200_OK, summary="Pending transaction")
async def confirm_transfer_pending(
		transaction_id: uuid.UUID,
		session: AsyncSession = Depends(get_session)
):
	transaction = await transaction_controller.update_transfer_status(
		session=session,
		transaction_id=transaction_id,
		status=TransactionStatus.PENDING
	)
	return transaction

@router.patch("/transaction/{transaction_id}/completed",
			  response_model=TransferOut,
			  status_code=status.HTTP_200_OK,
			  summary="Make transaction completed.")
async def confirm_transfer_completed(
		transaction_id: uuid.UUID,
		session: AsyncSession = Depends(get_session)
):
	transaction = await transaction_controller.update_transfer_status(status=TransactionStatus.COMPLETED,
																	  session=session, transaction_id=transaction_id)
	return transaction
