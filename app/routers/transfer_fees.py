from collections.abc import Iterable

from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.transfer_fees import transfer_fees_controller
from app.database import get_session
from app.schemas.transfer_fees import TransferFeesCreate, TransferFeesOut, UpdateTransferFees, \
	FeesSchema

router = APIRouter(
	prefix="/transfer-fees",
	tags=['Transfer fees'],
	responses={404: {'description': "not found"}}
)

@router.post('/create/fees/{from_country}/to/{to_country}', status_code=status.HTTP_201_CREATED,
			 summary="Create fees")
async def create(
		from_country: str,
		to_country: str,
		fees_schema: FeesSchema,
		session: AsyncSession = Depends(get_session)
):
	return await transfer_fees_controller.create(
		session=session,
		from_country=from_country,
		to_country=to_country,
		fees=fees_schema.fees
	)


@router.put('/update/fees/{from_country}/to/{to_country}',
			  status_code=status.HTTP_200_OK,
			# response_model=TransferFeesOut,
			summary='Update fees')
async def update_fees(
		from_country: str,
		to_country: str,
		update_schema: UpdateTransferFees,
		session: AsyncSession = Depends(get_session),
):
	transfer_fee = await transfer_fees_controller.update_transfer_fee(
		session=session,
		from_country=from_country,
		to_country=to_country,
		fee=update_schema.fees
	)
	if not transfer_fee:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transfer fee not found")
	return {
		"from_country": transfer_fee.sender_country.name,
		"to_country": transfer_fee.receiver_country.name,
		"fees": transfer_fee.fee_percentage
	}


@router.get('/', status_code=status.HTTP_200_OK, summary="Get all frees")
async def get_all_fees(session: AsyncSession = Depends(get_session)):
	return await transfer_fees_controller.all(session)


@router.delete('/delete/fees/{from_country}/to/{to_country}',
			   status_code=status.HTTP_204_NO_CONTENT,
			   summary="Delete fees"
			   )
async def delete_fee(
		from_country: str,
		to_country: str,
		session: AsyncSession = Depends(get_session)):
	deleted = await transfer_fees_controller.delete(session=session, from_country=from_country, to_country=to_country)
	if not deleted:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Transfer fee not found."
		)
	return {"detail": "Transfer fee deleted successfully."}
