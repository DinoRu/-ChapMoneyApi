import uuid

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.transaction import ReceivingMethod
from app.repositories.receiving_method import receive_payment_repository
from app.schemas.receiving_method import CreateReceivingMethod, UpdateReceivingMethod, \
	ReceivingMethodOut


class ReceivePaymentController:

	@classmethod
	async def create(cls, session: AsyncSession,
					 country_name: str,
					 method_name: str, required_card: bool) -> ReceivingMethodOut:
		new_receiving_method = await receive_payment_repository.create_method(
			session=session,
			country_name=country_name,
			name=method_name,
			required_card=required_card
		)
		if not new_receiving_method:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="Invilid data passed."
			)
		return ReceivingMethodOut.from_orm(new_receiving_method)

	@classmethod
	async def all(cls, session: AsyncSession):
		methods = await receive_payment_repository.list_methods(session=session)
		if not methods:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Methods not found."
			)
		return [{"guid": method.guid, "name": method.name} for method in methods]

	@classmethod
	async def get_or_404(cls, session: AsyncSession, guid: str) -> ReceivingMethodOut:
		method = await receive_payment_repository.get_method(
			session=session,
			method_id=guid
		)
		if not method:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Method not found."
			)
		return ReceivingMethodOut.from_orm(method)

	@classmethod
	async def update_method(cls, session: AsyncSession, guid: str, data: UpdateReceivingMethod):
		success = await receive_payment_repository.update_method(
			session=session,
			method_id=guid,
			name=data.name,
			required_card=data.required_card
		)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Method not found."
			)
		return {"detail": "Method updated successfully."}

	@classmethod
	async def bulk_update(cls, session: AsyncSession, methods: list[UpdateReceivingMethod]):
		pass

	@classmethod
	async def delete(cls, method_id: uuid.UUID, session: AsyncSession):
		success = await receive_payment_repository.delete_method(session,method_id)
		if not success:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="Method not found."
			)
		return {"detail": "Method deleted successfully."}

	@classmethod
	async def bulk_delete(cls, session: AsyncSession):
		pass


receive_payment_controller = ReceivePaymentController()