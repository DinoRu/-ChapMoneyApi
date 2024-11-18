from typing import List, Dict

from fastapi import HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.country import country_repository
from app.repositories.transfert_fees import transfer_fees_repository
from app.schemas.transfer_fees import TransferFeesCreate, UpdateTransferFees


class TransferFeeController:

	@classmethod
	async def create(cls, session: AsyncSession, from_country: str, to_country: str, fees: float):
		new_fees = await transfer_fees_repository.create_fees(
			session=session,
			from_country=from_country,
			to_country=to_country,
			fees=fees
		)
		if not new_fees:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Fees not created."
			)
		return {
			"from_country": from_country,
			"to_country": to_country,
			"fees": fees
		}

	@classmethod
	async def all(cls, session: AsyncSession) -> List[Dict[str, str]]:
		fees = await transfer_fees_repository.get_all_fees(session)
		if not fees:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Fees not found."
			)
		return [
			{
				"from_country": fee.sender_country.name,
				"to_country": fee.receiver_country.name,
				"fees": fee.fee_percentage
			} for fee in fees
		]

	@classmethod
	async def get_or_404(cls, session: AsyncSession, fees_id: str):
		pass

	@classmethod
	async def update_transfer_fee(cls,
								  session: AsyncSession, from_country: str,
								  to_country: str, fee: float):
		sender_country_id = await country_repository.get_country_by_name(session=session, country_name=from_country)
		receiver_country_id = await country_repository.get_country_by_name(session=session, country_name=to_country)

		if sender_country_id and receiver_country_id:
			transfer_fee = await transfer_fees_repository.get_fees(
				session=session,
				sender_country_id=sender_country_id,
				receiver_country_id=receiver_country_id
			)
			if transfer_fee:
				return await transfer_fees_repository.update_fees(session, transfer_fee, fee)
		return None

	@classmethod
	async def delete(cls, session: AsyncSession, from_country: str, to_country: str):
		sender_country_id = await country_repository.get_country_by_name(session, from_country)
		receiver_country_id = await country_repository.get_country_by_name(session, to_country)

		if sender_country_id and receiver_country_id:
			transfer_fee = await transfer_fees_repository.get_fees(session=session, sender_country_id=sender_country_id, receiver_country_id=receiver_country_id)
			if transfer_fee:
				await transfer_fees_repository.delete_fees(session=session, transfer_fee=transfer_fee)
				return True
		return False

	@classmethod
	async def delete_all(cls, session: AsyncSession):
		pass


transfer_fees_controller = TransferFeeController()