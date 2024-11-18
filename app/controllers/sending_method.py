import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.sending_method import send_payment_repository
from app.schemas.sending_method import CreateSendingMethod, UpdateSendingMethod


class SendingPaymentController:

	@classmethod
	async def add_sending_method(cls,
								 session: AsyncSession,
								 name: str,
								 country_name: str,
								 number: str,
								 owner_name: str
								 ):
		new_sending_method = await send_payment_repository.create_sending_method(
			session=session,
			name=name,
			country_name=country_name,
			number=number,
			owner_name=owner_name
		)
		if not new_sending_method:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Invalid country name or account GUID."
			)
		return {
			"guid": new_sending_method.guid,
			"name": new_sending_method.name,
			"country": country_name,
			"number": number,
			"owner_name": owner_name
		}

	@classmethod
	async def get_sending_methods(cls, session: AsyncSession, country_name: str):
		methods = await send_payment_repository.list_sending_methods(session, country_name)
		if methods is None:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Country not found."
			)
		return [{"guid": method.guid, "name": method.name} for
				method in methods]

	@classmethod
	async def modify_sending_method(
			cls,
			session: AsyncSession,
			method_guid: uuid.UUID,
			name: str,
			number: str,
			owner_name: str
	):
		success = await send_payment_repository.update_method(
			session, method_guid, name, number, owner_name)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Sending method not found."
			)
		return {"detail": "Sending method updated successfully."}

	@classmethod
	async def remove_sending_method(cls, session: AsyncSession, method_guid: uuid.UUID):
		success = await send_payment_repository.delete_method(session, method_guid)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Sending method not found."
			)
		return {"detail": "Sending method deleted successfully."}
	

send_payment_controller = SendingPaymentController()